
// --- Enhanced Photo Talking Avatar -------------------------------------------
// Canvas-based animation with frequency-band lip sync, idle breathing,
// multi-axis head movement, and smooth state transitions.
// Uses _joiActiveAudio / _joiIsSpeaking bridge set by speak().
(function(){
  try {
    const visual = document.getElementById('avatar-visual');
    const img = document.getElementById('avatar-image');
    if (!visual || !img) return;

    // Create canvas overlay
    let canvas = document.getElementById('avatar-talk-canvas');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.id = 'avatar-talk-canvas';
      visual.appendChild(canvas);
    }
    const ctx = canvas.getContext('2d');

    // Offscreen canvas for blink/mouth transforms (putImageData ignores transforms,
    // so we stage pixels here then use drawImage which DOES respect transforms)
    const _offCanvas = document.createElement('canvas');
    const _offCtx = _offCanvas.getContext('2d');

    // Track whether canvas has drawn at least one good frame.
    // Only then do we hide the <img> underneath.
    let _canvasReady = false;

    // --- Tunables (mutable — updated per-avatar from server) ----------------
    let FACE = {
      mx: 0.50, my: 0.50, mw: 0.20, mh: 0.09,   // mouth box
      ex: 0.55, ey: 0.32, ew: 0.28, eh: 0.08,     // eye/blink box
    };
    // Apply face coords from server response
    function applyFaceCoords(face) {
      if (!face) return;
      for (const k of ['mx','my','mw','mh','ex','ey','ew','eh']) {
        if (typeof face[k] === 'number') FACE[k] = face[k];
      }
    }
    // Save current FACE coords to server for this avatar
    async function saveFaceCoords() {
      try {
        const r = await fetch('/avatar/face', {
          method: 'POST', headers: {'Content-Type':'application/json'},
          body: JSON.stringify({face: FACE})
        });
        const d = await r.json();
        if (d.ok) toast('Face calibration saved');
        else toast(d.error || 'Save failed');
      } catch(e) { toast(e.message); }
    }
    // Sync sidebar sliders to current FACE values
    function fcSync() {
      for (const k of ['mx','my','mw','mh','ex','ey','ew','eh']) {
        const slider = document.getElementById('fc-' + k);
        const label = document.getElementById('fc-' + k + '-val');
        if (slider) slider.value = FACE[k];
        if (label) label.textContent = FACE[k].toFixed(2);
      }
    }
    // Expose globally so sidebar / console can call it
    window.applyFaceCoords = function(face) {
      applyFaceCoords(face);
      fcSync();
    };
    window.saveFaceCoords = saveFaceCoords;
    window.FACE = FACE;
    // Called by slider oninput — live preview as you drag
    window.fcUpdate = function(key, val) {
      const v = parseFloat(val);
      if (!isNaN(v)) FACE[key] = v;
      const label = document.getElementById('fc-' + key + '-val');
      if (label) label.textContent = v.toFixed(2);
    };
    // Initial sync on page load
    setTimeout(fcSync, 500);

    // --- Audio bridge (reads globals set by speak()) ------------------------
    function getAudio() { return _joiActiveAudio; }

    // --- Web Audio analyser -------------------------------------------------
    let audioCtx = null, analyser = null, sourceNode = null;
    let _lastConnectedAudio = null;
    const timeDomain = new Uint8Array(512);
    const freqData = new Uint8Array(128);

    // Smoothed mouth parameters
    let mouthOpen = 0, mouthWidth = 0, lipTension = 0, energy = 0;

    function ensureAnalyser() {
      const audio = getAudio();
      if (!audio) return null;

      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      if (!analyser) {
        analyser = audioCtx.createAnalyser();
        analyser.fftSize = 256;
        analyser.smoothingTimeConstant = 0.82;
      }

      // Reconnect if the audio element changed (each speak() creates a new Audio)
      if (audio !== _lastConnectedAudio) {
        try { if (sourceNode) sourceNode.disconnect(); } catch(e){}
        try {
          sourceNode = audioCtx.createMediaElementSource(audio);
          sourceNode.connect(analyser);
          analyser.connect(audioCtx.destination);
          _lastConnectedAudio = audio;
        } catch(e) {
          // MediaElementSource can only be created once per element
          console.warn('Avatar analyser reconnect:', e.message);
        }
      }
      return audio;
    }

    // --- Frequency-band analysis --------------------------------------------
    function updateAudioParams() {
      if (!analyser) return;

      // Time-domain RMS for overall energy
      analyser.getByteTimeDomainData(timeDomain);
      let sum = 0;
      for (let i = 0; i < timeDomain.length; i++) {
        const v = (timeDomain[i] - 128) / 128;
        sum += v * v;
      }
      const rms = Math.sqrt(sum / timeDomain.length);
      const rawEnergy = Math.min(1, Math.max(0, (rms - 0.02) * 7.0));

      // Frequency bands
      analyser.getByteFrequencyData(freqData);
      const binCount = freqData.length; // 128 bins

      // Bass (bins 0-4): mouth opening / jaw drop
      let bass = 0;
      for (let i = 0; i <= 4 && i < binCount; i++) bass += freqData[i];
      bass = Math.min(1, (bass / 5) / 180);

      // Low-mids (bins 5-12): mouth width
      let lowMid = 0;
      for (let i = 5; i <= 12 && i < binCount; i++) lowMid += freqData[i];
      lowMid = Math.min(1, (lowMid / 8) / 160);

      // High-mids (bins 13-25): lip tension / consonants
      let hiMid = 0;
      for (let i = 13; i <= 25 && i < binCount; i++) hiMid += freqData[i];
      hiMid = Math.min(1, (hiMid / 13) / 140);

      // Smooth with exponential moving average
      const s = 0.35; // responsiveness (higher = snappier)
      mouthOpen  = mouthOpen  * (1-s) + bass     * s;
      mouthWidth = mouthWidth * (1-s) + lowMid   * s;
      lipTension = lipTension * (1-s) + hiMid    * s;
      energy     = energy     * 0.75  + rawEnergy * 0.25;
    }

    // --- Blink system -------------------------------------------------------
    let blinking = false;
    let blinkScaleY = 1.0; // 1 = open, 0.18 = closed, 0.4 = half-blink
    let blinkTarget = 0.18;

    function scheduleBlink() {
      // Speaking: blink every 2-5s. Idle: every 3-7s.
      const isSpeakingNow = _joiIsSpeaking;
      const minDelay = isSpeakingNow ? 2000 : 3000;
      const maxDelay = isSpeakingNow ? 5000 : 7000;
      const delay = minDelay + Math.random() * (maxDelay - minDelay);

      setTimeout(() => {
        // Decide blink type
        const r = Math.random();
        if (r < 0.15) {
          // Double blink
          doBlink(0.18, 100 + Math.random() * 60, () => {
            setTimeout(() => {
              doBlink(0.18, 80 + Math.random() * 40, () => scheduleBlink());
            }, 80);
          });
        } else if (r < 0.30) {
          // Half blink
          doBlink(0.4, 100 + Math.random() * 40, () => scheduleBlink());
        } else {
          // Normal blink
          doBlink(0.18, 100 + Math.random() * 60, () => scheduleBlink());
        }
      }, delay);
    }

    function doBlink(closeAmount, duration, callback) {
      blinking = true;
      blinkTarget = closeAmount;
      setTimeout(() => {
        blinking = false;
        if (callback) callback();
      }, duration);
    }

    scheduleBlink();

    // --- Speaking blend (smooth transition) ----------------------------------
    let speakingBlend = 0; // 0 = idle, 1 = fully speaking

    // --- Idle animation state -----------------------------------------------
    let idleMicroExprTimer = 8000 + Math.random() * 7000;
    let idleMicroExprActive = false;
    let idleMicroExprStart = 0;
    let lastTickTime = Date.now();

    // --- Canvas sizing (runs every tick to handle hidden→visible transition) --
    let _lastCanvasW = 0, _lastCanvasH = 0;
    function resize() {
      const r = visual.getBoundingClientRect();
      if (r.width < 1 || r.height < 1) return; // still hidden, skip
      const dpr = Math.max(1, window.devicePixelRatio || 1);
      const needW = Math.floor(r.width * dpr);
      const needH = Math.floor(r.height * dpr);
      if (needW !== _lastCanvasW || needH !== _lastCanvasH) {
        canvas.width = needW;
        canvas.height = needH;
        _lastCanvasW = needW;
        _lastCanvasH = needH;
      }
    }
    resize();
    window.addEventListener('resize', resize);

    // --- Draw: base portrait with offset ------------------------------------
    function drawBase(dx, dy, scale) {
      // Re-check canvas size each frame (catches container becoming visible after login)
      resize();

      const w = canvas.width, h = canvas.height;
      ctx.clearRect(0, 0, w, h);
      if (w < 4 || h < 4) return; // canvas still too small (container hidden)
      if (!img.complete || !img.naturalWidth) return;

      ctx.save();
      const cx = w / 2, cy = h / 2, rad = Math.min(w, h) / 2;
      ctx.beginPath();
      ctx.arc(cx, cy, rad, 0, Math.PI * 2);
      ctx.closePath();
      ctx.clip();

      const iw = img.naturalWidth, ih = img.naturalHeight;
      const s = Math.max(w / iw, h / ih) * scale;
      const sw = iw * s, sh = ih * s;
      const x = (w - sw) / 2 + dx;
      const y = (h - sh) / 2 + dy;
      ctx.drawImage(img, x, y, sw, sh);

      ctx.restore();

      // First successful draw — hide the static <img> so canvas is the sole visible layer
      if (!_canvasReady) {
        _canvasReady = true;
        img.style.opacity = '0';
      }
    }

    // --- Draw: enhanced mouth warp ------------------------------------------
    function drawMouthWarp(openAmt, widthAmt) {
      if (!img.complete || !img.naturalWidth) return;
      const w = canvas.width, h = canvas.height;

      const boxW = FACE.mw * w;
      const boxH = FACE.mh * h;
      const boxX = (FACE.mx * w) - boxW / 2;
      const boxY = (FACE.my * h) - boxH / 2;

      const sx = Math.max(0, Math.floor(boxX));
      const sy = Math.max(0, Math.floor(boxY));
      const sw = Math.max(1, Math.floor(boxW));
      const sh = Math.max(1, Math.floor(boxH));

      let mouthData;
      try { mouthData = ctx.getImageData(sx, sy, sw, sh); } catch(e) { return; }

      // Stage pixels on offscreen canvas (putImageData ignores transforms!)
      _offCanvas.width = sw;
      _offCanvas.height = sh;
      _offCtx.putImageData(mouthData, 0, 0);

      const scaleY = 1 + 0.55 * openAmt;
      const scaleX = 1 + 0.15 * widthAmt;
      const midY = boxY + boxH / 2;
      const midX = boxX + boxW / 2;

      // Shift mouth region down slightly when open wide
      const dropY = openAmt * 2.0;

      ctx.save();
      ctx.beginPath();
      ctx.arc(w / 2, h / 2, Math.min(w, h) / 2, 0, Math.PI * 2);
      ctx.clip();

      // Clear original mouth region before redrawing transformed
      ctx.clearRect(sx, sy, sw, sh);

      ctx.translate(midX, midY + dropY);
      ctx.scale(scaleX, scaleY);
      ctx.translate(-midX, -(midY + dropY));

      // drawImage respects canvas transforms (unlike putImageData)
      ctx.drawImage(_offCanvas, sx, sy);
      ctx.restore();

      // Inner-mouth shadow — shape varies with width
      ctx.save();
      ctx.beginPath();
      ctx.arc(w / 2, h / 2, Math.min(w, h) / 2, 0, Math.PI * 2);
      ctx.clip();

      const shadowAlpha = 0.15 + 0.40 * openAmt;
      ctx.fillStyle = `rgba(0,0,0,${shadowAlpha})`;
      ctx.globalCompositeOperation = 'multiply';

      // Narrow "oh" vs wide "ah" shadow
      const shadowWidth = 0.40 + 0.24 * widthAmt;
      const shadowInset = (1 - shadowWidth) / 2;
      ctx.fillRect(
        boxX + boxW * shadowInset,
        boxY + boxH * 0.50 + dropY,
        boxW * shadowWidth,
        boxH * 0.32
      );

      ctx.restore();
      ctx.globalCompositeOperation = 'source-over';
    }

    // --- Draw: blink overlay ------------------------------------------------
    function drawBlink() {
      // Smoothly interpolate blinkScaleY
      const target = blinking ? blinkTarget : 1.0;
      blinkScaleY += (target - blinkScaleY) * 0.35;
      if (Math.abs(blinkScaleY - 1.0) < 0.01 && !blinking) return; // fully open, skip

      const w = canvas.width, h = canvas.height;
      const boxW = FACE.ew * w;
      const boxH = FACE.eh * h;
      const boxX = (FACE.ex * w) - boxW / 2;
      const boxY = (FACE.ey * h) - boxH / 2;

      const sx = Math.max(0, Math.floor(boxX));
      const sy = Math.max(0, Math.floor(boxY));
      const sw = Math.max(1, Math.floor(boxW));
      const sh = Math.max(1, Math.floor(boxH));

      let eyeData;
      try { eyeData = ctx.getImageData(sx, sy, sw, sh); } catch(e) { return; }

      // Stage on offscreen canvas (putImageData ignores transforms!)
      _offCanvas.width = sw;
      _offCanvas.height = sh;
      _offCtx.putImageData(eyeData, 0, 0);

      const midY = boxY + boxH / 2;

      ctx.save();
      ctx.beginPath();
      ctx.arc(w / 2, h / 2, Math.min(w, h) / 2, 0, Math.PI * 2);
      ctx.clip();

      // Clear eye region before redrawing transformed
      ctx.clearRect(sx, sy, sw, sh);

      ctx.translate(0, midY);
      ctx.scale(1, blinkScaleY);
      ctx.translate(0, -midY);

      // drawImage respects canvas transforms (unlike putImageData)
      ctx.drawImage(_offCanvas, sx, sy);
      ctx.restore();

      // Eyelid shadow
      if (blinkScaleY < 0.85) {
        const shadowAlpha = 0.25 * (1 - blinkScaleY);
        ctx.save();
        ctx.beginPath();
        ctx.arc(w / 2, h / 2, Math.min(w, h) / 2, 0, Math.PI * 2);
        ctx.clip();
        ctx.fillStyle = `rgba(0,0,0,${shadowAlpha})`;
        ctx.globalCompositeOperation = 'multiply';
        ctx.fillRect(boxX, boxY, boxW, boxH);
        ctx.restore();
        ctx.globalCompositeOperation = 'source-over';
      }
    }

    // --- Main tick ----------------------------------------------------------
    function tick() {
      const t = Date.now();
      const dt = t - lastTickTime;
      lastTickTime = t;

      // Determine speaking state from bridge variables
      const audio = ensureAnalyser();
      const isSpeakingNow = _joiIsSpeaking &&
        (audio ? (!audio.paused && !audio.ended && audio.currentTime > 0) : _joiIsSpeaking);

      // Update speaking blend (ramp up 200ms, ramp down 400ms)
      if (isSpeakingNow) {
        speakingBlend = Math.min(1, speakingBlend + dt / 200);
      } else {
        speakingBlend = Math.max(0, speakingBlend - dt / 400);
      }

      // Update audio analysis if speaking
      if (isSpeakingNow && analyser) {
        updateAudioParams();
      } else {
        // Decay parameters when not speaking
        mouthOpen  *= 0.88;
        mouthWidth *= 0.88;
        lipTension *= 0.88;
        energy     *= 0.90;
      }

      // --- Head position: blend speaking movement + idle breathing ---

      // Speaking: multi-axis movement
      const spkBobY  = 2.5 * Math.sin(t / 160) * energy;
      const spkSwayX = 1.5 * Math.sin(t / 230) * energy;

      // Idle: breathing + micro-sway
      const idleBreathY = 0.6 * Math.sin(t / 2000);
      const idleSwayX   = 0.5 * Math.sin(t / 3500);
      const idleScale   = 1 + 0.003 * Math.sin(t / 2500);

      // Blend
      const headX = spkSwayX * speakingBlend + idleSwayX * (1 - speakingBlend);
      const headY = spkBobY * speakingBlend + idleBreathY * (1 - speakingBlend);
      const headScale = 1 * speakingBlend + idleScale * (1 - speakingBlend);

      drawBase(headX, headY, headScale);

      // --- Mouth warp ---
      // Speaking: use frequency-band parameters
      // Idle: occasional micro-expression
      let finalMouthOpen = mouthOpen * speakingBlend;
      let finalMouthWidth = mouthWidth * speakingBlend;

      // Idle micro-expression (subtle mouth curve every 10-15s)
      if (speakingBlend < 0.1) {
        idleMicroExprTimer -= dt;
        if (idleMicroExprTimer <= 0 && !idleMicroExprActive) {
          idleMicroExprActive = true;
          idleMicroExprStart = t;
          idleMicroExprTimer = 10000 + Math.random() * 5000;
        }
        if (idleMicroExprActive) {
          const elapsed = t - idleMicroExprStart;
          if (elapsed > 800) {
            idleMicroExprActive = false;
          } else {
            const curve = Math.sin((elapsed / 800) * Math.PI);
            finalMouthOpen += 0.03 * curve;
            finalMouthWidth += 0.02 * curve;
          }
        }
      }

      if (finalMouthOpen > 0.01 || finalMouthWidth > 0.01) {
        drawMouthWarp(finalMouthOpen, finalMouthWidth);
      }

      // --- Blink ---
      drawBlink();

      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);

    // Allow AudioContext to resume after first user gesture
    window.addEventListener('pointerdown', () => {
      try { if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume(); } catch(e) {}
    }, { passive: true });

  } catch (e) {
    console.warn('Enhanced avatar animation failed:', e);
    // Restore original image if canvas animation fails
    const fallbackImg = document.getElementById('avatar-image');
    if (fallbackImg) fallbackImg.style.opacity = '1';
  }
})();
