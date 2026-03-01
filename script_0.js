
// =====================================================================
// STATE
// =====================================================================
let isLoggedIn = false, isAdmin = false;
let currentImage = null, selectedVoice = null, isSpeaking = false;
let voiceMode = 'kokoro'; // 'kokoro' (local Kokoro AI) or 'edge' (free Edge TTS)
let particles = [];
let recognition = null;   // SpeechRecognition instance (persistent)
let micActive = false;    // is the always-on mic running?
let ttsActive = false;    // true while Joi is speaking — mic ignores input
let lastJoiReply = '';    // last Joi reply text — used to filter echo
let _joiActiveAudio = null;   // Set by speak(), read by canvas animation engine
let _joiIsSpeaking = false;   // True while TTS audio is playing
let useServerSTT = false;     // Server-side Whisper + speaker ID
let _sttMediaRecorder = null; // MediaRecorder for server STT
let _sttStream = null;        // MediaStream for mic capture
let _sttChunkTimer = null;    // Interval for sending audio chunks

// =====================================================================
// HEX RAIN BACKGROUND (Matrix-style falling green characters)
// =====================================================================
let _hexRainRaf = null;
function initHexRain() {
    if (_hexRainRaf) { cancelAnimationFrame(_hexRainRaf); _hexRainRaf = null; }
    const canvas  = document.getElementById('hex-rain-canvas');
    if (!canvas) return;
    const wrapper = document.getElementById('chat-wrapper');
    if (!wrapper) return;

    // Katakana + half-width katakana + latin + digits — true Matrix feel
    const kata = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンァィゥェォッャュョ';
    const hkata= 'ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ';
    const latin = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%&?!<>[]';
    const charArr = (kata + hkata + latin).split('');

    const FS = 14;            // px per character cell — smaller = denser rain
    const FADE = 0.040;       // trail fade per frame (lower = longer trails)
    const SPEED_MIN = 0.35;
    const SPEED_MAX = 1.45;
    const TRAIL_FLICKER = 0.08; // probability a trail char redraws (shimmer)

    let drops = [], cols = 0, raf = null;

    function rndChar() { return charArr[Math.floor(Math.random() * charArr.length)]; }

    function resize() {
        const rect = wrapper.getBoundingClientRect();
        const dpr  = Math.min(window.devicePixelRatio || 1, 2);
        canvas.width  = Math.round(rect.width  * dpr);
        canvas.height = Math.round(rect.height * dpr);
        canvas.style.width  = rect.width  + 'px';
        canvas.style.height = rect.height + 'px';
        const ctx = canvas.getContext('2d');
        ctx.scale(dpr, dpr);

        cols = Math.floor(rect.width / FS);
        drops = Array.from({ length: cols }, (_, i) => ({
            y:     -(Math.random() * rect.height / FS * 1.5),  // staggered starts above screen
            speed: SPEED_MIN + Math.random() * (SPEED_MAX - SPEED_MIN),
            // Each column carries a trail of mutable characters
            trail: Array.from({ length: 32 }, () => rndChar()),
        }));
    }

    function draw() {
        if (!wrapper || !canvas) return;
        const rect = wrapper.getBoundingClientRect();
        const ctx  = canvas.getContext('2d');
        const W = rect.width, H = rect.height;

        // Fade background — this creates the trailing effect
        ctx.fillStyle = `rgba(0,0,0,${FADE})`;
        ctx.fillRect(0, 0, W, H);

        ctx.font = `bold ${FS}px "Courier New", monospace`;
        ctx.textBaseline = 'top';

        for (let i = 0; i < drops.length; i++) {
            const d  = drops[i];
            const x  = i * FS;
            const hy = Math.floor(d.y); // head row (in char units)

            // ── Draw trail characters below the head ──────────────────────
            // We draw from the head UP so earlier chars are dimmer via fade
            // The canvas fade (fillRect above) handles most of it;
            // we boost a few positions for realism
            const trailLen = d.trail.length;
            for (let j = 0; j < Math.min(trailLen, 6); j++) {
                const row = hy - j;
                if (row < 0) continue;
                const py = row * FS;
                if (py >= H) continue;

                if (Math.random() < TRAIL_FLICKER) {
                    d.trail[j] = rndChar(); // shimmer — char changes randomly
                }

                if (j === 0) {
                    // HEAD — bright near-white green, full glow
                    ctx.fillStyle = `rgba(200,255,210,${0.92 + Math.random() * 0.08})`;
                } else if (j === 1) {
                    ctx.fillStyle = `rgba(100,255,120,0.88)`;
                } else if (j === 2) {
                    ctx.fillStyle = `rgba(0,230,70,0.72)`;
                } else {
                    // Dimming tail — rendered once here, faded each frame by fillRect
                    const a = 0.55 - j * 0.09;
                    ctx.fillStyle = `rgba(0,${180 + j * 12},${40 + j * 5},${Math.max(a, 0.1)})`;
                }
                ctx.fillText(d.trail[j], x, py);
            }

            // Advance drop
            d.y += d.speed;

            // Reset when the head is well past the bottom
            if (d.y * FS > H + trailLen * FS * 2) {
                d.y     = -(5 + Math.random() * 30);
                d.speed = SPEED_MIN + Math.random() * (SPEED_MAX - SPEED_MIN);
                // Refresh trail chars on reset
                for (let k = 0; k < trailLen; k++) d.trail[k] = rndChar();
            }
        }

        _hexRainRaf = raf = requestAnimationFrame(draw);
    }

    resize();
    if (typeof ResizeObserver !== 'undefined') {
        new ResizeObserver(resize).observe(wrapper);
    }
    window.addEventListener('resize', resize);
    _hexRainRaf = raf = requestAnimationFrame(draw);
}

// =====================================================================
// INIT
// =====================================================================
document.addEventListener('DOMContentLoaded', () => {
    autoResizeTextarea();
    loadVoices();
    loadVoiceMode();
    loadMode();
    loadCommentary();
    loadServerSTTStatus();
    // restore bg prefs
    const bg = localStorage.getItem('joi-bg-image');
    if (bg) document.documentElement.style.setProperty('--bg-image', `url(${bg})`);
    const col = localStorage.getItem('joi-bg-color');
    if (col) { document.documentElement.style.setProperty('--bg', col); document.getElementById('bg-color-input').value = col; }
    if (window.speechSynthesis && window.speechSynthesis.onvoiceschanged !== undefined)
        window.speechSynthesis.onvoiceschanged = loadVoices;
});

function autoResizeTextarea() {
    const ta = document.getElementById('message-input');
    ta.addEventListener('input', function(){ this.style.height='auto'; this.style.height=this.scrollHeight+'px'; });
}

// =====================================================================
// LOGIN / LOGOUT
// =====================================================================
async function login(admin = false) {
    const pw = document.getElementById('password-input').value;
    if (!pw) return toast('Enter a password');
    try {
        const r = await fetch('/login', {method:'POST', headers:{'Content-Type':'application/json'},
                                         body: JSON.stringify({password:pw, admin})});
        const d = await r.json();
        if (d.ok) {
            isLoggedIn = true; isAdmin = d.admin;
            document.getElementById('login-screen').classList.add('hidden');
            document.getElementById('app-container').classList.add('active');
            // load everything
            await loadAvatar();
            await loadAvatarSwitcher();
            await loadHistory();
            await loadProjects();
            startCreditPolling();
            initHexRain();
            // initializeAvatar(); // disabled to reduce CPU (particle loop)
            speak("Hello, Lonnie. I've missed you.");
        } else { toast(d.error || 'Login failed'); }
    } catch(e) { toast('Login error: '+e.message); }
}

async function logout() {
    try { await fetch('/logout', {method:'POST'}); } catch(e){}
    location.reload();
}

// =====================================================================
// CHAT
// =====================================================================
function showChatThinking() {
    hideChatThinking(); // remove any existing
    const log = document.getElementById('chat-log');
    const div = document.createElement('div');
    div.className = 'chat-thinking';
    div.id = 'chat-thinking-indicator';
    div.innerHTML = '<span class="thinking-label">Joi is thinking</span>' +
        '<div class="thinking-dots"><span></span><span></span><span></span></div>';
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;
}
function hideChatThinking() {
    const el = document.getElementById('chat-thinking-indicator');
    if (el) el.remove();
}

async function sendMessage() {
    const input = document.getElementById('message-input');
    const msg = input.value.trim();
    if (!msg && !currentImage) return;

    addMessage('user', msg, currentImage);
    input.value = ''; input.style.height = 'auto';
    const tmpImg = currentImage; currentImage = null;

    const btn = document.getElementById('send-btn');
    btn.disabled = true; btn.innerHTML = '<span style="font-size:13px">…</span>';

    // Start brain processing animation if dock is open
    if (_brainDockOpen) startProcessingAnimation();

    // Show thinking indicator in chat
    showChatThinking();

    try {
        if (_brainDockOpen) setTimeout(loadBrainState, 350);
        const r = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'},
                                        body: JSON.stringify({message: msg, image: tmpImg})});
        const d = await r.json();
        hideChatThinking();
        if (d.ok) {
            addMessage('assistant', d.reply, null, {memory_used: d.memory_used});
            if (d.model) {
                const mi = document.getElementById('model-indicator');
                const dot = document.getElementById('model-dot');
                const badge = document.getElementById('mode-badge');
                const span = mi.querySelector('span:first-child') || mi;
                span.innerHTML = '';
                span.appendChild(dot);
                span.appendChild(document.createTextNode(' ' + d.model));
                // Color the dot by provider
                const m = d.model.toLowerCase();
                const orbKey = getOrbitalKey(m);
                const orbColors = {'openai':'#10a37f','gemini-high':'#4285f4','gemini-fast':'#34a853','gemini-lite':'#fbbc05','local':'#ff6600'};
                dot.style.background = orbColors[orbKey] || '#888';
            }
            speak(d.reply);
            // refresh sidebars if avatar/project actions happened
            if (d.reply.toLowerCase().includes('avatar') || d.reply.toLowerCase().includes('appearance'))
                { await loadAvatar(); await loadAvatarSwitcher(); }
            if (d.reply.toLowerCase().includes('project') || d.reply.toLowerCase().includes('organised'))
                await loadProjects();
            // Auto-open terminal dock when orchestration starts
            if (d.orchestration_started || (d.reply && d.reply.toLowerCase().includes('orchestration started'))) {
                if (!_termDockOpen) toggleTerminalDock();
            }
            // Update brain map with latest state (real-time)
            if (d.brain_state) updateBrainMapFromResponse(d.brain_state);
            // add to history sidebar live
            appendHistoryItem({role:'user', content:msg});
            appendHistoryItem({role:'assistant', content:d.reply});
        } else { addMessage('assistant', 'Error: '+(d.error||'Unknown')); }
    } catch(e) { hideChatThinking(); addMessage('assistant', 'Error: '+e.message); stopProcessingAnimation(); }
    finally { btn.disabled=false; btn.innerHTML='➤'; }
}

function addMessage(role, content, imageData=null, opts={}) {
    const log = document.getElementById('chat-log');
    const wrap = document.createElement('div');
    wrap.className = 'message '+role;

    const hdr = document.createElement('div');
    hdr.className = 'message-header';
    hdr.textContent = role==='user' ? 'Lonnie' : 'Joi';

    const body = document.createElement('div');
    body.className = 'message-content';

    if (imageData) {
        const img = document.createElement('img');
        img.src = imageData; img.style.maxWidth='260px'; img.style.borderRadius='10px'; img.style.marginBottom='6px';
        body.appendChild(img);
        body.appendChild(document.createElement('br'));
    }

    // Render download links — handle sandbox: hallucinations, /download/, /file/
    let rendered = content;
    // 1. Rewrite sandbox:/file:// markdown links → extract filename, serve from /file/
    rendered = rendered.replace(/\[([^\]]+)\]\((?:sandbox:|file:\/\/)[^)]*\/([^/)]+\.[a-z0-9]+)\)/gi,
        '<a class="file-link" href="/file/project/assets/files/$2" download="$2">📥 $1</a>');
    // 2. Catch raw sandbox: URLs not in markdown links
    rendered = rendered.replace(/(?<!\()(?:sandbox:|file:\/\/)[^\s<)]*\/([^\s</)]+\.[a-z0-9]+)/gi,
        '<a class="file-link" href="/file/project/assets/files/$1" download="$1">📥 $1</a>');
    // 3. Render /download/<id> links (correct backend URLs)
    rendered = rendered.replace(/\[([^\]]+)\]\((\/download\/[^)]+)\)/g,
        '<a class="file-link" href="$2" download>📥 $1</a>');
    // 4. Render /file/ links
    rendered = rendered.replace(/\[([^\]]+)\]\((\/file\/[^)]+)\)/g,
        '<a class="file-link" href="$2" download>📥 $1</a>');
    body.innerHTML += rendered;

    wrap.appendChild(hdr);
    wrap.appendChild(body);

    // Memory-used indicator for assistant messages
    if (role === 'assistant' && opts.memory_used && opts.memory_used.count > 0) {
        const mem = document.createElement('div');
        mem.style.cssText = 'font-size:11px;color:var(--secondary);margin-top:4px;cursor:pointer;opacity:0.7;';
        mem.textContent = '\uD83E\uDDE0 ' + opts.memory_used.count + ' memor' + (opts.memory_used.count === 1 ? 'y' : 'ies');
        mem.title = 'Click to see which memories were used';
        mem.onclick = function() {
            let detail = this.nextElementSibling;
            if (detail) { detail.style.display = detail.style.display === 'none' ? 'block' : 'none'; return; }
            detail = document.createElement('div');
            detail.style.cssText = 'font-size:11px;color:#aaa;margin-top:4px;padding:6px;background:rgba(0,0,0,0.3);border-radius:6px;';
            (opts.memory_used.items||[]).forEach(item => {
                detail.innerHTML += '<div>[' + item.type + '] score=' + item.score + ' id=' + item.id + '</div>';
            });
            this.parentNode.insertBefore(detail, this.nextSibling);
        };
        wrap.appendChild(mem);
    }

    log.appendChild(wrap);
    log.scrollTop = log.scrollHeight;
}

// =====================================================================
// TTS + LIP-SYNC
// =====================================================================
async function speak(text) {
    if (!text || isSpeaking) return;
    isSpeaking = true;
    ttsActive = true;
    lastJoiReply = text.toLowerCase().replace(/[^a-z0-9 ]/g, '').trim();
    document.getElementById('avatar-visual').classList.add('speaking');

    // Pause mic while speaking to prevent feedback loop
    if (recognition && micActive) {
        try { recognition.stop(); } catch(_){}
        _micDbg('event', 'paused-for-tts');
    }

    // Prefer server TTS if available; fall back cleanly if endpoint is missing or returns non-JSON.
    try {
        const r = await fetch('/tts', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ text, voice_mode: voiceMode })
        });

        const ct = (r.headers.get('content-type') || '').toLowerCase();
        if (!r.ok || !ct.includes('application/json')) throw new Error('TTS endpoint unavailable');

        const d = await r.json();
        if (d.ok && d.url) {
            const audio = new Audio(d.url);
            _joiActiveAudio = audio;
            _joiIsSpeaking = true;
            audio.onended = () => {
                _joiIsSpeaking = false;
                _joiActiveAudio = null;
                isSpeaking = false;
                document.getElementById('avatar-visual').classList.remove('speaking');
                _resumeMicAfterTTS();
            };
            audio.onerror = () => {
                _joiIsSpeaking = false;
                _joiActiveAudio = null;
                isSpeaking = false;
                document.getElementById('avatar-visual').classList.remove('speaking');
                useBrowserTTS(text);
            };
            await audio.play();
            return;
        }
        throw new Error('TTS bad payload');
    } catch (e) {
        useBrowserTTS(text);
    }
}

function useBrowserTTS(text) {
    const u = new SpeechSynthesisUtterance(text);
    if (selectedVoice) u.voice = selectedVoice;
    u.rate=0.95; u.pitch=1.1;
    u.onstart = () => { _joiIsSpeaking = true; };
    u.onend   = () => { _joiIsSpeaking=false; _joiActiveAudio=null; isSpeaking=false; document.getElementById('avatar-visual').classList.remove('speaking'); _resumeMicAfterTTS(); };
    window.speechSynthesis.speak(u);
}

function _resumeMicAfterTTS() {
    // Wait 400ms after TTS ends before re-enabling mic to avoid echo pickup
    setTimeout(() => {
        ttsActive = false;
        if (micActive && recognition) {
            try { recognition.start(); _micDbg('event', 'resumed-after-tts'); }
            catch(_) {}
        }
    }, 400);
}

// Old startLipSync/stopLipSync removed — canvas animation engine handles all avatar movement

// =====================================================================
// KOKORO STATUS BADGE (replaces ElevenLabs credits tracker)
// =====================================================================
async function loadKokoroStatus() {
    try {
        const r = await fetch('/kokoro/voices');
        if (!r.ok) return;
        const d = await r.json();
        const badge = document.getElementById('voice-status-badge');
        const label = document.getElementById('vs-label');
        const dot   = document.getElementById('vs-dot');
        if (!badge) return;
        badge.style.display = '';
        if (d.available) {
            if (label) label.textContent = 'Kokoro AI';
            if (dot)   dot.style.background = 'var(--secondary)';
            badge.title = 'Kokoro AI — local TTS, no credits needed. Click to open Voice Creator.';
        } else {
            if (label) label.textContent = 'Edge TTS';
            if (dot)   dot.style.background = '#ffaa00';
            badge.title = 'Kokoro not loaded — using Edge TTS free fallback. Click to open Voice Creator.';
        }
    } catch(_) {}
}

// Kept for call-site compatibility (called after login)
function startCreditPolling() {
    loadKokoroStatus();
}

// =====================================================================
// VOICE MODE (Kokoro AI / Edge TTS toggle)
// =====================================================================
async function loadVoiceMode() {
    try {
        const r = await fetch('/tts/mode');
        if (r.ok) {
            const d = await r.json();
            if (d.ok) {
                // Normalise legacy mode names
                voiceMode = (d.mode === 'ariana' || d.mode === 'elevenlabs') ? 'kokoro' : d.mode;
                _updateVoiceModeUI();
            }
        }
    } catch(_) {}
}

async function setVoiceMode(mode) {
    voiceMode = mode;
    _updateVoiceModeUI();
    try {
        const r = await fetch('/tts/mode', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ mode })
        });
        if (r.ok) {
            const d = await r.json();
            const status = document.getElementById('voice-mode-status');
            if (status) status.textContent = d.engine === 'kokoro' ? 'Using Kokoro AI (local)' : 'Using Edge TTS (free cloud)';
            toast(mode === 'kokoro' ? 'Voice: Kokoro AI (Local)' : 'Voice: Edge TTS (Free)');
        }
    } catch(e) {
        toast('Failed to set voice mode');
    }
}

function _updateVoiceModeUI() {
    const btnK = document.getElementById('btn-voice-kokoro');
    const btnE = document.getElementById('btn-voice-edge');
    if (!btnK || !btnE) return;
    if (voiceMode === 'kokoro') {
        btnK.style.borderColor = 'var(--accent)';
        btnK.style.background  = 'rgba(255,95,175,0.15)';
        btnK.style.color       = 'var(--accent)';
        btnE.style.borderColor = '#555';
        btnE.style.background  = 'transparent';
        btnE.style.color       = '#aaa';
    } else {
        btnE.style.borderColor = 'var(--accent)';
        btnE.style.background  = 'rgba(255,95,175,0.15)';
        btnE.style.color       = 'var(--accent)';
        btnK.style.borderColor = '#555';
        btnK.style.background  = 'transparent';
        btnK.style.color       = '#aaa';
    }
}

// =====================================================================
// VOICE CREATOR  (Kokoro-82M local TTS control panel)
// =====================================================================
let _vcKokoroVoices = [];
let _vcSelectedVoice = 'af_heart';

async function openVoiceCreator() {
    const modal = document.getElementById('voice-creator-modal');
    if (modal) modal.classList.add('active');
    await _vcLoadVoices();
    await _vcLoadSettings();
}

async function _vcLoadVoices() {
    try {
        const r = await fetch('/kokoro/voices');
        if (!r.ok) return;
        const d = await r.json();
        _vcKokoroVoices = d.voices || [];

        const banner = document.getElementById('vc-banner-text');
        const bannerEl = document.getElementById('vc-kokoro-banner');
        if (d.available) {
            if (bannerEl) bannerEl.style.borderColor = 'var(--secondary)';
            if (banner)   banner.innerHTML = '<strong style="color:var(--secondary);">Kokoro AI is ready</strong> — running locally on your machine. No API key or credits needed.';
        } else {
            if (bannerEl) bannerEl.style.borderColor = '#ffaa00';
            if (banner)   banner.innerHTML = '<strong style="color:#ffaa00;">Kokoro not loaded yet.</strong> On first use it downloads the model (~500 MB from HuggingFace). Edge TTS will be used as fallback.';
        }

        _vcRenderVoiceGrid();
    } catch(e) { console.warn('[VoiceCreator] loadVoices:', e); }
}

function _vcRenderVoiceGrid() {
    const grid = document.getElementById('vc-voice-grid');
    if (!grid) return;
    grid.innerHTML = '';
    _vcKokoroVoices.forEach(v => {
        const btn = document.createElement('button');
        btn.id = 'vcv-' + v.id;
        const active = v.id === _vcSelectedVoice;
        btn.style.cssText = `padding:8px 10px;border-radius:8px;border:2px solid ${active ? 'var(--accent)' : '#555'};background:${active ? 'rgba(255,95,175,0.15)' : 'transparent'};color:${active ? '#fff' : '#ccc'};cursor:pointer;font-size:12px;text-align:left;transition:all .2s;`;
        btn.innerHTML = `<strong style="display:block;color:${active ? '#fff' : '#ddd'};">${v.label}</strong><span style="color:#888;font-size:11px;">${v.desc}</span>`;
        btn.onclick = () => _vcSelectVoice(v.id);
        grid.appendChild(btn);
    });
}

function _vcSelectVoice(voiceId) {
    _vcSelectedVoice = voiceId;
    document.querySelectorAll('[id^="vcv-"]').forEach(btn => {
        btn.style.borderColor = '#555';
        btn.style.background  = 'transparent';
        btn.style.color       = '#ccc';
        btn.querySelector('strong').style.color = '#ddd';
    });
    const active = document.getElementById('vcv-' + voiceId);
    if (active) {
        active.style.borderColor = 'var(--accent)';
        active.style.background  = 'rgba(255,95,175,0.15)';
        active.style.color       = '#fff';
        active.querySelector('strong').style.color = '#fff';
    }
}

async function _vcLoadSettings() {
    try {
        const r = await fetch('/kokoro/settings');
        if (!r.ok) return;
        const d = await r.json();
        if (!d.ok) return;
        const s = d.settings;

        _vcSelectedVoice = s.voice || 'af_heart';

        const speedEl  = document.getElementById('vc-speed');
        const tempEl   = document.getElementById('vc-temp');
        const promptEl = document.getElementById('vc-voice-prompt');
        const speedVal = document.getElementById('vc-speed-val');
        const tempVal  = document.getElementById('vc-temp-val');

        if (speedEl)  { speedEl.value  = s.speed || 1.0; }
        if (speedVal) { speedVal.textContent = parseFloat(s.speed || 1.0).toFixed(2) + '×'; }
        if (tempEl)   { tempEl.value   = s.temperature || 0.5; }
        if (tempVal)  { tempVal.textContent  = parseFloat(s.temperature || 0.5).toFixed(2); }
        if (promptEl) { promptEl.value = s.voice_prompt || ''; }

        _vcRenderVoiceGrid();
        _vcRenderPresets(s.presets || {}, s.active_preset);

        // Sync sidebar voice label
        const vInfo = _vcKokoroVoices.find(v => v.id === _vcSelectedVoice);
        const lbl   = document.getElementById('sb-voice-label');
        if (lbl) lbl.textContent = `Voice: ${vInfo ? vInfo.label : _vcSelectedVoice} (Kokoro)`;
    } catch(e) { console.warn('[VoiceCreator] loadSettings:', e); }
}

function _vcRenderPresets(presets, activePreset) {
    const list = document.getElementById('vc-presets-list');
    if (!list) return;
    list.innerHTML = '';
    const entries = Object.entries(presets);
    if (!entries.length) {
        list.innerHTML = '<span style="font-size:12px;color:#666;">No presets saved yet.</span>';
        return;
    }
    entries.forEach(([name, p]) => {
        const isActive = name === activePreset;
        const btn = document.createElement('button');
        btn.style.cssText = `padding:5px 12px;border-radius:8px;border:2px solid ${isActive ? 'var(--secondary)' : '#555'};background:${isActive ? 'rgba(0,255,204,0.12)' : 'transparent'};color:#fff;cursor:pointer;font-size:12px;transition:all .2s;`;
        btn.textContent = p.label || name;
        btn.title = `Voice: ${p.voice}  |  Speed: ${p.speed}  |  Temp: ${p.temperature}`;
        btn.onclick = () => _vcLoadPreset(name);
        list.appendChild(btn);
    });
}

async function _vcLoadPreset(name) {
    try {
        const r = await fetch('/kokoro/settings', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ load_preset: name })
        });
        const d = await r.json();
        if (d.ok) { await _vcLoadSettings(); toast('Loaded preset: ' + name); }
    } catch(e) { toast('Failed to load preset'); }
}

async function saveVoicePreset() {
    const nameEl = document.getElementById('vc-new-preset-name');
    const name   = nameEl ? nameEl.value.trim() : '';
    if (!name) { toast('Enter a preset name'); return; }
    const speed       = parseFloat(document.getElementById('vc-speed')?.value || 1.0);
    const temperature = parseFloat(document.getElementById('vc-temp')?.value  || 0.5);
    const voice_prompt = document.getElementById('vc-voice-prompt')?.value || '';
    try {
        // First save current settings, then save preset
        await fetch('/kokoro/settings', {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ voice: _vcSelectedVoice, speed, temperature, voice_prompt })
        });
        const r = await fetch('/kokoro/settings', {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ save_preset: { name, label: name } })
        });
        const d = await r.json();
        if (d.ok) {
            if (nameEl) nameEl.value = '';
            _vcRenderPresets(d.settings.presets || {}, d.settings.active_preset);
            toast('Preset saved: ' + name);
        }
    } catch(e) { toast('Failed to save preset'); }
}

async function saveVoiceSettings() {
    const speed        = parseFloat(document.getElementById('vc-speed')?.value || 1.0);
    const temperature  = parseFloat(document.getElementById('vc-temp')?.value  || 0.5);
    const voice_prompt = document.getElementById('vc-voice-prompt')?.value || '';
    try {
        const r = await fetch('/kokoro/settings', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ voice: _vcSelectedVoice, speed, temperature, voice_prompt })
        });
        const d = await r.json();
        if (d.ok) {
            toast('Voice settings saved');
            const vInfo = _vcKokoroVoices.find(v => v.id === _vcSelectedVoice);
            const lbl   = document.getElementById('sb-voice-label');
            if (lbl) lbl.textContent = `Voice: ${vInfo ? vInfo.label : _vcSelectedVoice} (Kokoro)`;
            loadKokoroStatus();
        }
    } catch(e) { toast('Failed to save settings'); }
}

async function testKokoroVoice() {
    await saveVoiceSettings();
    isSpeaking = false; // reset flag so speak() will proceed
    const descEl = document.getElementById('vc-ai-desc');
    const desc = descEl && descEl.value.trim();
    const phrase = desc
        ? `Hello — I'm Joi. My voice was shaped by the description: "${desc.slice(0,80)}". How do I sound?`
        : "Hello, I'm Joi. My voice is powered by Kokoro, running entirely on your machine — no API key, no credits.";
    speak(phrase);
}

// ── Generate voice profile from natural-language description ─────────────────
async function generateVoiceFromDesc() {
    const descEl = document.getElementById('vc-ai-desc');
    const resultEl = document.getElementById('vc-desc-result');
    const desc = descEl ? descEl.value.trim() : '';
    if (!desc) { toast('✏️ Enter a description first'); return; }

    if (resultEl) {
        resultEl.style.display = 'block';
        resultEl.innerHTML = '<span style="color:#888;">⏳ Analysing description…</span>';
    }

    try {
        const r = await fetch('/kokoro/voice_from_desc', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ description: desc })
        });
        const d = await r.json();
        if (!d.ok) {
            if (resultEl) resultEl.innerHTML = `<span style="color:#ff4444;">Error: ${d.error}</span>`;
            return;
        }
        const p = d.profile;
        const tagsHtml = p.matched_tags.length
            ? p.matched_tags.map(t => `<span style="display:inline-block;padding:1px 8px;border-radius:12px;background:rgba(157,0,255,0.25);border:1px solid rgba(157,0,255,0.5);color:#d0a0ff;font-size:11px;margin:2px;">${t}</span>`).join('')
            : '<span style="color:#777;">no specific tags matched — using defaults</span>';

        if (resultEl) {
            resultEl.style.display = 'block';
            resultEl.innerHTML = `
                <div style="margin-bottom:6px;">
                  <strong style="color:var(--secondary);">✅ Voice Generated</strong>
                  <span style="float:right;color:#888;font-size:11px;">Settings applied</span>
                </div>
                <div style="margin:4px 0;"><span style="color:#aaa;">Voice:</span> <strong style="color:#fff;">${p.voice}</strong> &nbsp; <span style="color:#aaa;">Speed:</span> <strong style="color:var(--secondary);">${p.speed}×</strong> &nbsp; <span style="color:#aaa;">Temp:</span> <strong style="color:var(--accent);">${p.temperature}</strong></div>
                <div style="margin-top:6px;"><span style="color:#aaa;font-size:11px;">Matched tags:</span><br/>${tagsHtml}</div>`;
        }

        // Refresh sliders + voice grid to reflect the new settings
        await _vcLoadSettings();
        toast('✨ Voice profile generated from description!');

    } catch(e) {
        console.error('[VoiceDesc]', e);
        if (resultEl) resultEl.innerHTML = '<span style="color:#ff4444;">Failed to connect to Voice Engine.</span>';
        toast('Voice Engine error — is Joi running?');
    }
}

// =====================================================================
// ALWAYS-ON MIC  (wake-word: "hey joi" / "hi joi" / "hey joy")
// =====================================================================
// Debug helper — updates the small on-screen debug strip
function _micDbg(field, val) {
    const el = document.getElementById('mic-debug');
    if (!el) return;
    if (!_micDbg._d) _micDbg._d = {};
    _micDbg._d[field] = val;
    const d = _micDbg._d;
    el.textContent = 'E:' + (d.event||'-') + ' Err:' + (d.error||'-') + ' T:' + (d.transcript||'-').slice(0,60);
}

// Simple word-overlap similarity (0.0 to 1.0)
function _similarity(a, b) {
    const wa = new Set(a.split(/\s+/));
    const wb = new Set(b.split(/\s+/));
    let overlap = 0;
    wa.forEach(w => { if (wb.has(w)) overlap++; });
    return overlap / Math.max(wa.size, wb.size, 1);
}

function toggleMic() {
    if (micActive) { stopMic(); } else { startMic(); }
}

function startMic() {
    // If server STT is enabled, use MediaRecorder → /voice/transcribe instead
    if (useServerSTT) {
        micActive = true;
        document.getElementById('mic-btn').classList.add('active');
        document.getElementById('mic-status').classList.add('listening');
        document.getElementById('mic-label').textContent = 'server STT';
        startServerSTT();
        return;
    }

    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { toast('Speech recognition not supported'); return; }

    // Create ONE persistent recognition object
    if (!recognition) {
        recognition = new SR();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            _micDbg('event', 'started');
            console.log('[MIC] onstart');
            document.getElementById('mic-btn').classList.add('active');
            document.getElementById('mic-status').classList.add('listening');
            document.getElementById('mic-label').textContent = 'listening';
        };

        recognition.onaudiostart = () => {
            _micDbg('event', 'audio');
            console.log('[MIC] onaudiostart');
            document.getElementById('mic-label').textContent = 'hearing...';
        };

        recognition.onspeechstart = () => {
            _micDbg('event', 'speech');
            console.log('[MIC] onspeechstart');
            document.getElementById('mic-label').textContent = 'hearing...';
        };

        recognition.onresult = (e) => {
            // Guard: ignore results while Joi is speaking (prevents feedback loop)
            if (ttsActive) {
                _micDbg('event', 'ignored-tts-active');
                console.log('[MIC] ignored result — TTS active');
                return;
            }

            let interim = '', final = '';
            for (let i = e.resultIndex; i < e.results.length; i++) {
                const t = e.results[i][0].transcript;
                if (e.results[i].isFinal) final += t;
                else interim += t;
            }

            const raw = (final || interim).trim();
            _micDbg('transcript', raw);
            console.log('[MIC] result:', JSON.stringify({final, interim}));

            if (!final) return; // wait for final transcript

            // Similarity guard: discard if transcript matches Joi's last reply >70%
            const lower = final.trim().toLowerCase();
            const clean = lower.replace(/[^a-z0-9 ]/g, '').trim();
            if (lastJoiReply && clean.length > 5 && _similarity(clean, lastJoiReply) > 0.7) {
                _micDbg('event', 'echo-discarded');
                console.log('[MIC] discarded echo of Joi reply');
                return;
            }

            // Wake-word detection (fuzzy: joi/joy/joe/joey)
            const wakeRe = /\b(hey|hi|hay)\s*(joi|joy|joe|joey)\b/i;
            if (wakeRe.test(lower)) {
                const after = lower.replace(wakeRe, '').trim();
                if (after.length > 2) {
                    document.getElementById('message-input').value = after;
                    sendMessage();
                    _micDbg('event', 'sent: ' + after.slice(0,30));
                } else {
                    document.getElementById('message-input').focus();
                    toast('Listening...');
                    _micDbg('event', 'wake-only');
                }
                return;
            }

            // No wake word — auto-send the transcript (mic is explicitly on)
            const input = document.getElementById('message-input');
            const txt = final.trim();
            if (txt.length > 1) {
                input.value = txt;
                sendMessage();
                _micDbg('event', 'auto-sent: ' + txt.slice(0,30));
            }
        };

        recognition.onerror = (ev) => {
            const code = ev.error || 'unknown';
            _micDbg('error', code);
            console.warn('[MIC] onerror:', code);
            // no-speech and aborted are recoverable; onend will restart
            if (code !== 'no-speech' && code !== 'aborted') {
                document.getElementById('mic-label').textContent = 'err: ' + code;
            }
        };

        recognition.onend = () => {
            _micDbg('event', 'ended');
            console.log('[MIC] onend, micActive=', micActive, 'ttsActive=', ttsActive);
            // If TTS is playing, don't restart — _resumeMicAfterTTS() handles it
            if (ttsActive) {
                document.getElementById('mic-label').textContent = 'Joi speaking...';
                return;
            }
            if (micActive) {
                document.getElementById('mic-label').textContent = 'restarting...';
                setTimeout(() => {
                    if (!micActive || ttsActive) return;
                    try {
                        recognition.start();
                        console.log('[MIC] restarted');
                    } catch (err) {
                        console.warn('[MIC] restart failed:', err);
                        _micDbg('error', 'restart:' + err.message);
                    }
                }, 300);
            } else {
                document.getElementById('mic-btn').classList.remove('active');
                document.getElementById('mic-status').classList.remove('listening');
                document.getElementById('mic-label').textContent = 'mic off';
            }
        };
    }

    // Start listening
    micActive = true;
    try {
        recognition.start();
    } catch (err) {
        // already started — stop and retry
        console.warn('[MIC] start failed, retrying:', err);
        try { recognition.stop(); } catch(_){}
        setTimeout(() => { if (micActive) { try { recognition.start(); } catch(_){} } }, 300);
    }
    document.getElementById('mic-btn').classList.add('active');
    document.getElementById('mic-status').classList.add('listening');
    document.getElementById('mic-label').textContent = 'starting...';
    _micDbg('event', 'init');
    _micDbg('error', '-');
    _micDbg('transcript', '-');
}

function stopMic() {
    micActive = false;
    if (recognition) { try { recognition.stop(); } catch(e){} }
    stopServerSTT();
    // don't null recognition — reuse the same object
    document.getElementById('mic-btn').classList.remove('active');
    document.getElementById('mic-status').classList.remove('listening');
    document.getElementById('mic-label').textContent = 'mic off';
    _micDbg('event', 'stopped');
}

// =====================================================================
// SERVER-SIDE STT (Whisper + Speaker ID)
// =====================================================================

async function loadServerSTTStatus() {
    try {
        const res = await fetch('/voice/status');
        if (res.ok) {
            const data = await res.json();
            useServerSTT = data.enrolled || false;
            const cb = document.getElementById('cb-server-stt');
            if (cb) cb.checked = useServerSTT;
            const status = document.getElementById('voice-enroll-status');
            if (status) status.textContent = data.enrolled ? `Enrolled: ${data.profile_name || 'user'}` : 'Not enrolled';
        }
    } catch (e) {
        console.log('[STT] Server STT not available:', e.message);
    }
}

function toggleServerSTT() {
    const cb = document.getElementById('cb-server-stt');
    useServerSTT = cb ? cb.checked : false;
    console.log('[STT] Server STT:', useServerSTT ? 'ON' : 'OFF');
    if (useServerSTT && micActive) {
        // Switch from browser STT to server STT
        if (recognition) { try { recognition.stop(); } catch(e){} }
        startServerSTT();
    } else if (!useServerSTT && micActive) {
        stopServerSTT();
        // Restart browser STT
        if (recognition) { try { recognition.start(); } catch(e){} }
    }
}

async function startServerSTT() {
    if (_sttMediaRecorder && _sttMediaRecorder.state !== 'inactive') return;
    try {
        _sttStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        _sttMediaRecorder = new MediaRecorder(_sttStream, { mimeType: 'audio/webm;codecs=opus' });
        let chunks = [];

        _sttMediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) chunks.push(e.data);
        };

        _sttMediaRecorder.onstop = async () => {
            if (chunks.length === 0) return;
            const blob = new Blob(chunks, { type: 'audio/webm' });
            chunks = [];

            // Convert to base64
            const reader = new FileReader();
            reader.onloadend = async () => {
                const b64 = reader.result.split(',')[1];
                try {
                    const res = await fetch('/voice/transcribe', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ audio_b64: b64 })
                    });
                    if (res.ok) {
                        const data = await res.json();
                        if (data.speaker_match && data.text && data.text.trim().length > 1) {
                            console.log('[STT] Server transcript:', data.text, 'confidence:', data.confidence);
                            // Check for wake word
                            const lower = data.text.toLowerCase();
                            const wakeRe = /\b(hey|hi|hay)\s*(joi|joy|joe|joey)\b/i;
                            const txt = wakeRe.test(lower) ? lower.replace(wakeRe, '').trim() : data.text.trim();
                            if (txt.length > 1) {
                                document.getElementById('message-input').value = txt;
                                sendMessage();
                            }
                        } else if (!data.speaker_match) {
                            console.log('[STT] Speaker not matched, confidence:', data.confidence);
                        }
                    }
                } catch (err) {
                    console.warn('[STT] Transcribe error:', err);
                }
            };
            reader.readAsDataURL(blob);
        };

        // Record in 4-second chunks
        _sttMediaRecorder.start();
        _sttChunkTimer = setInterval(() => {
            if (!micActive || !useServerSTT || ttsActive) return;
            if (_sttMediaRecorder && _sttMediaRecorder.state === 'recording') {
                _sttMediaRecorder.stop();
                setTimeout(() => {
                    if (micActive && useServerSTT && !ttsActive) {
                        try { _sttMediaRecorder.start(); } catch(e){}
                    }
                }, 100);
            }
        }, 4000);

        console.log('[STT] Server STT started');
    } catch (e) {
        console.warn('[STT] Failed to start server STT:', e);
        toast('Server STT failed — check mic permissions');
    }
}

function stopServerSTT() {
    if (_sttChunkTimer) { clearInterval(_sttChunkTimer); _sttChunkTimer = null; }
    if (_sttMediaRecorder && _sttMediaRecorder.state !== 'inactive') {
        try { _sttMediaRecorder.stop(); } catch(e){}
    }
    if (_sttStream) {
        _sttStream.getTracks().forEach(t => t.stop());
        _sttStream = null;
    }
    _sttMediaRecorder = null;
    console.log('[STT] Server STT stopped');
}

// =====================================================================
// VOICE ENROLLMENT
// =====================================================================

async function startVoiceEnrollment() {
    const status = document.getElementById('voice-enroll-status');
    const btn = document.getElementById('btn-enroll-voice');
    if (!status || !btn) return;

    try {
        btn.disabled = true;
        status.textContent = 'Recording 15 seconds...';
        status.style.color = '#ff9900';

        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm;codecs=opus' });
        let chunks = [];

        recorder.ondataavailable = (e) => { if (e.data.size > 0) chunks.push(e.data); };

        recorder.onstop = async () => {
            stream.getTracks().forEach(t => t.stop());
            status.textContent = 'Processing...';

            const blob = new Blob(chunks, { type: 'audio/webm' });
            const reader = new FileReader();
            reader.onloadend = async () => {
                const b64 = reader.result.split(',')[1];
                try {
                    const res = await fetch('/voice/enroll', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ audio_b64: b64 })
                    });
                    const data = await res.json();
                    if (data.ok) {
                        status.textContent = 'Voice enrolled!';
                        status.style.color = '#00ff88';
                        useServerSTT = true;
                        const cb = document.getElementById('cb-server-stt');
                        if (cb) cb.checked = true;
                    } else {
                        status.textContent = data.error || 'Enrollment failed';
                        status.style.color = '#ff4444';
                    }
                } catch (e) {
                    status.textContent = 'Server error: ' + e.message;
                    status.style.color = '#ff4444';
                }
                btn.disabled = false;
            };
            reader.readAsDataURL(blob);
        };

        // Countdown timer
        recorder.start();
        let remaining = 15;
        const countdown = setInterval(() => {
            remaining--;
            if (remaining > 0) {
                status.textContent = `Recording... ${remaining}s remaining`;
            } else {
                clearInterval(countdown);
            }
        }, 1000);

        setTimeout(() => {
            if (recorder.state === 'recording') recorder.stop();
            clearInterval(countdown);
        }, 15000);

    } catch (e) {
        status.textContent = 'Mic error: ' + e.message;
        status.style.color = '#ff4444';
        btn.disabled = false;
    }
}

// =====================================================================
// FACE ENROLLMENT
// =====================================================================

async function startFaceEnrollment() {
    const status = document.getElementById('face-enroll-status');
    const btn = document.getElementById('btn-enroll-face');
    if (!status || !btn) return;

    const name = prompt('Enter the name for this person:');
    if (!name || !name.trim()) return;

    status.textContent = 'Starting enrollment...';
    status.style.color = '#ff9900';
    btn.disabled = true;

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: `[SYSTEM] Enroll face for ${name.trim()}` })
        });
        // The actual enrollment happens via the enroll_face tool call in the backend
        // Just trigger it via chat and show progress
        status.textContent = `Enrolling ${name.trim()} — capturing 5 frames over 10 seconds...`;

        // Poll camera status for enrollment progress
        let checks = 0;
        const pollEnroll = setInterval(async () => {
            checks++;
            try {
                const camRes = await fetch('/camera/status');
                const camData = await camRes.json();
                if (!camData.enrollment_active) {
                    clearInterval(pollEnroll);
                    status.textContent = `${name.trim()} enrolled!`;
                    status.style.color = '#00ff88';
                    btn.disabled = false;
                }
            } catch (e) {}
            if (checks > 30) { // 30 seconds timeout
                clearInterval(pollEnroll);
                status.textContent = 'Enrollment timed out';
                status.style.color = '#ff4444';
                btn.disabled = false;
            }
        }, 1000);

    } catch (e) {
        status.textContent = 'Error: ' + e.message;
        status.style.color = '#ff4444';
        btn.disabled = false;
    }
}

async function listKnownFaces() {
    const container = document.getElementById('known-faces-list');
    if (!container) return;
    container.textContent = 'Loading...';
    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: '[SYSTEM] List known faces' })
        });
        const data = await res.json();
        // Also try direct camera status
        const camRes = await fetch('/camera/status');
        const camData = await camRes.json();
        if (camData.known_people && camData.known_people.length > 0) {
            container.innerHTML = camData.known_people.map(name =>
                `<span style="display:inline-block;padding:2px 8px;margin:2px;border-radius:4px;background:rgba(190,147,255,0.15);border:1px solid rgba(190,147,255,0.3);">${name}</span>`
            ).join('');
        } else {
            container.textContent = 'No faces enrolled yet.';
        }
    } catch (e) {
        container.textContent = 'Error loading faces.';
    }
}

// =====================================================================
// CONTINUOUS VISION
// =====================================================================
let visionActive = false;
let visionPollTimer = null;

async function toggleVision() {
    if (visionActive) { await stopVision(); }
    else { await startVision(); }
}

async function startVision() {
    try {
        const r = await fetch('/vision/start', {method:'POST', headers:{'Content-Type':'application/json'}});
        const d = await r.json();
        if (d.ok) {
            visionActive = true;
            document.getElementById('vision-btn').classList.add('active');
            document.getElementById('vision-indicator').classList.add('on');
            addMessage('assistant', 'Vision activated — I can now see your entire desktop, all windows and tabs.');
            // Start polling for proactive observations
            visionPollTimer = setInterval(pollProactive, 6000);
        } else {
            addMessage('assistant', 'Vision error: ' + (d.error || 'unknown'));
        }
    } catch(e) { addMessage('assistant', 'Vision start failed: ' + e.message); }
}

async function stopVision() {
    try {
        await fetch('/vision/stop', {method:'POST', headers:{'Content-Type':'application/json'}});
    } catch(_) {}
    visionActive = false;
    document.getElementById('vision-btn').classList.remove('active');
    document.getElementById('vision-indicator').classList.remove('on');
    if (visionPollTimer) { clearInterval(visionPollTimer); visionPollTimer = null; }
    addMessage('assistant', 'Vision deactivated.');
}

async function pollProactive() {
    if (!visionActive) return;
    try {
        const r = await fetch('/vision/proactive');
        const d = await r.json();
        if (d.ok && d.messages && d.messages.length > 0) {
            for (const msg of d.messages) {
                addMessage('assistant', msg);
                speak(msg);
            }
        }
    } catch(_) {}
}

// =====================================================================
// WEBCAM CAMERA
// =====================================================================
let cameraActive = false;
let cameraStream = null;
let cameraCapTimer = null;
let cameraPollTimer = null;

async function toggleCamera() {
    if (cameraActive) { await stopCamera(); }
    else { await startCamera(); }
}

async function startCamera() {
    try {
        cameraStream = await navigator.mediaDevices.getUserMedia({video: true, audio: false});
    } catch(e) {
        const msg = e.name === 'NotAllowedError'
            ? 'Camera permission denied. Please allow camera access in your browser settings.'
            : 'Camera error: ' + e.message;
        addMessage('assistant', msg);
        return;
    }

    // Show preview
    const preview = document.getElementById('camera-preview');
    preview.srcObject = cameraStream;
    preview.classList.add('on');

    // Tell backend
    try {
        const r = await fetch('/camera/start', {method:'POST', headers:{'Content-Type':'application/json'}});
        const d = await r.json();
        if (!d.ok) { stopCamera(); addMessage('assistant', 'Camera backend error: ' + d.error); return; }
    } catch(e) { stopCamera(); addMessage('assistant', 'Camera start failed: ' + e.message); return; }

    cameraActive = true;
    document.getElementById('camera-btn').classList.add('active');
    document.getElementById('camera-indicator').classList.add('on');
    addMessage('assistant', 'Camera active — I can see you now, Lonnie!');

    // Capture frames every 2 seconds
    cameraCapTimer = setInterval(captureAndSendFrame, 2000);
    // Poll proactive observations every 6 seconds
    cameraPollTimer = setInterval(pollCameraProactive, 6000);
}

async function stopCamera() {
    cameraActive = false;
    if (cameraStream) {
        cameraStream.getTracks().forEach(t => t.stop());
        cameraStream = null;
    }
    const preview = document.getElementById('camera-preview');
    preview.srcObject = null;
    preview.classList.remove('on');
    document.getElementById('camera-btn').classList.remove('active');
    document.getElementById('camera-indicator').classList.remove('on');
    if (cameraCapTimer) { clearInterval(cameraCapTimer); cameraCapTimer = null; }
    if (cameraPollTimer) { clearInterval(cameraPollTimer); cameraPollTimer = null; }
    try { await fetch('/camera/stop', {method:'POST', headers:{'Content-Type':'application/json'}}); } catch(_){}
    addMessage('assistant', 'Camera off.');
}

function captureAndSendFrame() {
    if (!cameraActive || !cameraStream) return;
    const video = document.getElementById('camera-preview');
    if (!video.videoWidth) return; // not ready yet
    const canvas = document.createElement('canvas');
    canvas.width = Math.min(video.videoWidth, 640);
    canvas.height = Math.round(canvas.width * video.videoHeight / video.videoWidth);
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const b64 = canvas.toDataURL('image/jpeg', 0.7).split(',')[1];
    fetch('/camera/frame', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({image_b64: b64})
    }).catch(() => {});
}

async function pollCameraProactive() {
    if (!cameraActive) return;
    try {
        const r = await fetch('/camera/proactive');
        const d = await r.json();
        if (d.ok && d.messages && d.messages.length > 0) {
            for (const msg of d.messages) {
                addMessage('assistant', msg);
                speak(msg);
            }
        }
    } catch(_) {}
}

// =====================================================================
// AVATAR
// =====================================================================
async function loadAvatar() {
    const img = document.getElementById('avatar-image');
    const canvas = document.getElementById('avatar-canvas');

    // Default: embedded avatar image (no server round-trip)
    img.style.display = 'block';
    canvas.style.display = 'none';

    try {
        const r = await fetch('/avatar');
        const ct = (r.headers.get('content-type') || '').toLowerCase();
        if (!r.ok || !ct.includes('application/json')) return;

        const d = await r.json();
        if (d.ok && d.url) {
            img.src = d.url;
            img.style.display = 'block';
            canvas.style.display = 'none';
        }
        if (d.face && window.applyFaceCoords) window.applyFaceCoords(d.face);
    } catch (e) {
        // keep default
    }
}

async function loadAvatarSwitcher() {
    const container = document.getElementById('avatar-switcher');
    container.innerHTML = '';
    try {
        const r = await fetch('/avatars');
        const ct = (r.headers.get('content-type') || '').toLowerCase();
        if (!r.ok || !ct.includes('application/json')) return;

        const d = await r.json();
        if (d.ok && d.avatars) {
            d.avatars.forEach(a => {
                const img = document.createElement('img');
                img.className = 'avatar-thumb' + (a.is_current ? ' current' : '');
                img.src = a.url;
                img.title = a.name;
                img.onclick = () => switchAvatar(a.name);
                container.appendChild(img);
            });
        }
    } catch (e) { /* ignore */ }
}

async function switchAvatar(name) {
    try {
        const r = await fetch('/avatars/switch', {method:'POST', headers:{'Content-Type':'application/json'},
                                                   body: JSON.stringify({name})});
        const d = await r.json();
        if (d.ok) {
            if (d.face && window.applyFaceCoords) window.applyFaceCoords(d.face);
            toast('Switched to '+name); await loadAvatar(); await loadAvatarSwitcher();
        }
        else toast(d.error);
    } catch(e) { toast(e.message); }
}

// Particle avatar fallback
function initializeAvatar() {
    const canvas = document.getElementById('avatar-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width=220; canvas.height=220;
    particles = [];
    for (let i=0;i<50;i++) particles.push({
        x:Math.random()*220, y:Math.random()*220,
        vx:(Math.random()-.5)*2, vy:(Math.random()-.5)*2,
        size:Math.random()*3+1
    });
    (function animate(){
        ctx.fillStyle='rgba(0,0,0,0.1)';
        ctx.fillRect(0,0,220,220);
        particles.forEach(p=>{
            p.x+=p.vx; p.y+=p.vy;
            if(p.x<0||p.x>220) p.vx*=-1;
            if(p.y<0||p.y>220) p.vy*=-1;
            ctx.fillStyle='rgba(255,0,255,0.8)';
            ctx.beginPath(); ctx.arc(p.x,p.y,p.size,0,Math.PI*2); ctx.fill();
        });
        requestAnimationFrame(animate);
    })();
}

// =====================================================================
// MAIN SIDEBAR (Sidebar UX Contract)
// =====================================================================
function toggleSidebar() {
    const sb = document.getElementById('main-sidebar');
    const ov = document.getElementById('sidebar-overlay');
    const app = document.getElementById('app-container');
    const isOpen = sb.classList.contains('open');
    if (isOpen) {
        closeSidebar();
    } else {
        sb.classList.add('open');
        ov.classList.add('active');
        app.classList.add('sidebar-open');
        // Always scroll to top (Quick Status)
        document.getElementById('sidebar-scroll').scrollTop = 0;
        // Refresh status
        refreshSidebarStatus();
    }
}
function closeSidebar() {
    document.getElementById('main-sidebar').classList.remove('open');
    document.getElementById('sidebar-overlay').classList.remove('active');
    document.getElementById('app-container').classList.remove('sidebar-open');
}
function sbToggle(el) {
    el.classList.toggle('on');
}
async function sbTogglePrivate(el) {
    const goingOn = !el.classList.contains('on');
    try {
        const r = await fetch('/private-mode', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({enabled: goingOn})});
        const d = await r.json();
        if (d.ok) {
            el.classList.toggle('on', d.enabled);
            const modelEl = document.getElementById('sb-model');
            if (d.enabled) {
                modelEl.innerHTML = '<span class="sb-dot" style="background:#ff69b4"></span>Private (Local)';
            } else {
                modelEl.innerHTML = '<span class="sb-dot green"></span>gpt-4o';
            }
        }
    } catch(e) { console.warn('Private mode toggle failed', e); }
}
function enablePaidUsage() {
    document.getElementById('sb-paid-meter').style.display = 'block';
    document.getElementById('sb-budget-banner').classList.remove('visible');
}
function stayLocal() {
    document.getElementById('sb-budget-banner').classList.remove('visible');
}
function sidebarNav(target) {
    closeSidebar();
    switch(target) {
        case 'projects':      toggleProjects(); break;
        case 'history':       toggleHistory(); break;
        case 'proposals':     showProposals(); break;
        case 'research':      showResearch(); break;
        case 'memory':        showMemory(); break;
        case 'diagnostics':   showDiagnostics(); break;
        case 'brain-map':     toggleBrainDock(); break;
        case 'terminal':      toggleTerminalDock(); break;
        case 'settings':      showSettings(); break;
        case 'logout':        logout(); break;
        case 'voice-creator': openVoiceCreator(); break;
        case 'avatar-studio':
            window.open('/avatar_studio', '_blank');
            break;
    }
}
async function refreshSidebarStatus() {
    // Try to get current model/mode from diagnostics manifest
    try {
        const r = await fetch('/diagnostics/manifest');
        if (r.ok) {
            const d = await r.json();
            if (d.model) {
                document.getElementById('sb-model').innerHTML =
                    '<span class="sb-dot green"></span>' + (d.model || 'gpt-4o');
            }
            if (d.provider) {
                const cloudLabel = d.provider === 'local' ? 'Local-only' : 'Paid-cap';
                document.getElementById('sb-cloud').innerHTML =
                    '<span class="sb-dot green"></span>' + cloudLabel;
            }
        }
    } catch(e) { /* silent */ }
    // Refresh private mode state
    try {
        const pr = await fetch('/private-mode');
        if (pr.ok) {
            const pd = await pr.json();
            const privToggle = document.getElementById('sb-tog-private');
            if (privToggle) privToggle.classList.toggle('on', pd.enabled);
            if (pd.enabled) {
                document.getElementById('sb-model').innerHTML = '<span class="sb-dot" style="background:#ff69b4"></span>Private (Local)';
            }
        }
    } catch(e) { /* silent */ }
    // Refresh avatar thumb
    try {
        const img = document.getElementById('sb-avatar-img');
        const mainAvatar = document.querySelector('#avatar-visual img');
        if (mainAvatar && mainAvatar.src) {
            img.src = mainAvatar.src;
            img.style.display = 'block';
        }
    } catch(e) { /* silent */ }
}

// =====================================================================
// FILE BROWSER SIDEBAR
// =====================================================================
let _fsCurrentRoot = 'project';
let _fsCurrentDir = '';

function toggleProjects() {
    const sidebar = document.getElementById('projects-sidebar');
    sidebar.classList.toggle('open');
}

function _fsFormatSize(bytes) {
    if (bytes === 0) return '';
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes/1024).toFixed(1) + ' KB';
    return (bytes/1048576).toFixed(1) + ' MB';
}

function _fsGetIcon(name, isDir) {
    if (isDir) return '📁';
    const ext = name.split('.').pop().toLowerCase();
    const icons = {
        py:'🐍', js:'📜', html:'🌐', css:'🎨', json:'📋',
        md:'📝', txt:'📄', pdf:'📕', csv:'📊',
        png:'🖼', jpg:'🖼', jpeg:'🖼', gif:'🖼', webp:'🖼', svg:'🖼',
        mp3:'🎵', wav:'🎵', mp4:'🎬', mkv:'🎬',
        zip:'📦', rar:'📦', exe:'⚙', bat:'⚙', sh:'⚙',
    };
    return icons[ext] || '📄';
}

function _fsUpdateBreadcrumb() {
    const bc = document.getElementById('fs-breadcrumb');
    const parts = _fsCurrentDir ? _fsCurrentDir.split(/[/\\]/).filter(Boolean) : [];
    let html = `<span onclick="fsBrowse('${_fsCurrentRoot}','')">${_fsCurrentRoot}</span>`;
    let path = '';
    for (const part of parts) {
        path += (path ? '/' : '') + part;
        const safePath = path.replace(/'/g, "\\'");
        html += `<span class="sep">/</span><span onclick="fsBrowse('${_fsCurrentRoot}','${safePath}')">${part}</span>`;
    }
    bc.innerHTML = html;
}

async function fsBrowse(root, dir) {
    _fsCurrentRoot = root;
    _fsCurrentDir = dir;
    document.getElementById('fs-root-select').value = root;
    _fsUpdateBreadcrumb();

    const list = document.getElementById('projects-list');
    list.innerHTML = '<p style="font-size:12px;color:rgba(255,255,255,0.4);padding:10px">Loading...</p>';

    try {
        const params = new URLSearchParams({root, dir});
        const r = await fetch('/fs/browse?' + params);
        const d = await r.json();
        list.innerHTML = '';

        if (!d.ok) {
            list.innerHTML = `<p style="font-size:12px;color:#ff6b6b;padding:10px">${d.error}</p>`;
            return;
        }

        // Parent directory link
        if (dir) {
            const parentDir = dir.replace(/[/\\][^/\\]*$/, '');
            const parentEl = document.createElement('div');
            parentEl.className = 'fs-item dir';
            parentEl.innerHTML = `<span class="fs-icon">⬆</span><span class="fs-name">..</span>`;
            parentEl.onclick = () => fsBrowse(root, parentDir);
            list.appendChild(parentEl);
        }

        // Sort: directories first, then files, both alphabetical
        const items = d.items || [];
        const dirs = items.filter(i => i.type === 'dir').sort((a,b) => a.name.localeCompare(b.name));
        const files = items.filter(i => i.type === 'file').sort((a,b) => a.name.localeCompare(b.name));

        for (const item of [...dirs, ...files]) {
            const el = document.createElement('div');
            const isDir = item.type === 'dir';
            el.className = 'fs-item' + (isDir ? ' dir' : '');
            const icon = _fsGetIcon(item.name, isDir);
            const size = isDir ? '' : _fsFormatSize(item.size);
            el.innerHTML = `<span class="fs-icon">${icon}</span><span class="fs-name">${item.name}</span><span class="fs-size">${size}</span>`;

            if (isDir) {
                el.onclick = () => fsBrowse(root, item.path);
            } else {
                el.onclick = () => openFileViewer(root, item.path, item.name);
            }
            list.appendChild(el);
        }

        if (items.length === 0) {
            list.innerHTML = '<p style="font-size:12px;color:rgba(255,255,255,0.4);padding:10px">Empty folder</p>';
        }

        if (d.truncated) {
            const note = document.createElement('p');
            note.style.cssText = 'font-size:11px;color:rgba(255,255,255,0.3);padding:6px 8px;text-align:center';
            note.textContent = `Showing first ${items.length} items...`;
            list.appendChild(note);
        }
    } catch(e) {
        list.innerHTML = `<p style="font-size:12px;color:#ff6b6b;padding:10px">Error: ${e.message}</p>`;
    }
}

async function openFileViewer(root, path, name) {
    const overlay = document.getElementById('file-viewer-overlay');
    const title = document.getElementById('file-viewer-title');
    const body = document.getElementById('file-viewer-body');
    const dlLink = document.getElementById('file-viewer-download');

    title.textContent = name;
    body.innerHTML = '<p style="color:rgba(255,255,255,0.4)">Loading...</p>';
    dlLink.href = `/file/${root}/${path}`;
    dlLink.download = name;
    overlay.classList.add('open');

    try {
        const r = await fetch('/fs/read', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({root, path})
        });
        const d = await r.json();

        if (!d.ok) {
            body.innerHTML = `<p style="color:#ff6b6b">${d.error}</p>
                <p style="margin-top:10px"><a href="/file/${root}/${path}" download="${name}" style="color:var(--secondary)">Download file instead</a></p>`;
            return;
        }

        if (d.type === 'text') {
            const escaped = d.text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
            body.innerHTML = `<pre>${escaped}</pre>`;
        } else if (d.type === 'pdf') {
            const escaped = d.text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
            body.innerHTML = `<p style="color:var(--secondary);margin-bottom:8px">PDF — ${d.pages} pages</p><pre>${escaped}</pre>`;
        } else if (d.type === 'image') {
            body.innerHTML = `<img src="${d.data}" alt="${name}">`;
        } else {
            body.innerHTML = `<p style="color:rgba(255,255,255,0.5)">Preview not available for this file type.</p>
                <p style="margin-top:10px"><a href="/file/${root}/${path}" download="${name}" style="color:var(--secondary)">Download file</a></p>`;
        }
    } catch(e) {
        body.innerHTML = `<p style="color:#ff6b6b">Error loading file: ${e.message}</p>`;
    }
}

function closeFileViewer() {
    document.getElementById('file-viewer-overlay').classList.remove('open');
    document.getElementById('file-viewer-body').innerHTML = '';
}

async function loadProjects() {
    // Load file browser starting at project root
    await fsBrowse('project', '');
}

async function scanProjects() {
    toast('Scanning your files…');
    try {
        const r1 = await fetch('/projects/scan', {method:'POST', headers:{'Content-Type':'application/json'},
                                                   body: JSON.stringify({roots:["documents","desktop","downloads","home"]})});
        const scan = await r1.json();
        if (!scan.ok) { toast(scan.error); return; }
        toast(scan.summary);

        const r2 = await fetch('/projects/organise', {method:'POST', headers:{'Content-Type':'application/json'},
                                                       body: JSON.stringify({categories: scan.categories})});
        const org = await r2.json();
        toast(org.message || 'Done!');

        await fsBrowse(_fsCurrentRoot, _fsCurrentDir);
    } catch(e) { toast(e.message); }
}

// =====================================================================
// HISTORY SIDEBAR
// =====================================================================
function toggleHistory() {
    const sidebar = document.getElementById('history-sidebar');
    sidebar.classList.toggle('open');
}

async function loadHistory() {
    try {
        const r = await fetch('/history?limit=80');
        const d = await r.json();
        const list = document.getElementById('history-list');
        list.innerHTML = '';
        if (d.ok && d.history) {
            d.history.forEach(h => {
                appendHistoryItem(h, list);
            });
            list.scrollTop = list.scrollHeight;
        }
    } catch(e) {}
}

function appendHistoryItem(h, container=null) {
    if (!container) container = document.getElementById('history-list');
    const div = document.createElement('div');
    const isUser = h.role === 'user';
    div.className = 'history-item ' + (isUser ? 'user-msg' : 'joi-msg');
    const timeStr = h.ts ? new Date(h.ts).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'}) : '';
    div.innerHTML = `<span class="hist-time">${isUser?'You':'Joi'} ${timeStr}</span><br>${(h.content||'').slice(0,120)}`;
    div.onclick = () => {
        // scroll to or highlight — for now just show in input
        if (isUser) document.getElementById('message-input').value = h.content||'';
    };
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

// =====================================================================
// VOICE / SETTINGS
// =====================================================================
function loadVoices() {
    const select = document.getElementById('voice-select');
    const voices = window.speechSynthesis.getVoices();
    select.innerHTML = '<option value="">Default</option>';
    voices.forEach(v => {
        const o = document.createElement('option');
        o.value = v.name; o.textContent = `${v.name} (${v.lang})`;
        select.appendChild(o);
    });
    const fem = voices.find(v => v.name.includes('Female')||v.name.includes('Samantha')||v.name.includes('Zira'));
    if (fem) { selectedVoice=fem; select.value=fem.name; }
}
function updateVoice() {
    const voices = window.speechSynthesis.getVoices();
    selectedVoice = voices.find(v => v.name === document.getElementById('voice-select').value);
}
function testVoice() { isSpeaking=false; speak("Hello, Lonnie. This is how I sound."); }

// =====================================================================
// IMAGE UPLOAD
// =====================================================================
function handleImageUpload(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = e => { currentImage = e.target.result; toast('Image attached'); };
        reader.readAsDataURL(input.files[0]);
    }
}

// =====================================================================
// BACKGROUND
// =====================================================================
function setBgImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = e => {
            document.documentElement.style.setProperty('--bg-image', `url(${e.target.result})`);
            localStorage.setItem('joi-bg-image', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}
function setBgColor(color) {
    document.documentElement.style.setProperty('--bg', color);
    localStorage.setItem('joi-bg-color', color);
}

// =====================================================================
// MODALS
// =====================================================================
function showSettings()  { document.getElementById('settings-modal').classList.add('active'); loadMode(); loadCommentary(); }
function closeModal(id)  {
    document.getElementById(id).classList.remove('active');
    // Stop brain poll if closing the brain modal and dock is also closed
    if (id === 'brain-map-modal' && !_brainDockOpen && _brainPollId) {
        clearInterval(_brainPollId); _brainPollId = null;
    }
}

// =====================================================================
// MODE SYSTEM
// =====================================================================
let currentMode = 'full';
const MODE_DESCS = {
    companion: 'Warm casual chat — quick, personal, girlfriend energy',
    work: 'Task-focused — efficient, collaborative, minimal fluff',
    creative: 'Expressive & imaginative — metaphors, poetry, big ideas',
    precision: 'Exact & technical — factual, concise, no embellishment',
    full: 'Adaptive — auto-detects reply length from your message',
};

async function loadMode() {
    try {
        const r = await fetch('/mode'); const d = await r.json();
        if (d.ok) { currentMode = d.mode; _updateModeUI(); }
    } catch(e) {}
}

async function setJoiMode(name) {
    try {
        const r = await fetch('/mode', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({mode:name})});
        const d = await r.json();
        if (d.ok) { currentMode = d.mode; _updateModeUI(); toast('Mode: ' + d.mode); }
        else toast(d.error || 'Failed');
    } catch(e) { toast('Mode switch failed'); }
}

function _updateModeUI() {
    const badge = document.getElementById('mode-badge');
    if (badge) badge.textContent = 'mode: ' + currentMode;
    const desc = document.getElementById('mode-desc');
    if (desc) desc.textContent = MODE_DESCS[currentMode] || '';
    document.querySelectorAll('.mode-opt').forEach(b => {
        if (b.dataset.mode === currentMode) {
            b.style.borderColor = 'var(--accent)';
            b.style.background = 'rgba(157,0,255,0.2)';
        } else {
            b.style.borderColor = '#555';
            b.style.background = 'transparent';
        }
    });
}

// =====================================================================
// COMMENTARY CONTROLS
// =====================================================================
async function loadCommentary() {
    try {
        const r = await fetch('/commentary'); const d = await r.json();
        if (d.ok && d.settings) {
            const s = d.settings;
            const vc = document.getElementById('cb-vision-commentary');
            const cc = document.getElementById('cb-camera-commentary');
            if (vc) vc.checked = s.vision_commentary;
            if (cc) cc.checked = s.camera_commentary;
            const vs = document.getElementById('vision-interval-slider');
            const cs = document.getElementById('camera-interval-slider');
            if (vs) { vs.value = s.vision_min_interval; document.getElementById('vision-interval-val').textContent = s.vision_min_interval; }
            if (cs) { cs.value = s.camera_min_interval; document.getElementById('camera-interval-val').textContent = s.camera_min_interval; }
            window.isMuted = !!s.global_mute;
            const muteBtn = document.getElementById('mute-all-btn');
            if (muteBtn) {
                muteBtn.textContent = window.isMuted ? 'MUTED' : 'Mute All';
                muteBtn.classList.toggle('muted', window.isMuted);
                muteBtn.style.background = window.isMuted ? 'rgba(255,68,68,0.4)' : 'rgba(255,68,68,0.1)';
            }
        }
    } catch(e) {}
}

async function updateCommentary() {
    const vc = document.getElementById('cb-vision-commentary');
    const cc = document.getElementById('cb-camera-commentary');
    const vs = document.getElementById('vision-interval-slider');
    const cs = document.getElementById('camera-interval-slider');
    const body = {
        vision_commentary: vc ? vc.checked : true,
        camera_commentary: cc ? cc.checked : true,
        vision_min_interval: vs ? parseInt(vs.value) : 45,
        camera_min_interval: cs ? parseInt(cs.value) : 30,
    };
    try {
        await fetch('/commentary', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
    } catch(e) {}
}

async function muteAll() {
    try {
        const newState = !window.isMuted;
        await fetch('/commentary', {method:'POST', headers:{'Content-Type':'application/json'},
            body:JSON.stringify({global_mute: newState})});
        window.isMuted = newState;
        const btn = document.getElementById('mute-all-btn');
        if (btn) {
            btn.textContent = newState ? 'MUTED' : 'Mute All';
            btn.classList.toggle('muted', newState);
            btn.style.background = newState ? 'rgba(255,68,68,0.4)' : 'rgba(255,68,68,0.1)';
        }
        toast(newState ? 'All commentary muted' : 'Commentary unmuted');
    } catch(e) {}
}

// =====================================================================
// DIAGNOSTICS
// =====================================================================
// ═══════════════════════════════════════════════════════════════
// BRAIN MAP v3 / NEURAL HUD — Ultron-Style Dense Neural Web
// ═══════════════════════════════════════════════════════════════
let _lastBrainState = null;
let _brainDockOpen = false;
let _processingPollId = null;
let _brainPollId = null;  // periodic brain state polling
let _brainParticles = [];
let _brainAnimFrame = null;
let _brainCanvasCtx = null;

// ── Node positions (match SVG viewBox 340x340 for dock) ──
const BRAIN_NODES = {
    IDENTITY:     {x:170, y:52,  color:'#ff00ff'},
    REASONING:    {x:95,  y:85,  color:'#00ffcc'},
    LANGUAGE:     {x:72,  y:155, color:'#32c850'},
    CREATIVITY:   {x:88,  y:215, color:'#cc44ff'},
    LONG_MEMORY:  {x:238, y:95,  color:'#3c64ff'},
    SHORT_MEMORY: {x:175, y:130, color:'#64b4ff'},
    FACTS:        {x:210, y:148, color:'#4488ff'},
    LEARNING:     {x:250, y:160, color:'#22ddaa'},
    VISION:       {x:260, y:210, color:'#ffdc32'},
    CAMERA:       {x:245, y:248, color:'#ffaa22'},
    VOICE:        {x:60,  y:248, color:'#dd66ff'},
    WEB:          {x:278, y:130, color:'#44ccff'},
    TOOLS:        {x:145, y:195, color:'#ff6644'},
    FILES:        {x:100, y:258, color:'#88cc44'},
    DESKTOP:      {x:168, y:260, color:'#ffaa44'},
    REPAIR:       {x:200, y:275, color:'#ffa032'},
    EMPATHY:      {x:150, y:145, color:'#ff88cc'},
    // Agent Worker Sectors (orchestration pipeline)
    ORCHESTRATOR: {x:32,  y:88,  color:'#ff00aa'},
    ARCHITECT:    {x:30,  y:130, color:'#5588ff'},
    CODER:        {x:32,  y:170, color:'#44ff88'},
    VALIDATOR:    {x:55,  y:200, color:'#ffaa00'},
};

// ── LLM Orbital positions (5 groups) ──
const LLM_BEAMS = {
    'openai':       { node:'llm-openai',       from:{x:170,y:165}, to:{x:320,y:48},  color:'#10a37f' },
    'gemini-high':  { node:'llm-gemini-high',  from:{x:170,y:165}, to:{x:20,y:48},   color:'#4285f4' },
    'gemini-fast':  { node:'llm-gemini-fast',  from:{x:170,y:165}, to:{x:20,y:300},  color:'#34a853' },
    'gemini-lite':  { node:'llm-gemini-lite',  from:{x:170,y:165}, to:{x:320,y:300}, color:'#fbbc05' },
    'local':        { node:'llm-local',        from:{x:170,y:165}, to:{x:170,y:335}, color:'#ff6600' },
};

// ── Map any model string to orbital key (actual models: gpt-4o, gpt-4o-mini, o3, gemini-1.5-flash, gemini-2.5-flash, etc.) ──
function getOrbitalKey(model) {
    if (!model) return null;
    const m = String(model).toLowerCase();
    if (m.includes('o3') || m.includes('gpt')) return 'openai';
    if (m.includes('gemini-3-pro') || m.includes('2.5-pro') || m.includes('gemini-pro')) return 'gemini-high';
    if (m.includes('flash') || m.includes('2-pro-exp') || m.includes('gemini-3-flash') || m.includes('1.5-flash') || m.includes('2.5-flash')) return 'gemini-fast';
    if (m.includes('lite') || m.includes('gemma')) return 'gemini-lite';
    if (m.includes('mistral') || m.includes('local')) return 'local';
    return null;
}

// Default orbital label per key (when idle); active orbital shows actual display_name from /neuro
const LLM_ORBITAL_DEFAULT_LABELS = { 'openai': 'GPT', 'gemini-high': 'G-PRO', 'gemini-fast': 'G-FAST', 'gemini-lite': 'G-LITE', 'local': 'LOCAL' };
const LLM_ORBITAL_MODAL_DEFAULT_LABELS = { 'openai': 'GPT-4o', 'gemini-high': 'Gemini Pro', 'gemini-fast': 'Gemini Flash', 'gemini-lite': 'Gemini Lite', 'local': 'Local' };

// ── Neural connection rules (35 connections — Ultron density) ──
const BRAIN_CONNECTIONS = [
    // Core cognition chain
    ['IDENTITY','REASONING'], ['REASONING','LANGUAGE'], ['LANGUAGE','CREATIVITY'],
    ['IDENTITY','EMPATHY'], ['EMPATHY','LANGUAGE'], ['REASONING','TOOLS'],
    // Memory network
    ['LONG_MEMORY','SHORT_MEMORY'], ['SHORT_MEMORY','FACTS'], ['FACTS','LONG_MEMORY'],
    ['LONG_MEMORY','LEARNING'], ['LEARNING','REASONING'],
    // Sensory paths
    ['VISION','REASONING'], ['CAMERA','VISION'], ['VISION','LONG_MEMORY'],
    ['CAMERA','EMPATHY'],
    // IO paths
    ['WEB','REASONING'], ['WEB','LONG_MEMORY'], ['VOICE','LANGUAGE'],
    ['VOICE','EMPATHY'],
    // Action paths
    ['TOOLS','FILES'], ['TOOLS','DESKTOP'], ['TOOLS','WEB'],
    ['REASONING','REPAIR'], ['REPAIR','TOOLS'],
    // Cross-brain bridges
    ['IDENTITY','LONG_MEMORY'], ['EMPATHY','CREATIVITY'],
    ['LEARNING','REPAIR'], ['CREATIVITY','VOICE'],
    ['FACTS','LANGUAGE'], ['DESKTOP','VISION'],
    ['FILES','LONG_MEMORY'], ['SHORT_MEMORY','REASONING'],
    // Deep connections
    ['IDENTITY','CREATIVITY'], ['EMPATHY','LEARNING'],
    ['REPAIR','IDENTITY'],
    // Agent worker connections (orchestration pipeline)
    ['ORCHESTRATOR','REASONING'], ['ORCHESTRATOR','ARCHITECT'],
    ['ARCHITECT','CODER'], ['CODER','VALIDATOR'],
    ['VALIDATOR','REPAIR'], ['ORCHESTRATOR','TOOLS'],
    ['CODER','FILES'], ['ARCHITECT','LONG_MEMORY'],
];

// ── Dock toggle ──
function toggleBrainDock() {
    const dock = document.getElementById('brain-dock');
    if (!dock) return;
    _brainDockOpen = !_brainDockOpen;
    dock.classList.toggle('open', _brainDockOpen);
    if (_brainDockOpen) {
        initBrainCanvas();
        loadBrainState();
        _dockReviewLoaded = false; // refresh provider state on dock open
        // Real-time polling so neurons, gauges, and loadout update live (1.5s)
        if (!_brainPollId) {
            _brainPollId = setInterval(loadBrainState, 1500);
        }
    } else {
        stopBrainAnimation();
        if (_brainPollId) { clearInterval(_brainPollId); _brainPollId = null; }
    }
}
function closeBrainDock() {
    const dock = document.getElementById('brain-dock');
    if (dock) dock.classList.remove('open');
    _brainDockOpen = false;
    stopBrainAnimation();
    if (_brainPollId) { clearInterval(_brainPollId); _brainPollId = null; }
}
function expandBrainMap() {
    document.getElementById('brain-map-modal').classList.add('active');
    loadBrainState();
    // Start polling in expanded mode too (1.5s for real-time feel)
    if (!_brainPollId) {
        _brainPollId = setInterval(loadBrainState, 1500);
    }
}
async function showBrainMap() {
    // Legacy: open dock first
    toggleBrainDock();
}

// ══════════════════════════════════════════════════════════════════
// AGENT TERMINAL DOCK — Multi-Agent Orchestration UI
// ══════════════════════════════════════════════════════════════════

let _termDockOpen = false;
let _termSSE = null;
let _termSectionCounter = 0;

function toggleTerminalDock() {
    const dock = document.getElementById('terminal-dock');
    if (!dock) return;
    _termDockOpen = !_termDockOpen;
    dock.classList.toggle('open', _termDockOpen);
    if (_termDockOpen) {
        connectTerminalSSE();
        loadTerminalState();
    } else {
        disconnectTerminalSSE();
    }
}

function closeTerminalDock() {
    const dock = document.getElementById('terminal-dock');
    if (dock) dock.classList.remove('open');
    _termDockOpen = false;
    disconnectTerminalSSE();
}

function connectTerminalSSE() {
    if (_termSSE) return; // already connected
    try {
        _termSSE = new EventSource('/orchestrator/stream');
        _termSSE.onmessage = function(e) {
            try {
                const event = JSON.parse(e.data);
                handleTerminalEvent(event);
            } catch(err) {
                console.warn('Terminal SSE parse error:', err);
            }
        };
        _termSSE.onerror = function() {
            disconnectTerminalSSE();
            // Auto-reconnect after 3s
            if (_termDockOpen) {
                setTimeout(() => { if (_termDockOpen) connectTerminalSSE(); }, 3000);
            }
        };
    } catch(err) {
        console.warn('Terminal SSE connection failed:', err);
    }
}

function disconnectTerminalSSE() {
    if (_termSSE) {
        _termSSE.close();
        _termSSE = null;
    }
}

function handleTerminalEvent(event) {
    const type = event.type || 'info';
    const out = document.getElementById('term-output');
    if (!out) return;

    // Route swarm events to swarm handler
    if (type.startsWith('worker_') || type === 'agent_message' || type.startsWith('swarm_')) {
        handleSwarmEvent(event);
        // Also show in sequential output for visibility
    }
    if (_swarmMode === 'swarm' && type === 'diff_ready') {
        appendToSwarmCode(event);
    }

    switch(type) {
        case 'session_state':
            updateTermPhase(event.phase || 'IDLE');
            break;

        case 'info':
            appendTermLine(event.message || '', 'term-info');
            break;

        case 'agent_spawned':
            _termSectionCounter++;
            const badge = agentBadge(event.agent || 'ORCHESTRATOR');
            const modelStr = event.model || '';
            const modelOrb = getOrbitalKey(modelStr);
            const modelColors = {'openai':'#10a37f','gemini-high':'#4285f4','gemini-fast':'#34a853','gemini-lite':'#fbbc05','local':'#ff6600'};
            const modelBadge = modelStr ? ` <span style="color:${modelColors[modelOrb]||'#888'};font-size:11px;">[${modelStr}]</span>` : '';
            appendTermLine(`${badge}${event.message || 'Agent spawned'}${modelBadge}`, 'term-spawning');
            updateAgentCount();
            break;

        case 'agent_thinking':
            const tbadge = agentBadge(event.agent || 'ORCHESTRATOR');
            appendTermLine(`${tbadge}${event.message || 'Thinking...'}`, 'term-thinking');
            break;

        case 'agent_output':
            appendTermLine(event.message || '', 'term-executing');
            break;

        case 'plan_generated':
            updateTermPhase('PLAN');
            appendTermLine('', 'term-info');
            appendTermLine(`Plan: ${event.plan_summary || ''}`, 'term-success');
            appendTermLine(`Subtasks: ${event.subtask_count || 0} | Risk: ${event.risk || 'Unknown'}`, 'term-info');
            if (event.subtasks) {
                event.subtasks.forEach(s => {
                    appendTermLine(`  #${s.id}: ${s.description}`, 'term-info');
                });
            }
            updateTermProgress(0, event.subtask_count || 1);
            break;

        case 'diff_ready':
            appendTermLine('', 'term-info');
            appendTermLine(`Diff for subtask #${event.subtask_id} (${event.file_path || 'file'}):`, 'term-info');
            appendDiff(event.diff || '');
            if (event.confidence) {
                appendTermLine(`Confidence: ${event.confidence}%`, 'term-info');
            }
            break;

        case 'validation_running':
            const vbadge = agentBadge('VALIDATOR');
            appendTermLine(`${vbadge}$ ${event.command || ''}`, 'term-executing');
            break;

        case 'validation_passed':
            const vpbadge = agentBadge('VALIDATOR');
            appendTermLine(`${vpbadge}PASSED`, 'term-success');
            if (event.message) appendTermLine(`  ${event.message}`, 'term-info');
            break;

        case 'validation_failed':
            const vfbadge = agentBadge('VALIDATOR');
            appendTermLine(`${vfbadge}FAILED`, 'term-error');
            if (event.message) appendTermLine(`  ${event.message}`, 'term-error');
            break;

        case 'approval_requested':
            updateTermPhase(event.gate === 'plan' ? 'PLAN' : 'EXECUTE');
            showApprovalGate(event);
            break;

        case 'approved':
            appendTermLine(`Approved${event.subtask_id ? ' subtask #' + event.subtask_id : ' plan'}`, 'term-success');
            clearApprovalArea();
            break;

        case 'rejected':
            appendTermLine(`Rejected${event.subtask_id ? ' subtask #' + event.subtask_id : ' plan'}${event.reason ? ': ' + event.reason : ''}`, 'term-error');
            clearApprovalArea();
            break;

        case 'applied':
            appendTermLine(`Applied subtask #${event.subtask_id}`, 'term-success');
            updateTermPhase('APPLY');
            break;

        case 'rollback':
            appendTermLine(`ROLLBACK subtask #${event.subtask_id}: ${event.message || ''}`, 'term-error');
            break;

        case 'user_message':
            appendTermLine(`YOU: ${event.message || ''}`, 'term-user');
            break;

        case 'joi_response':
            appendTermLine(`JOI: ${event.message || ''}`, 'term-joi');
            break;

        case 'error':
            const ebadge = event.agent ? agentBadge(event.agent) : '';
            appendTermLine(`${ebadge}ERROR: ${event.message || 'Unknown error'}`, 'term-error');
            break;

        case 'session_complete':
            updateTermPhase(event.status === 'complete' ? 'COMPLETE' : 'FAILED');
            appendTermLine('', 'term-info');
            appendTermLine(event.message || 'Session complete', event.status === 'complete' ? 'term-success' : 'term-error');
            if (event.completed !== undefined) {
                updateTermProgress(event.completed, event.total || 1);
            }
            break;

        default:
            if (event.message) appendTermLine(event.message, 'term-info');
    }

    // Auto-scroll
    out.scrollTop = out.scrollHeight;
}

function appendTermLine(text, className) {
    const out = document.getElementById('term-output');
    if (!out) return;
    const line = document.createElement('div');
    line.className = 'term-line ' + (className || '');
    line.innerHTML = text;
    out.appendChild(line);
}

function appendDiff(diffText) {
    if (!diffText) return;
    const lines = diffText.split('\n');
    lines.forEach(line => {
        let cls = 'term-info';
        if (line.startsWith('+') && !line.startsWith('+++')) cls = 'term-diff-add';
        else if (line.startsWith('-') && !line.startsWith('---')) cls = 'term-diff-remove';
        else if (line.startsWith('@@')) cls = 'term-diff-header';
        else if (line.startsWith('---') || line.startsWith('+++')) cls = 'term-diff-header';
        appendTermLine(escapeHtml(line), cls);
    });
}

function escapeHtml(text) {
    const d = document.createElement('div');
    d.textContent = text;
    return d.innerHTML;
}

function agentBadge(agent) {
    const name = (agent || 'ORCHESTRATOR').toUpperCase();
    const cls = {
        'ORCHESTRATOR': 'term-badge-orchestrator',
        'ARCHITECT': 'term-badge-architect',
        'CODER': 'term-badge-coder',
        'VALIDATOR': 'term-badge-validator',
        'EXPLORE': 'term-badge-explore',
        'SECURITY': 'term-badge-security',
        'UIUX': 'term-badge-uiux',
        'TEST': 'term-badge-test',
        'QUEEN': 'term-badge-queen',
    }[name] || 'term-badge-orchestrator';
    return `<span class="term-badge ${cls}">${name}</span>`;
}

function updateTermPhase(phase) {
    const badge = document.getElementById('term-phase-badge');
    if (!badge) return;
    badge.textContent = phase;
    badge.className = 'term-phase-badge term-phase-' + phase;
}

function updateTermProgress(completed, total) {
    const bar = document.getElementById('term-progress-bar');
    if (!bar) return;
    const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
    bar.style.width = pct + '%';
}

function updateAgentCount() {
    const el = document.getElementById('term-agent-count');
    if (!el) return;
    const cur = parseInt(el.textContent || '0');
    el.textContent = cur + 1;
}

function showApprovalGate(event) {
    const area = document.getElementById('term-approval-area');
    if (!area) return;

    const isSubtask = event.gate === 'subtask';
    const stId = event.subtask_id;

    let diffHtml = '';
    if (event.diff) {
        const lines = event.diff.split('\n').map(l => {
            let cls = '';
            if (l.startsWith('+') && !l.startsWith('+++')) cls = 'term-diff-add';
            else if (l.startsWith('-') && !l.startsWith('---')) cls = 'term-diff-remove';
            else if (l.startsWith('@@') || l.startsWith('---') || l.startsWith('+++')) cls = 'term-diff-header';
            return `<div class="term-line ${cls}">${escapeHtml(l)}</div>`;
        }).join('');
        diffHtml = `<div class="term-approval-diff">${lines}</div>`;
    }

    area.innerHTML = `
        <div class="term-approval">
            <div class="term-approval-title">APPROVAL REQUIRED${isSubtask ? ' - Subtask #' + stId : ' - Plan'}</div>
            <div class="term-approval-meta">${event.description || event.message || ''}</div>
            ${diffHtml}
            <div class="term-approval-buttons">
                <button class="term-btn-approve" onclick="termApprove(${isSubtask ? stId : 'null'})">APPROVE</button>
                <button class="term-btn-reject" onclick="termReject(${isSubtask ? stId : 'null'})">REJECT</button>
            </div>
        </div>
    `;
}

function clearApprovalArea() {
    const area = document.getElementById('term-approval-area');
    if (area) area.innerHTML = '';
}

async function termApprove(subtaskId) {
    clearApprovalArea();
    try {
        await fetch('/orchestrator', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({action: 'approve', subtask_id: subtaskId})
        });
    } catch(e) { console.error('Approve failed:', e); }
}

async function termReject(subtaskId) {
    clearApprovalArea();
    try {
        await fetch('/orchestrator', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({action: 'reject', subtask_id: subtaskId})
        });
    } catch(e) { console.error('Reject failed:', e); }
}

async function sendTermChat() {
    const input = document.getElementById('term-chat-box');
    if (!input) return;
    const msg = input.value.trim();
    if (!msg) return;
    input.value = '';

    try {
        await fetch('/orchestrator/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: msg})
        });
    } catch(e) {
        appendTermLine('ERROR: Chat send failed', 'term-error');
    }
}

async function loadTerminalState() {
    try {
        const r = await fetch('/orchestrator');
        if (!r.ok) return;
        const data = await r.json();
        if (data.ok && data.session) {
            const s = data.session;
            updateTermPhase(s.phase || 'IDLE');
            const cnt = document.getElementById('term-agent-count');
            if (cnt) cnt.textContent = s.agent_count || 0;
            if (s.subtasks && s.subtasks.length > 0) {
                const completed = s.subtasks.filter(st => st.status === 'applied').length;
                updateTermProgress(completed, s.subtasks.length);
            }
        }
    } catch(e) { /* terminal state load failed silently */ }
}

// ── Swarm Mode ──
let _swarmMode = 'sequential';
let _swarmAgents = {};
let _selectedAgent = null;
let _swarmMsgCount = 0;

function toggleSwarmMode() {
    const dock = document.getElementById('terminal-dock');
    const btn = document.getElementById('swarm-mode-btn');
    const seqOut = document.getElementById('term-output');
    const swarmGrid = document.getElementById('swarm-grid');
    if (!dock || !btn || !seqOut || !swarmGrid) return;

    if (_swarmMode === 'sequential') {
        _swarmMode = 'swarm';
        btn.textContent = 'SWARM';
        btn.classList.add('active');
        dock.classList.add('swarm-mode');
        seqOut.style.display = 'none';
        swarmGrid.style.display = 'grid';
    } else {
        _swarmMode = 'sequential';
        btn.textContent = 'SEQ';
        btn.classList.remove('active');
        dock.classList.remove('swarm-mode');
        seqOut.style.display = '';
        swarmGrid.style.display = 'none';
    }
}

function handleSwarmEvent(event) {
    const type = event.type || '';

    switch(type) {
        case 'worker_spawned':
            addAgentCard(event.worker_id, event.role, 'spawned', event.description);
            break;
        case 'worker_claimed':
            updateAgentCard(event.worker_id, 'running', event.task_id, event.description);
            break;
        case 'worker_complete':
            updateAgentCard(event.worker_id, 'complete', event.task_id, event.summary);
            break;
        case 'worker_blocked':
            updateAgentCard(event.worker_id || ('coder_' + event.task_id), 'failed', event.task_id, event.reason);
            appendTermLine(`BLOCKED subtask #${event.task_id}: ${event.reason || ''}`, 'term-error');
            break;
        case 'worker_reverted':
            updateAgentCard(event.worker_id || ('coder_' + event.task_id), 'failed', event.task_id, event.reason);
            appendTermLine(`REVERTED subtask #${event.task_id}: ${event.reason || ''}`, 'term-error');
            break;
        case 'agent_message':
            appendMessageLog(event.from_agent, event.to_agent, event.message, event.severity);
            break;
        case 'swarm_task_list':
            renderTaskList(event.tasks || []);
            break;
        case 'swarm_complete':
            updateTermPhase(event.status === 'complete' ? 'COMPLETE' : 'FAILED');
            appendTermLine(event.message || 'Swarm complete',
                event.status === 'complete' ? 'term-success' : 'term-error');
            if (event.completed !== undefined) {
                updateTermProgress(event.completed, event.total || 1);
            }
            break;
    }
}

function addAgentCard(id, role, status, description) {
    if (!id) return;
    _swarmAgents[id] = {role, status, description: description || ''};
    const container = document.getElementById('swarm-agent-cards');
    if (!container) return;

    // Don't duplicate
    if (document.getElementById('agent-card-' + id)) return;

    const roleColors = {
        'coder':'#0f8', 'explore':'#4af', 'security':'#f55',
        'uiux':'#c8f', 'test':'#fa0', 'scaffold':'#0fc',
        'analyst':'#ff9f1c', 'report_writer':'#a8dadc', 'doc_writer':'#e9c46a'
    };
    const roleModels = {
        'coder':'gpt-5-codex-mini', 'explore':'gpt-4.1-mini', 'security':'o4-mini',
        'uiux':'gpt-5-mini', 'test':'o4-mini', 'scaffold':'gpt-5-nano',
        'analyst':'gpt-4.1-mini', 'report_writer':'gpt-5-mini', 'doc_writer':'gpt-5-codex-mini'
    };
    const color = roleColors[role] || '#0fc';
    const modelHint = roleModels[role] || '';

    const card = document.createElement('div');
    card.className = 'swarm-agent-card';
    card.id = 'agent-card-' + id;
    card.onclick = () => showAgentDetail(id);
    card.innerHTML = `
        <div><span class="agent-status ${status}"></span>
        <span class="agent-role" style="color:${color}">${(role||'coder').toUpperCase()}</span>
        ${modelHint ? `<span style="color:rgba(255,255,255,0.3);font-size:9px;margin-left:4px;">${modelHint}</span>` : ''}</div>
        <div class="agent-task" id="agent-task-${id}">${escapeHtml(description || id)}</div>
    `;
    container.appendChild(card);
}

function updateAgentCard(id, status, taskId, info) {
    if (!id) return;
    if (_swarmAgents[id]) {
        _swarmAgents[id].status = status;
        if (info) _swarmAgents[id].description = info;
    }

    const card = document.getElementById('agent-card-' + id);
    if (!card) {
        // Card not yet created — create it
        const role = id.split('_')[0] || 'coder';
        addAgentCard(id, role, status, info);
        return;
    }

    const dot = card.querySelector('.agent-status');
    if (dot) { dot.className = 'agent-status ' + status; }
    const taskEl = document.getElementById('agent-task-' + id);
    if (taskEl && info) { taskEl.textContent = info; }
}

function showAgentDetail(agentId) {
    _selectedAgent = agentId;
    const detail = document.getElementById('swarm-agent-detail');
    const title = document.getElementById('swarm-detail-title');
    const body = document.getElementById('swarm-detail-body');
    if (!detail || !title || !body) return;

    title.textContent = agentId;
    body.textContent = 'Loading...';
    detail.style.display = 'block';

    fetch('/swarm/agent/' + encodeURIComponent(agentId))
        .then(r => r.json())
        .then(data => {
            if (data.ok) {
                body.textContent = JSON.stringify(data, null, 2);
            } else {
                body.textContent = 'Agent not found: ' + (data.error || '');
            }
        })
        .catch(e => { body.textContent = 'Error: ' + e; });
}

function closeAgentDetail() {
    _selectedAgent = null;
    const detail = document.getElementById('swarm-agent-detail');
    if (detail) detail.style.display = 'none';
}

function renderTaskList(tasks) {
    const container = document.getElementById('swarm-task-list');
    if (!container) return;
    container.innerHTML = '';

    const _taskRoleColors = {
        'coder':'#0f8', 'explore':'#4af', 'security':'#f55',
        'uiux':'#c8f', 'test':'#fa0', 'scaffold':'#0fc',
        'analyst':'#ff9f1c', 'report_writer':'#a8dadc', 'doc_writer':'#e9c46a'
    };
    const _taskRoleModels = {
        'coder':'gpt-5-codex-mini', 'explore':'gpt-4.1-mini', 'security':'o4-mini',
        'uiux':'gpt-5-mini', 'test':'o4-mini', 'scaffold':'gpt-5-nano',
        'analyst':'gpt-4.1-mini', 'report_writer':'gpt-5-mini', 'doc_writer':'gpt-5-codex-mini'
    };

    tasks.forEach(t => {
        const item = document.createElement('div');
        item.className = 'swarm-task-item ' + (t.status || 'pending');
        const roleKey = (t.role || 'coder').toLowerCase();
        const roleColor = _taskRoleColors[roleKey] || '#0fc';
        const modelTag = _taskRoleModels[roleKey] ? `<span style="color:rgba(255,255,255,0.25);font-size:9px;margin-left:4px;">${_taskRoleModels[roleKey]}</span>` : '';
        item.innerHTML = `
            <span class="task-id">#${t.id}</span>
            <span class="task-role" style="color:${roleColor}">${roleKey.toUpperCase()}</span>${modelTag}
            <div style="margin-top:2px;color:rgba(255,255,255,0.5);font-size:10px;">${escapeHtml(t.description || '')}</div>
            ${t.claimed_by ? `<div class="task-claimed">${escapeHtml(t.claimed_by)}</div>` : ''}
        `;
        container.appendChild(item);
    });
}

function appendToSwarmCode(event) {
    const container = document.getElementById('swarm-code-output');
    if (!container) return;

    if (event.file_path) {
        const header = document.createElement('div');
        header.className = 'term-line term-info';
        header.textContent = `Subtask #${event.subtask_id} — ${event.file_path}`;
        container.appendChild(header);
    }

    if (event.diff) {
        event.diff.split('\n').forEach(line => {
            const el = document.createElement('div');
            el.className = 'term-line ';
            if (line.startsWith('+') && !line.startsWith('+++')) el.className += 'term-diff-add';
            else if (line.startsWith('-') && !line.startsWith('---')) el.className += 'term-diff-remove';
            else if (line.startsWith('@@') || line.startsWith('---') || line.startsWith('+++')) el.className += 'term-diff-header';
            else el.className += 'term-info';
            el.textContent = line;
            container.appendChild(el);
        });
    }
    container.scrollTop = container.scrollHeight;
}

function appendMessageLog(from, to, message, severity) {
    const log = document.getElementById('swarm-message-log');
    if (!log) return;

    _swarmMsgCount++;
    const item = document.createElement('div');
    item.className = 'swarm-msg-item' + (severity === 'critical' ? ' critical' : '');
    item.innerHTML = `<span class="msg-from">${escapeHtml(from || '?')}</span>→${escapeHtml(to || 'all')}: ${escapeHtml((message || '').substring(0, 100))}`;
    log.appendChild(item);

    // Prune to 20 entries
    while (log.children.length > 20) {
        log.removeChild(log.firstChild);
    }
    log.scrollTop = log.scrollHeight;
}

// ── End Agent Terminal ──

// ── LLM Selector + Review Toggle ──
let _dockReviewLoaded = false;
async function onLLMSelect(provider) {
    try {
        await fetch('/provider', {method:'POST', headers:{'Content-Type':'application/json'},
            body: JSON.stringify({provider})});
    } catch(e) { console.warn('Provider switch failed:', e); }
}
async function onReviewToggle(enabled) {
    try {
        await fetch('/review-mode', {method:'POST', headers:{'Content-Type':'application/json'},
            body: JSON.stringify({enabled})});
        const lbl = document.getElementById('review-label');
        if (lbl) lbl.textContent = enabled ? 'ON' : 'OFF';
    } catch(e) { console.warn('Review toggle failed:', e); }
}
async function loadProviderState() {
    try {
        const r = await fetch('/provider');
        const d = await r.json();
        const sel = document.getElementById('llm-selector');
        if (d.ok && sel) sel.value = d.provider || 'auto';
    } catch(e) { /* silent */ }
    try {
        const r2 = await fetch('/review-mode');
        const d2 = await r2.json();
        const chk = document.getElementById('review-toggle');
        const lbl = document.getElementById('review-label');
        if (chk) chk.checked = d2.enabled || false;
        if (lbl) lbl.textContent = d2.enabled ? 'ON' : 'OFF';
    } catch(e) { /* silent */ }
    _dockReviewLoaded = true;
}

// ── Load brain state ──
async function loadBrainState() {
    try {
        const r = await fetch('/neuro');
        const d = await r.json();
        if (d.ok) {
            _lastBrainState = d;
            renderBrainState(d);
            renderDockState(d);
        }
    } catch(e) { console.warn('Brain state load failed:', e); }
}

// ── Render SVG brain nodes (both dock + modal) — v3 ──
function renderBrainState(state) {
    if (!state) return;
    const sectors = state.sectors || {};
    const routing = state.routing || {};
    const inner = state.inner_state || {};
    const llm = state.llm_activity || {};
    const toolAct = state.tool_activity || [];
    const memAct = state.memory_activity || {};
    const globalMood = state.global_mood_effect || {};
    const isRest = state.rest_state || false;

    // Update SVG sector paths (modal) — with flash-on-activation
    document.querySelectorAll('.brain-sector').forEach(el => {
        const s = el.getAttribute('data-sector');
        const intensity = typeof sectors[s] === 'number' ? sectors[s] : (sectors[s] ? 1.0 : 0.0);
        const wasActive = el.classList.contains('active-' + s);
        el.className = 'brain-sector';
        if (intensity > 0.15) {
            el.classList.add('active-' + s);
            // Flash burst if newly activated or high intensity
            if (!wasActive || intensity > 0.6) {
                el.classList.remove('flash-burst');
                void el.offsetWidth; // force reflow to re-trigger animation
                el.classList.add('flash-burst');
            }
        }
        el.style.opacity = isRest ? Math.max(0.08, intensity) : Math.max(0.25, intensity);
    });

    // Update SVG brain nodes (dock) — opacity directly from intensity
    document.querySelectorAll('#brain-svg-v2 .brain-node').forEach(el => {
        const s = el.dataset.sector;
        const intensity = typeof sectors[s] === 'number' ? sectors[s] : 0;
        const innerCircle = el.querySelector('.node-inner');
        const glowCircle = el.querySelector('.node-glow');
        if (!innerCircle) return;

        el.style.opacity = isRest ? Math.max(0.05, intensity) : Math.max(0.12, intensity);
        if (glowCircle) glowCircle.setAttribute('opacity', Math.min(0.9, intensity * 0.9));

        // Remove animation classes
        el.classList.remove('thinking', 'flickering', 'firing', 'resting');

        // Firing flash for high-intensity sectors
        if (intensity > 0.7) el.classList.add('firing');

        // Rest state breathing on IDENTITY
        if (isRest && s === 'IDENTITY') el.classList.add('resting');

        // Empathy node gets mood-driven color
        if (s === 'EMPATHY' && routing.mood_color) {
            innerCircle.setAttribute('stroke', routing.mood_color);
            if (routing.mood_flicker) el.classList.add('flickering');
        }
    });

    // Neural traces — activate when BOTH endpoints > 0.25
    document.querySelectorAll('#brain-svg-v2 .brain-trace').forEach(el => {
        el.classList.remove('active');
        el.style.opacity = isRest ? '0.02' : '0.05';
    });
    BRAIN_CONNECTIONS.forEach(([a,b]) => {
        const traceEl = document.getElementById(`trace-${a}-${b}`) ||
                        document.getElementById(`trace-${b}-${a}`);
        if (!traceEl) return;
        const combined = (sectors[a]||0) + (sectors[b]||0);
        if (combined > 0.5) {
            traceEl.classList.add('active');
            traceEl.style.opacity = Math.min(0.8, combined * 0.4);
        }
    });

    // Latency alert on brain outline
    const outline = document.getElementById('brain-outline-path');
    if (outline) outline.classList.toggle('latency', !!state.latency_alert);
    const modalOutline = document.getElementById('modal-brain-outline');
    if (modalOutline) modalOutline.classList.toggle('latency', !!state.latency_alert);

    // LLM orbital activation (uses orbital_map from brain state if available)
    const orbitalMap = state.orbital_map || {};
    Object.entries(LLM_BEAMS).forEach(([orbitalKey, beam]) => {
        const orbitalEl = document.getElementById(beam.node);
        const beamEl = document.getElementById(`beam-${orbitalKey}`);
        const modalOrbitalEl = document.getElementById(`modal-${beam.node}`);

        // Check orbital_map first, fall back to model string matching
        let isActive = false;
        if (orbitalMap[orbitalKey]) {
            isActive = orbitalMap[orbitalKey].active && llm.age_seconds < 30;
        } else {
            // Fallback: resolve active_model → orbital key
            const resolvedKey = getOrbitalKey(llm.active_model);
            isActive = resolvedKey === orbitalKey && llm.age_seconds < 30;
        }

        const displayName = (llm.display_name || llm.active_model || routing.model || '').toString();
        const labelText = isActive && displayName && displayName !== 'none' ? (displayName.length > 14 ? displayName.substring(0, 14) + '…' : displayName) : (LLM_ORBITAL_DEFAULT_LABELS[orbitalKey] || orbitalKey);
        const modalLabelText = isActive && displayName && displayName !== 'none' ? (displayName.length > 16 ? displayName.substring(0, 16) + '…' : displayName) : (LLM_ORBITAL_MODAL_DEFAULT_LABELS[orbitalKey] || orbitalKey);

        if (orbitalEl) {
            orbitalEl.style.opacity = isActive ? '1.0' : '0.1';
            orbitalEl.classList.toggle('active', isActive);
            const lbl = orbitalEl.querySelector('.orbital-label');
            if (lbl) lbl.textContent = labelText;
        }
        if (modalOrbitalEl) {
            modalOrbitalEl.style.opacity = isActive ? '1.0' : '0.15';
            modalOrbitalEl.classList.toggle('active', isActive);
            const modalLbl = modalOrbitalEl.querySelector('.orbital-label');
            if (modalLbl) modalLbl.textContent = modalLabelText;
        }
        if (beamEl) {
            beamEl.style.opacity = isActive ? '0.6' : '0';
            beamEl.classList.toggle('active', isActive);
        }
        // Spawn beam particles when active
        if (isActive && _brainCanvasCtx) {
            const dir = llm.direction === 'sending' ? [beam.from, beam.to] : [beam.to, beam.from];
            for (let i = 0; i < 3; i++) {
                _brainParticles.push(new NeuralParticle(dir[0], dir[1], {
                    isBeam: true, speed: 0.012, size: 3 + Math.random()*2,
                    color: beam.color, alpha: 0.7
                }));
            }
        }
    });

    // Memory recall burst — blue energy wave on LONG_MEMORY
    if (memAct.recalled > 0 && memAct.intensity > 0.4) {
        triggerNodeBurst('LONG_MEMORY', '#3c64ff', memAct.intensity);
    }

    // Global mood HUD effect
    applyGlobalMoodEffect(globalMood);

    // Spawn regular particles for active connections (skip in rest state)
    if (_brainCanvasCtx && !isRest) {
        // Keep existing particles, add new ones
        const maxParticles = 120;
        BRAIN_CONNECTIONS.forEach(([a,b]) => {
            if (_brainParticles.length >= maxParticles) return;
            const aNode = BRAIN_NODES[a];
            const bNode = BRAIN_NODES[b];
            if (!aNode || !bNode) return;
            const combined = (sectors[a]||0) + (sectors[b]||0);
            if (combined > 0.5) {
                const count = Math.min(Math.ceil(combined * 2), 6);
                for (let i = 0; i < count; i++) {
                    if (Math.random() < 0.3) { // spawn probabilistically
                        _brainParticles.push(new NeuralParticle(aNode, bNode));
                    }
                }
            }
        });
        if (_brainParticles.length > 0 && !_brainAnimFrame) startBrainAnimation();
    }

    // Modal-specific elements
    const modelEl = document.getElementById('neuro-model');
    if (modelEl) modelEl.textContent = 'MODEL: ' + (routing.model || '--');
    const latEl = document.getElementById('neuro-latency');
    if (latEl) latEl.textContent = 'LATENCY: ' + (routing.response_time_ms || 0) + 'ms';
    const moodEl = document.getElementById('neuro-mood');
    if (moodEl) moodEl.textContent = 'MOOD: ' + (inner.mood || '--');
    const arcEl = document.getElementById('neuro-arc');
    if (arcEl) arcEl.textContent = 'ARC: ' + (inner.conversation_arc || '--');
    const modeTag = document.getElementById('neuro-mode');
    if (modeTag) modeTag.textContent = 'MODE: ' + (routing.mode || '--').toUpperCase();
    const provTag = document.getElementById('neuro-provider');
    if (provTag) provTag.textContent = 'PROVIDER: ' + (routing.provider || '--').toUpperCase();

    // Context tags (modal)
    const tagsEl = document.getElementById('neuro-context-tags');
    if (tagsEl) {
        const ctx = state.context_injected || [];
        tagsEl.innerHTML = ctx.map(c => `<span class="ctx-chip active">${c}</span>`).join('');
    }

    // Inner state gauges (modal)
    const gaugesEl = document.getElementById('neuro-gauges');
    if (gaugesEl) {
        const gaugeKeys = ['energy','trust','closeness','stress','curiosity','sass','warmth'];
        const gaugeColors = {energy:'#0fc',trust:'#78f',closeness:'#f0f',stress:'#f55',curiosity:'#fda',sass:'#f8a',warmth:'#fa5'};
        gaugesEl.innerHTML = gaugeKeys.map(k => {
            const v = inner[k] || 0;
            const pct = Math.round(v * 100);
            const col = gaugeColors[k] || '#888';
            return `<div class="neuro-gauge"><div class="neuro-gauge-label">${k.toUpperCase()} ${pct}%</div><div class="neuro-gauge-bar"><div class="neuro-gauge-fill" style="width:${pct}%;background:${col};"></div></div></div>`;
        }).join('');
    }

    // Monologue (modal)
    const monoEl = document.getElementById('neuro-monologue');
    if (monoEl) {
        const thoughts = state.monologue || [];
        if (thoughts.length === 0) {
            monoEl.innerHTML = '<div style="color:rgba(255,255,255,0.3);font-size:12px;">No internal thoughts captured this session.</div>';
        } else {
            monoEl.innerHTML = thoughts.map(t => {
                const ts = t.timestamp ? new Date(t.timestamp * 1000).toLocaleTimeString() : '';
                const text = t.thought || t.content || JSON.stringify(t);
                return `<div class="monologue-item"><span class="thought-ts">${ts}</span> ${text}</div>`;
            }).join('');
        }
    }

    // Logprobs (modal)
    const lpEl = document.getElementById('neuro-logprobs');
    if (lpEl) {
        const lp = state.logprobs || [];
        if (lp.length === 0) {
            lpEl.innerHTML = '<span style="color:rgba(255,255,255,0.3);">No logprobs. Enable JOI_ENABLE_LOGPROBS=1 in .env.</span>';
        } else {
            lpEl.innerHTML = lp.map(entry => {
                const alts = (entry.alternatives || []).slice(0, 3).map(a =>
                    `<span class="logprob-alt">[${a.token}:${a.logprob.toFixed(2)}]</span>`
                ).join(' ');
                return `<span class="logprob-token"><span class="logprob-chosen">${entry.token}</span>${alts ? ' ' + alts : ''} </span>`;
            }).join('');
        }
    }

    // Personality sliders (modal)
    renderPersonalitySliders(state.personality_weights || {});
}

// ── Global mood HUD effect ──
function applyGlobalMoodEffect(effect) {
    const dock = document.getElementById('brain-dock');
    if (!dock) return;
    dock.classList.remove('mood-sass', 'mood-stress', 'mood-energy');
    if (effect.effect === 'sass_flicker') dock.classList.add('mood-sass');
    else if (effect.effect === 'stress_flicker') dock.classList.add('mood-stress');
    else if (effect.effect === 'energy_surge') dock.classList.add('mood-energy');
}

// ── Node burst animation (tool execution flashes, memory recall) ──
function triggerNodeBurst(sectorName, color, intensity) {
    const node = document.querySelector(`.brain-node[data-sector="${sectorName}"]`);
    if (!node) return;
    node.style.transition = 'none';
    node.style.filter = `brightness(${1 + intensity * 2}) drop-shadow(0 0 ${intensity * 15}px ${color})`;
    setTimeout(() => {
        node.style.transition = 'all 0.8s ease-out';
        node.style.filter = '';
    }, 200 + intensity * 300);
}

// ── Render dock-specific compact state ──
function renderDockState(state) {
    if (!state) return;
    const routing = state.routing || {};
    const inner = state.inner_state || {};
    const isRest = state.rest_state || false;

    // Compact metrics + LLM selector + review toggle
    const metricsEl = document.getElementById('brain-dock-metrics');
    if (metricsEl) {
        const gaugeKeys = [{k:'energy',c:'#0fc'},{k:'stress',c:'#f55'},{k:'sass',c:'#f8a'},{k:'warmth',c:'#fa5'}];
        const restLabel = isRest ? ' <span style="color:#555;font-size:9px;">[REST]</span>' : '';
        const curProvider = (routing.provider || 'auto').toLowerCase();
        const verif = state.verification;
        const verifLabel = verif ? (verif.approved ? `<span style="color:#0f8;">&#10003; ${verif.verifier_model}</span>` : `<span style="color:#f55;">&#10007; ${verif.verifier_model}</span>`) : '';
        metricsEl.innerHTML = `
            <div class="dock-metric-row"><span>MODEL</span><span>${routing.model || '--'}${restLabel}</span></div>
            <div class="dock-metric-row"><span>MODE</span><span>${(routing.mode || '--').toUpperCase()}</span></div>
            <div class="dock-metric-row"><span>LATENCY</span><span>${routing.response_time_ms || 0}ms${verifLabel ? ' ' + verifLabel : ''}</span></div>
            <div class="dock-metric-row" style="margin-top:4px;">
                <span>LLM</span>
                <select id="llm-selector" onchange="onLLMSelect(this.value)">
                    <option value="auto"${curProvider==='auto'?' selected':''}>Auto (Brain)</option>
                    <option value="openai"${curProvider==='openai'?' selected':''}>GPT-4o</option>
                    <option value="gemini"${curProvider==='gemini'?' selected':''}>Gemini</option>
                    <option value="local"${curProvider==='local'?' selected':''}>Local/Mistral</option>
                </select>
            </div>
            <div class="dock-metric-row">
                <span>REVIEW</span>
                <label style="display:flex;align-items:center;gap:4px;">
                    <input type="checkbox" id="review-toggle" onchange="onReviewToggle(this.checked)"/>
                    <span id="review-label" style="font-size:10px;color:rgba(255,255,255,0.5);">OFF</span>
                </label>
            </div>
            <div class="dock-gauges">${gaugeKeys.map(g => {
                const v = inner[g.k] || 0;
                const pct = Math.round(v * 100);
                return `<div class="dock-gauge"><span class="dock-gauge-label">${g.k}</span><div class="dock-gauge-bar"><div class="dock-gauge-fill" style="width:${pct}%;background:${g.c};"></div></div></div>`;
            }).join('')}</div>
        `;
        // Restore review toggle state (don't overwrite on each render)
        if (typeof _dockReviewLoaded === 'undefined' || !_dockReviewLoaded) {
            loadProviderState();
        }
    }

    // Latency warning
    const latWarn = document.getElementById('dock-latency-warning');
    if (latWarn) latWarn.classList.toggle('active', !!state.latency_alert);

    // Thought stream with logprob token alternatives
    const streamEl = document.getElementById('thought-stream-content');
    if (streamEl) {
        const thoughts = state.monologue || [];
        const lp = state.logprobs || [];
        let html = '';

        // Monologue items first
        if (thoughts.length > 0) {
            html += thoughts.slice(0, 8).map(t => {
                const ts = t.timestamp ? new Date(t.timestamp * 1000).toLocaleTimeString() : '';
                const text = t.thought || t.content || JSON.stringify(t);
                return `<div class="stream-item"><span class="stream-ts">${ts}</span> ${text}</div>`;
            }).join('');
        }

        // Logprob tokens
        if (lp.length > 0) {
            html += '<div class="stream-item" style="color:rgba(255,255,255,0.2);font-size:9px;letter-spacing:1px;margin-top:4px;">TOKEN LOGITS</div>';
            html += lp.slice(0, 15).map(entry => {
                const alts = (entry.alternatives || []).slice(0, 3)
                    .map(a => `<span class="stream-alt">${a.token}:${a.logprob.toFixed(2)}</span>`).join(' ');
                return `<div class="stream-item"><span class="stream-chosen">${entry.token}</span> ${alts}</div>`;
            }).join('');
        }

        if (!html) {
            html = isRest
                ? '<div class="stream-item" style="opacity:0.2">idle — no activity</div>'
                : '<div style="color:rgba(255,255,255,0.25);font-size:11px;padding:4px 0;">No thoughts yet. Send a message.</div>';
        }
        streamEl.innerHTML = html;
    }

    // Vision thumbnail
    if (state.has_vision_thumb) loadVisionThumbnail();

    // ── Sci‑Fi HUD widgets: LLM badge, Cognitive Load, Empathy, 3D brain, Synaptic Pulse, EKG, Logic Log ──
    const displayName = (state.llm_activity && state.llm_activity.display_name) || state.routing?.model || '--';
    const llmText = displayName === 'none' ? 'idle' : displayName;
    const llmNameEl = document.getElementById('neuro-llm-name');
    if (llmNameEl) llmNameEl.textContent = llmText;
    const llmDisplayEl = document.getElementById('neuro-llm-display');
    if (llmDisplayEl) llmDisplayEl.textContent = llmText;
    const cogRing = document.getElementById('cognitive-load-ring');
    const cogPctEl = document.getElementById('cognitive-load-pct');
    const cogStatusEl = document.getElementById('cognitive-load-status');
    if (cogRing && cogPctEl) {
        const processing = state.processing || false;
        const sectors = state.sectors || {};
        const maxSector = Math.max(0, ...Object.values(sectors).filter(v => typeof v === 'number'));
        const rt = state.routing?.response_time_ms || 0;
        let pct = (processing ? 45 : 0) + maxSector * 35 + Math.min(25, Math.floor(rt / 80));
        pct = Math.min(100, Math.round(pct));
        cogRing.style.setProperty('--cog-deg', pct * 3.6 + 'deg');
        cogRing.classList.toggle('cognitive-load-high', pct > 70);
        cogPctEl.textContent = pct + '%';
        if (cogStatusEl) cogStatusEl.textContent = pct > 70 ? 'HIGH' : 'NORMAL';
    }
    const empathySphere = document.getElementById('empathy-sphere');
    const empathyTone = document.getElementById('empathy-tone');
    if (empathySphere && empathyTone) {
        const mood = (state.inner_state && state.inner_state.mood) || 'chill';
        const warmth = (state.inner_state && state.inner_state.warmth) || 0.6;
        const colors = { calm: '#4488ff', chill: '#8866ff', analytical: '#aa66ff', playful: '#ff88cc', focused: '#00ffcc', tender: '#ffaacc', excited: '#ffaa44', sassy: '#ff00ff', stressed: '#ff4466', protective: '#ff4444', creative: '#cc44ff', curious: '#00ccff', loving: '#ff66aa', unknown: '#8866ff' };
        const bg = colors[mood] || colors.unknown;
        empathySphere.style.background = `radial-gradient(circle at 30% 30%, ${bg}, ${bg}88)`;
        empathySphere.style.boxShadow = `0 0 20px ${bg}99, inset -4px -4px 12px rgba(0,0,0,0.3)`;
        empathyTone.textContent = (mood || '--').toUpperCase();
    }
    const brainCanvasWrap = document.getElementById('brain-canvas-wrap');
    if (brainCanvasWrap) {
        const sectors = state.sectors || {};
        const activeCount = Object.values(sectors).filter(v => typeof v === 'number' && v > 0.2).length;
        const t = (Date.now() / 4000) % (Math.PI * 2);
        const tilt = 2 + Math.sin(t) * 4;
        const rotY = (Date.now() / 8000) * 15 + activeCount * 3;
        brainCanvasWrap.style.transform = `rotateY(${rotY}deg) rotateX(${tilt}deg)`;
    }
    updateSynapticPulseCanvas(state.processing, state.sectors);
    updateMemoryEkgCanvas(state.routing?.response_time_ms, state.memory_activity);
    updateLogicLog(state);
    // Active firings (derived from processing + sector activity)
    const afEl = document.getElementById('neuro-active-firings');
    if (afEl && state.sectors) {
        const sum = Object.values(state.sectors).filter(v => typeof v === 'number').reduce((a,b) => a + b, 0);
        const firings = Math.round((state.processing ? 4000 : 200) + sum * 600);
        afEl.textContent = 'ACTIVE FIRINGS: ' + firings + '/sec';
    }
    // Function Loadout bars (all sectors, real-time)
    const loadoutEl = document.getElementById('neuro-loadout-bars');
    if (loadoutEl && state.sectors) {
        const ALL_SECTORS = ['IDENTITY','REASONING','LANGUAGE','CREATIVITY','LONG_MEMORY','SHORT_MEMORY','FACTS','LEARNING','VISION','CAMERA','VOICE','WEB','TOOLS','FILES','DESKTOP','REPAIR','EMPATHY','ORCHESTRATOR','ARCHITECT','CODER','VALIDATOR'];
        loadoutEl.innerHTML = ALL_SECTORS.map(name => {
            const v = state.sectors[name];
            const pct = Math.min(100, Math.round((typeof v === 'number' ? v : 0) * 100));
            return '<div class="neuro-loadout-row"><span class="neuro-loadout-label">' + name + '</span><div class="neuro-loadout-bar"><div class="neuro-loadout-fill" style="width:' + pct + '%;"></div></div><span class="neuro-loadout-pct">' + pct + '%</span></div>';
        }).join('');
    }
}

// ── Synaptic Pulse: zig-zag neon lines when processing ──
let _synapticPhase = 0;
function updateSynapticPulseCanvas(processing, sectors) {
    const canvas = document.getElementById('synaptic-pulse-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width; const h = canvas.height;
    ctx.fillStyle = 'rgba(0,0,0,0.4)';
    ctx.fillRect(0, 0, w, h);
    const intensity = processing ? 1 : (sectors && typeof sectors.REASONING === 'number' ? sectors.REASONING * 0.6 : 0);
    _synapticPhase += 0.15 + intensity * 0.2;
    ctx.strokeStyle = `rgba(0,255,204,${0.2 + intensity * 0.5})`;
    ctx.lineWidth = 1.5;
    ctx.shadowBlur = 8;
    ctx.shadowColor = '#00ffcc';
    ctx.beginPath();
    for (let x = 0; x <= w; x += 12) {
        const y = h / 2 + Math.sin((x / 20) + _synapticPhase) * 12 + Math.sin((x / 8) + _synapticPhase * 2) * 4;
        if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.shadowBlur = 0;
}

// ── Memory Latency: EKG-style wave ──
const _ekgBuffer = [];
const EKG_MAX = 80;
function updateMemoryEkgCanvas(responseTimeMs, memoryActivity) {
    const canvas = document.getElementById('memory-ekg-canvas');
    if (!canvas) return;
    const v = responseTimeMs || 0;
    const memInt = (memoryActivity && memoryActivity.intensity) || 0;
    _ekgBuffer.push(Math.min(1, (v / 3000) * 0.7 + memInt * 0.3));
    if (_ekgBuffer.length > EKG_MAX) _ekgBuffer.shift();
    const ctx = canvas.getContext('2d');
    const w = canvas.width; const h = canvas.height;
    ctx.fillStyle = 'rgba(0,0,0,0.4)';
    ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = 'rgba(0,255,204,0.8)';
    ctx.lineWidth = 2;
    ctx.shadowBlur = 6;
    ctx.shadowColor = '#00ffcc';
    ctx.beginPath();
    const step = w / (EKG_MAX - 1);
    _ekgBuffer.forEach((val, i) => {
        const x = i * step;
        const y = h - 4 - val * (h - 8);
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.stroke();
    ctx.shadowBlur = 0;
}

// ── Logic Log: Matrix-style scrolling green text ──
let _logicLogLines = [];
const LOG_MAX_LINES = 12;
function updateLogicLog(state) {
    const container = document.getElementById('logic-log-content');
    if (!container) return;
    const parts = [];
    if (state.context_injected && state.context_injected.length) parts.push(state.context_injected.slice(0, 3).join(' '));
    if (state.monologue && state.monologue.length) state.monologue.slice(0, 2).forEach(m => parts.push((m.thought || m.content || '').slice(0, 40)));
    if (state.routing && state.routing.model) parts.push('LLM:' + state.routing.model);
    const line = parts.join(' | ').slice(0, 48) || (state.rest_state ? 'idle' : '...');
    if (line && line !== 'idle') _logicLogLines.push(line);
    if (_logicLogLines.length > LOG_MAX_LINES) _logicLogLines.shift();
    container.innerHTML = _logicLogLines.map(l => '<div style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' + l.replace(/</g, '&lt;') + '</div>').join('');
    container.scrollTop = container.scrollHeight;
}

// ── Vision thumbnail ──
async function loadVisionThumbnail() {
    try {
        const r = await fetch('/neuro/vision-thumb');
        const d = await r.json();
        const img = document.getElementById('dock-vision-thumb');
        if (d.ok && img) {
            img.src = 'data:image/jpeg;base64,' + d.thumbnail;
            img.classList.add('active');
        }
    } catch(e) { /* silent */ }
}

// ── Canvas particle system — v3 curved bezier paths ──
class NeuralParticle {
    constructor(from, to, options = {}) {
        this.from = from;
        this.to = to;
        this.t = Math.random();
        this.speed = options.speed || (0.002 + Math.random() * 0.006);
        this.color = options.color || from.color || '#ff00ff';
        this.size = options.size || (1.2 + Math.random() * 2);
        this.alpha = options.alpha || (0.3 + Math.random() * 0.5);
        this.isBeam = options.isBeam || false;
        // Curved path control point (offset from midpoint)
        const mx = (from.x + to.x) / 2;
        const my = (from.y + to.y) / 2;
        this.cx = mx + (Math.random() - 0.5) * 30;
        this.cy = my + (Math.random() - 0.5) * 30;
        this._dead = false;
    }
    update() {
        this.t += this.speed;
        if (this.t > 1) {
            if (this.isBeam) { this._dead = true; return; }
            this.t = 0;
        }
    }
    draw(ctx, scaleX, scaleY) {
        // Quadratic bezier interpolation
        const t = this.t;
        const x = (1-t)*(1-t)*this.from.x + 2*(1-t)*t*this.cx + t*t*this.to.x;
        const y = (1-t)*(1-t)*this.from.y + 2*(1-t)*t*this.cy + t*t*this.to.y;
        ctx.beginPath();
        ctx.arc(x * scaleX, y * scaleY, this.size, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        const fadeCurve = Math.sin(this.t * Math.PI); // bell curve fade
        ctx.globalAlpha = this.alpha * fadeCurve;
        if (this.isBeam && this.size > 3) {
            ctx.shadowBlur = 8;
            ctx.shadowColor = this.color;
        }
        ctx.fill();
        ctx.shadowBlur = 0;
        ctx.globalAlpha = 1;
    }
}

function initBrainCanvas() {
    const canvas = document.getElementById('brain-canvas');
    if (!canvas) return;
    const wrap = document.getElementById('brain-canvas-wrap');
    if (wrap) {
        canvas.width = wrap.clientWidth || 340;
        canvas.height = wrap.clientHeight || 340;
    }
    _brainCanvasCtx = canvas.getContext('2d');
}

function startBrainAnimation() {
    if (_brainAnimFrame) return;
    function animate() {
        if (!_brainCanvasCtx) return;
        const canvas = _brainCanvasCtx.canvas;
        const scaleX = canvas.width / 340;
        const scaleY = canvas.height / 340;
        _brainCanvasCtx.clearRect(0, 0, canvas.width, canvas.height);
        // Update + draw, remove dead particles
        _brainParticles = _brainParticles.filter(p => {
            p.update();
            if (p._dead) return false;
            p.draw(_brainCanvasCtx, scaleX, scaleY);
            return true;
        });
        // Cap particles to prevent memory bloat
        if (_brainParticles.length > 200) {
            _brainParticles = _brainParticles.slice(-150);
        }
        _brainAnimFrame = requestAnimationFrame(animate);
    }
    animate();
}

function stopBrainAnimation() {
    if (_brainAnimFrame) {
        cancelAnimationFrame(_brainAnimFrame);
        _brainAnimFrame = null;
    }
}

// ── Processing animation ──
function startProcessingAnimation() {
    // Light up key nodes as "thinking" (not all 16 — just cognition chain)
    ['IDENTITY','REASONING','LANGUAGE','EMPATHY','SHORT_MEMORY'].forEach(s => {
        const el = document.querySelector(`#brain-svg-v2 .brain-node[data-sector="${s}"]`);
        if (el) el.classList.add('thinking');
    });
    const label = document.getElementById('brain-processing-label');
    if (label) label.classList.add('active');

    // Spawn processing particles along cognition chain
    if (_brainCanvasCtx) {
        const processingPaths = [
            [BRAIN_NODES.LANGUAGE, BRAIN_NODES.REASONING],
            [BRAIN_NODES.REASONING, BRAIN_NODES.LONG_MEMORY],
            [BRAIN_NODES.IDENTITY, BRAIN_NODES.EMPATHY],
            [BRAIN_NODES.SHORT_MEMORY, BRAIN_NODES.REASONING],
        ];
        processingPaths.forEach(([a,b]) => {
            if (a && b) {
                for (let i = 0; i < 4; i++) _brainParticles.push(new NeuralParticle(a, b));
            }
        });
        if (!_brainAnimFrame) startBrainAnimation();
    }

    // Poll processing state
    _processingPollId = setInterval(async () => {
        try {
            const r = await fetch('/neuro/processing');
            const d = await r.json();
            if (!d.processing) stopProcessingAnimation();
        } catch(e) { /* continue */ }
    }, 3000);
}

function stopProcessingAnimation() {
    if (_processingPollId) { clearInterval(_processingPollId); _processingPollId = null; }
    document.querySelectorAll('#brain-svg-v2 .brain-node').forEach(el => el.classList.remove('thinking'));
    const label = document.getElementById('brain-processing-label');
    if (label) label.classList.remove('active');
}

// ── Latency mode switch ──
async function switchToPrecisionMode() {
    try {
        await fetch('/mode', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({mode:'precision'})});
        const badge = document.getElementById('mode-badge');
        if (badge) badge.textContent = 'mode: precision';
        const warn = document.getElementById('dock-latency-warning');
        if (warn) warn.classList.remove('active');
    } catch(e) { console.warn('Mode switch failed:', e); }
}

// ── Personality sliders ──
function renderPersonalitySliders(weights) {
    const el = document.getElementById('neuro-personality');
    if (!el) return;
    const sliderDefs = [
        {key:'ariana_layer', label:'Ariana Layer'},
        {key:'modern_layer', label:'Modern Layer'},
        {key:'devotion_layer', label:'Devotion Layer'},
        {key:'sass', label:'Sass'},
        {key:'warmth', label:'Warmth'},
        {key:'energy', label:'Energy'},
    ];
    el.innerHTML = sliderDefs.map(s => {
        const v = weights[s.key] || 0;
        const pct = Math.round(v * 100);
        return `<div class="personality-slider">
            <label><span>${s.label}</span><span id="pw-val-${s.key}">${pct}%</span></label>
            <input type="range" min="0" max="100" value="${pct}" oninput="onPersonalitySlider('${s.key}', this.value)">
        </div>`;
    }).join('');
}

let _pwDebounce = null;
function onPersonalitySlider(key, val) {
    const pct = parseInt(val);
    const valEl = document.getElementById('pw-val-' + key);
    if (valEl) valEl.textContent = pct + '%';
    clearTimeout(_pwDebounce);
    _pwDebounce = setTimeout(() => setPersonalityWeight(key, pct / 100), 400);
}

async function setPersonalityWeight(key, value) {
    try {
        const r = await fetch('/neuro/personality', {
            method:'POST', headers:{'Content-Type':'application/json'},
            body: JSON.stringify({key, value})
        });
        const d = await r.json();
        if (!d.ok) console.warn('Personality weight update failed:', d.error);
    } catch(e) { console.warn('Personality weight error:', e); }
}

// ── Response integration ──
function updateBrainMapFromResponse(brainState) {
    _lastBrainState = brainState;
    stopProcessingAnimation();
    renderBrainState(brainState);
    if (_brainDockOpen) renderDockState(brainState);

    // Flash active sectors briefly
    const sectors = brainState.sectors || {};
    Object.entries(sectors).forEach(([s, v]) => {
        if (v > 0.5) {
            const nodeColor = BRAIN_NODES[s] ? BRAIN_NODES[s].color : '#fff';
            triggerNodeBurst(s, nodeColor, v);
        }
    });

    // Flash tool-specific sectors
    const toolAct = brainState.tool_activity || [];
    toolAct.forEach(ta => {
        const nodeColor = BRAIN_NODES[ta.sector] ? BRAIN_NODES[ta.sector].color : '#ff6644';
        triggerNodeBurst(ta.sector, nodeColor, 0.8);
    });

    checkForScanPulse();
}

async function checkForScanPulse() {
    try {
        const r = await fetch('/neuro/scan');
        const d = await r.json();
        if (d.ok && d.recent) triggerScanAnimation();
    } catch(e) { /* non-critical */ }
}

function triggerScanAnimation() {
    const container = document.getElementById('brain-svg-container');
    if (container) {
        container.classList.add('scanning');
        setTimeout(() => container.classList.remove('scanning'), 1400);
    }
}

function toggleNeuroSection(name) {
    const section = document.getElementById(name + '-section');
    const toggle = document.getElementById(name + '-toggle');
    if (!section) return;
    const open = section.style.display !== 'none';
    section.style.display = open ? 'none' : 'block';
    toggle.classList.toggle('open', !open);
}

async function showDiagnostics() {
    document.getElementById('diagnostics-modal').classList.add('active');
    loadManifest();
}

async function loadManifest() {
    const el = document.getElementById('diag-manifest');
    el.innerHTML = 'Loading...';
    try {
        const r = await fetch('/diagnostics/manifest?refresh=1'); const d = await r.json();
        if (d.ok && d.manifest) {
            const m = d.manifest;
            let html = '<div style="margin-bottom:10px;"><strong>Uptime:</strong> ' + Math.round(m.uptime_seconds) + 's</div>';
            html += '<div style="margin-bottom:8px;"><strong>Providers:</strong> ';
            for (const [k,v] of Object.entries(m.providers||{})) {
                html += '<span style="margin-right:8px;color:' + (v ? '#0f0' : '#f55') + ';">' + k + (v ? ' ✓' : ' ✗') + '</span>';
            }
            html += '</div>';
            html += '<div style="margin-bottom:8px;"><strong>Features:</strong> ';
            for (const [k,v] of Object.entries(m.features||{})) {
                html += '<span style="margin-right:8px;color:' + (v ? '#0f0' : '#888') + ';">' + k + (v ? ' ✓' : ' ✗') + '</span>';
            }
            html += '</div>';
            html += '<div style="margin-bottom:8px;"><strong>Memory:</strong> ' + (m.memory?.backend||'?') + ' (' + (m.memory?.count||0) + ' vectors)</div>';
            html += '<details><summary style="cursor:pointer;color:var(--secondary);"><strong>Tools (' + m.tool_count + ')</strong></summary><div style="margin:6px 0;column-count:2;">';
            (m.tools||[]).forEach(t => { html += '<div style="font-size:11px;padding:1px 0;">' + t + '</div>'; });
            html += '</div></details>';
            html += '<details><summary style="cursor:pointer;color:var(--secondary);"><strong>Routes (' + m.route_count + ')</strong></summary><div style="margin:6px 0;">';
            (m.routes||[]).forEach(r => { html += '<div style="font-size:11px;padding:1px 0;">' + r.rule + ' [' + r.methods.join(',') + ']</div>'; });
            html += '</div></details>';
            el.innerHTML = html;
        } else { el.innerHTML = 'Failed to load manifest'; }
    } catch(e) { el.innerHTML = 'Error: ' + e.message; }
}

async function runSelfTest() {
    const status = document.getElementById('diag-test-status');
    const results = document.getElementById('diag-test-results');
    status.textContent = 'Running...';
    status.style.color = '#ffaa00';
    results.innerHTML = '';
    try {
        const r = await fetch('/diagnostics/self-test', {method:'POST'}); const d = await r.json();
        if (d.ok) {
            status.textContent = d.all_pass ? 'ALL PASS' : 'SOME FAILURES';
            status.style.color = d.all_pass ? '#0f0' : '#f55';
            let html = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:13px;">';
            for (const [name, result] of Object.entries(d.tests||{})) {
                const ok = result.pass;
                html += '<div style="padding:6px 10px;border-radius:6px;background:' + (ok ? 'rgba(0,255,0,0.08)' : 'rgba(255,0,0,0.08)') + ';border:1px solid ' + (ok ? '#0f04' : '#f004') + ';">';
                html += '<span style="color:' + (ok ? '#0f0' : '#f55') + ';font-weight:bold;">' + (ok ? '✓' : '✗') + '</span> ' + name;
                if (result.error) html += '<div style="font-size:11px;color:#f88;margin-top:2px;">' + result.error + '</div>';
                html += '</div>';
            }
            html += '</div>';
            results.innerHTML = html;
        } else { status.textContent = 'Test failed'; status.style.color = '#f55'; }
    } catch(e) { status.textContent = 'Error: ' + e.message; status.style.color = '#f55'; }
}

async function showProposals() {
    try {
        const r = await fetch('/proposals');
        const ct = (r.headers.get('content-type') || '').toLowerCase();
        if (!r.ok || !ct.includes('application/json')) {
            toast('Proposals route is missing (server returned non‑JSON).');
            return;
        }
        const d = await r.json();

        const el = document.getElementById('proposals-content');
        el.innerHTML = '';
        if (d.ok && d.proposals && d.proposals.length) {
            d.proposals.forEach(p => {
                el.innerHTML += `<div class="card">
                  <h4>#${p.id} — ${p.summary}</h4>
                  <p>Status: <strong>${p.status}</strong> | File: ${p.target_file}</p>
                  ${isAdmin && p.status==='pending' ? `<div class="btn-row">
                    <button class="btn-approve" onclick="approveProposal(${p.id})">✓ Approve</button>
                    <button class="btn-reject"  onclick="rejectProposal(${p.id})">✕ Reject</button>
                  </div>` : ''}
                </div>`;
            });
        } else { el.innerHTML = '<p>No proposals.</p>'; }

        document.getElementById('proposals-modal').classList.add('active');
    } catch (e) { toast(e.message); }
}

async function approveProposal(id) {
    if (!confirm('Approve and apply this code change?')) return;
    const r = await fetch(`/proposals/${id}/approve`, {method:'POST'});
    const d = await r.json();
    toast(d.ok ? 'Approved & applied!' : d.error);
    showProposals();
}
async function rejectProposal(id) {
    const r = await fetch(`/proposals/${id}/reject`, {method:'POST'});
    toast('Rejected');
    showProposals();
}

// =====================================================================
// MEMORY PANEL
// =====================================================================
async function showMemory() {
    document.getElementById('memory-modal').classList.add('active');
    await Promise.all([loadMemoryStatus(), loadMemoryPolicy(), loadMemoryFeed()]);
}

async function loadMemoryStatus() {
    try {
        const r = await fetch('/memory/status');
        if (!r.ok) return;
        const d = await r.json();
        if (!d.ok) return;
        document.getElementById('ms-backend').textContent = d.backend || '--';
        document.getElementById('ms-model').textContent = d.embedding_model || '--';
        document.getElementById('ms-collection').textContent = d.collection || '--';
        document.getElementById('ms-count').textContent = d.vector_count ?? '--';
        document.getElementById('ms-lastwrite').textContent = d.last_write_time
            ? new Date(d.last_write_time).toLocaleTimeString() : 'never';
        const statusEl = document.getElementById('ms-status');
        if (d.last_error) {
            statusEl.textContent = 'ERROR';
            statusEl.style.color = '#ff4444';
        } else {
            statusEl.textContent = d.last_write_ok !== false ? 'OK' : 'FAIL';
            statusEl.style.color = d.last_write_ok !== false ? 'var(--secondary)' : '#ff4444';
        }
        const warn = document.getElementById('ms-warning');
        if (d.fallback_warning) {
            warn.textContent = d.fallback_warning;
            warn.style.display = 'block';
        } else {
            warn.style.display = 'none';
        }
    } catch(_) {}
}

async function testMemory() {
    const result = document.getElementById('mem-test-result');
    result.textContent = 'Testing...';
    result.style.color = '#aaa';
    try {
        const r = await fetch('/memory/test', {method:'POST',headers:{'Content-Type':'application/json'}});
        const d = await r.json();
        if (d.ok && d.write && d.read) {
            result.innerHTML = '<span style="color:var(--secondary)">&#10003; Found it!</span> — ' + d.test_text;
        } else if (d.ok && d.write && !d.read) {
            result.innerHTML = '<span style="color:#ffaa00">&#10007; Write OK but read failed</span>';
        } else {
            result.innerHTML = '<span style="color:#ff4444">&#10007; Write failed</span> — ' + (d.error||'');
        }
        await loadMemoryStatus();
    } catch(e) {
        result.innerHTML = '<span style="color:#ff4444">&#10007; Error: ' + e.message + '</span>';
    }
}

async function loadMemoryPolicy() {
    try {
        const r = await fetch('/memory/policy');
        const d = await r.json();
        if (!d.ok) return;
        document.getElementById('pol-facts').checked = !!d.policy.save_facts;
        document.getElementById('pol-decisions').checked = !!d.policy.save_decisions;
        document.getElementById('pol-summaries').checked = !!d.policy.save_summaries;
        document.getElementById('pol-messages').checked = !!d.policy.save_messages;
    } catch(_) {}
}

async function updatePolicy() {
    const policy = {
        save_facts: document.getElementById('pol-facts').checked,
        save_decisions: document.getElementById('pol-decisions').checked,
        save_summaries: document.getElementById('pol-summaries').checked,
        save_messages: document.getElementById('pol-messages').checked,
    };
    try {
        await fetch('/memory/policy', {
            method:'POST', headers:{'Content-Type':'application/json'},
            body: JSON.stringify(policy)
        });
        toast('Memory policy updated');
    } catch(_) {}
}

async function loadMemoryFeed() {
    try {
        const r = await fetch('/memory/feed');
        const d = await r.json();
        const el = document.getElementById('mem-feed');
        if (!d.ok || !d.feed || !d.feed.length) {
            el.innerHTML = '<p style="color:#666;">No memories saved yet.</p>';
            return;
        }
        el.innerHTML = d.feed.map(m => {
            const icon = m.ok ? '<span style="color:var(--secondary)">&#9679;</span>'
                              : '<span style="color:#ff4444">&#9679;</span>';
            const time = m.timestamp ? new Date(m.timestamp).toLocaleTimeString() : '';
            return `<div style="padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.05);">
                ${icon} <strong>${m.type}</strong>
                <span style="color:#888;margin-left:6px;">${m.backend}</span>
                <span style="color:#666;float:right;">${time}</span>
                <div style="color:#aaa;font-size:11px;margin-top:2px;">${m.preview}</div>
            </div>`;
        }).join('');
    } catch(_) {}
}

async function showResearch() {
    try {
        const r = await fetch('/research');
        const ct = (r.headers.get('content-type') || '').toLowerCase();
        if (!r.ok || !ct.includes('application/json')) {
            toast('Research route is missing (server returned non‑JSON).');
            return;
        }
        const d = await r.json();

        const el = document.getElementById('research-content');
        el.innerHTML = '';
        if (d.ok && d.entries && d.entries.length) {
            d.entries.forEach(e => {
                el.innerHTML += `<div class="card">
                  <h4>${e.title}</h4>
                  <p>Category: ${e.category} | ${new Date(e.ts).toLocaleString()}</p>
                  <button onclick="viewResearch(${e.id})">📖 Open</button>
                </div>`;
            });
        } else { el.innerHTML = '<p>No research entries.</p>'; }

        document.getElementById('research-modal').classList.add('active');
    } catch (e) { toast(e.message); }
}

async function viewResearch(id) {
    const r = await fetch(`/research/${id}`);
    const d = await r.json();
    if (d.ok) {
        const el = document.getElementById('research-content');
        el.innerHTML = `<h4>${d.entry.title}</h4><p style="white-space:pre-wrap;font-size:13px;color:rgba(255,255,255,0.8);margin-top:10px">${d.entry.content}</p>`;
    }
}

// =====================================================================
// KEYBOARD
// =====================================================================
document.addEventListener('keydown', e => {
    if (e.key==='Enter' && !e.shiftKey && e.target.id==='message-input') { e.preventDefault(); sendMessage(); }
    if (e.key==='Escape') { document.querySelectorAll('.modal.active').forEach(m=>m.classList.remove('active')); }
});

// =====================================================================
// TOAST
// =====================================================================
let toastTimer = null;
function toast(msg) {
    const el = document.getElementById('toast');
    el.textContent = msg; el.classList.add('show');
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('show'), 3200);
}

// =====================================================================
// FILE ATTACH (any file) — requires backend POST /upload
// =====================================================================
async function handleFileAttach(inputEl) {
    const f = inputEl.files && inputEl.files[0];
    if (!f) return;

    const isImage = f.type && f.type.startsWith('image/');

    // If it's an image, also set currentImage so Joi can SEE it via vision
    if (isImage) {
        const reader = new FileReader();
        reader.onload = e => { currentImage = e.target.result; };
        reader.readAsDataURL(f);
    }

    try {
        const fd = new FormData();
        fd.append('file', f);
        const r = await fetch('/upload', { method: 'POST', body: fd });
        let d = null;
        try { d = await r.json(); } catch(e) {}
        if (!r.ok || !d || !d.ok) {
            const msg = (d && (d.error || d.details)) ? (d.error || d.details) : ('Upload failed (HTTP ' + r.status + ')');
            toast(msg);
            if (isImage) currentImage = null;
            return;
        }
        const link = d.url || '';
        const name = d.filename || f.name;
        const ta = document.getElementById('message-input');
        if (ta) {
            if (isImage) {
                ta.value = (ta.value ? ta.value + '\n' : '') + `[Attached image: ${name}]`;
            } else {
                ta.value = (ta.value ? ta.value + '\n' : '') + `Uploaded file: ${name}\n${link}\n`;
            }
            ta.focus();
        }
        toast(isImage ? 'Image attached — send a message for Joi to see it' : 'Uploaded: ' + name);
    } catch (e) {
        toast(e.message || String(e));
        if (isImage) currentImage = null;
    } finally {
        inputEl.value = '';
    }
}

// Drag & drop anywhere to upload first file
window.addEventListener('dragover', (e) => { e.preventDefault(); });

window.addEventListener('drop', async (e) => {
    e.preventDefault();
    const f = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
    if (!f) return;

    try {
        const fd = new FormData();
        fd.append('file', f);

        const r = await fetch('/upload', { method: 'POST', body: fd });
        let d = null;
        try { d = await r.json(); } catch (err) {}

        if (!r.ok || !d || !d.ok) {
            const msg = (d && (d.error || d.details))
                ? (d.error || d.details)
                : ('Upload failed (HTTP ' + r.status + ')');
            toast(msg);
            return;
        }

        const link = d.url || '';
        const name = d.filename || f.name;
        const ta = document.getElementById('message-input');
        if (ta) {
            ta.value = (ta.value ? ta.value + '\n' : '') + `Uploaded file: ${name}\n${link}\n`;
            ta.focus();
        }
        toast('Uploaded: ' + name);
    } catch (err) {
        toast(err.message || String(err));
    }
});

// Hook up the attach button (change handler is inline on the input element)
document.getElementById('attach-btn').addEventListener('click', () => {
    document.getElementById('file-attach-input').click();
});
