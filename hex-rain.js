/**
 * High-performance Matrix "Digital Rain" canvas background.
 * - 3 layers (parallax: font size + opacity)
 * - Lead: Bright White #FFFFFF + shadowBlur; trail: Electric Green #00FF41 → Deep Forest #003B00
 * - dataQueue: idle = hex + Base64; speaking = UTF-8 bytes of AI text in leading drops; thinking = 3x speed + flicker
 * - requestAnimationFrame, responsive resize without clearing buffer, pointer-events: none, z-index: -1
 */
(function () {
  'use strict';

  const FONT_FAMILY = '"JetBrains Mono", "Fira Code", "Consolas", monospace';
  const LEAD_COLOR = '#FFFFFF';
  const TRAIL_START = '#00FF41';   // Electric Green
  const TRAIL_END = '#003B00';     // Deep Forest Green
  const GLOW_BLUR = 18;
  const IDLE_SPEED = 1.0;
  const THINKING_SPEED_MULT = 3;
  const SPEAKING_SPEED = 1.4;

  const IDLE_CHARS = '0123456789ABCDEF+/=';
  const LAYERS = [
    { fontPx: 10, opacity: 0.22, speedMul: 0.55, colWidth: 22, dropsPerCol: 22 },
    { fontPx: 14, opacity: 0.5,  speedMul: 1,   colWidth: 26, dropsPerCol: 18 },
    { fontPx: 18, opacity: 0.88, speedMul: 1.35, colWidth: 32, dropsPerCol: 14 }
  ];

  let canvas, ctx, layers = [], dataQueue = [], mode = 'idle';
  let rafId = null, w = 0, h = 0, dpr = 1;
  let lastResizeW = 0, lastResizeH = 0;
  let flickerPhase = 0;

  const encoder = typeof TextEncoder !== 'undefined' ? new TextEncoder() : null;

  function textToUtf8Bytes(text) {
    if (!encoder) {
      const out = [];
      for (let i = 0; i < text.length; i++) out.push(text.charCodeAt(i) & 0xff);
      return out;
    }
    return Array.from(encoder.encode(text));
  }

  function randomIdleChar() {
    return IDLE_CHARS[Math.floor(Math.random() * IDLE_CHARS.length)];
  }

  function byteToHex(byte) {
    return (byte & 0xff).toString(16).toUpperCase().padStart(2, '0');
  }

  function nextCharForLead() {
    if (mode === 'speaking' && dataQueue.length > 0) return byteToHex(dataQueue.shift());
    return randomIdleChar();
  }

  function buildColumn(layer, x) {
    const drops = [];
    let y = Math.random() * -h * 1.5;
    for (let i = 0; i < layer.dropsPerCol; i++) {
      drops.push({ y, char: randomIdleChar() });
      y -= layer.charHeight * 0.92;
    }
    return { x, drops };
  }

  function initLayer(layer, index) {
    const charHeight = Math.round(layer.fontPx * 1.35);
    const colWidth = layer.colWidth;
    const n = Math.max(6, Math.ceil(w / colWidth) + 2);
    const columns = [];
    for (let i = 0; i < n; i++) columns.push(buildColumn({ ...layer, charHeight }, i * colWidth + (index * 3 % 5)));
    return { ...layer, index, charHeight, columns };
  }

  function ensureLayers() {
    if (layers.length === 0) {
      LAYERS.forEach((l, i) => layers.push(initLayer(l, i)));
    }
    const colCount = Math.max(8, Math.ceil(w / 24));
    layers.forEach((layer, li) => {
      const colWidth = layer.colWidth;
      const need = Math.max(6, Math.ceil(w / colWidth) + 2);
      if (layer.columns.length < need) {
        const charHeight = layer.charHeight;
        while (layer.columns.length < need) {
          const x = layer.columns.length * colWidth + (li * 3 % 5);
          layer.columns.push(buildColumn({ ...layer, charHeight }, x));
        }
      } else if (layer.columns.length > need + 2) {
        layer.columns.length = need + 1;
      }
      layer.columns.forEach((col, ci) => {
        col.x = ci * colWidth + (li * 3 % 5);
      });
    });
  }

  function parseHex(hex) {
    const s = String(hex).replace('#', '');
    if (s.length !== 6) return [0, 255, 65];
    const r = parseInt(s.slice(0, 2), 16);
    const g = parseInt(s.slice(2, 4), 16);
    const b = parseInt(s.slice(4, 6), 16);
    return isNaN(r) ? [0, 255, 65] : [r, g, b];
  }

  function lerpColor(t) {
    const [r1, g1, b1] = parseHex(TRAIL_START);
    const [r2, g2, b2] = parseHex(TRAIL_END);
    const r = Math.round(r1 + (r2 - r1) * t);
    const g = Math.round(g1 + (g2 - g1) * t);
    const b = Math.round(b1 + (b2 - b1) * t);
    return `rgb(${r},${g},${b})`;
  }

  function tick() {
    if (!ctx || !canvas) return;
    flickerPhase++;

    const baseSpeed = mode === 'thinking' ? IDLE_SPEED * THINKING_SPEED_MULT : (mode === 'speaking' ? SPEAKING_SPEED : IDLE_SPEED);
    const flicker = mode === 'thinking';

    ctx.fillStyle = 'rgba(0, 10, 0, 0.11)';
    ctx.fillRect(0, 0, w, h);

    layers.forEach(layer => {
      const speed = baseSpeed * layer.speedMul;
      const font = `${layer.fontPx}px ${FONT_FAMILY}`;
      ctx.font = font;
      ctx.textBaseline = 'top';

      layer.columns.forEach((col, colIndex) => {
        col.drops.forEach((drop) => {
          drop.y += speed;
          if (drop.y > h + layer.charHeight * 2) {
            drop.y = -layer.charHeight * 2;
            drop.char = nextCharForLead();
          }
        });

        const visible = col.drops.filter(d => d.y > -layer.charHeight && d.y < h + layer.charHeight);
        if (visible.length === 0) return;
        const sorted = [...visible].sort((a, b) => a.y - b.y);
        const lead = sorted[0];

        col.drops.forEach((drop) => {
          if (drop.y < -layer.charHeight || drop.y > h + layer.charHeight) return;
          const isLead = drop === lead;
          let alpha = layer.opacity;
          if (flicker && !isLead) {
            const seed = (drop.y * 7 + colIndex * 13 + flickerPhase) % 31;
            alpha = seed < 12 ? layer.opacity * 0.4 : layer.opacity;
          }
          if (isLead) {
            ctx.shadowColor = LEAD_COLOR;
            ctx.shadowBlur = GLOW_BLUR;
            ctx.fillStyle = LEAD_COLOR;
          } else {
            ctx.shadowBlur = 0;
            const t = Math.min(1, (drop.y + layer.charHeight) / (h * 0.5));
            ctx.fillStyle = lerpColor(t);
            ctx.globalAlpha = alpha;
          }
          ctx.fillText(drop.char, col.x, drop.y);
          ctx.globalAlpha = 1;
        });
        ctx.shadowBlur = 0;
      });
    });

    rafId = requestAnimationFrame(tick);
  }

  function resize() {
    if (!canvas) return;
    const cw = canvas.clientWidth;
    const ch = canvas.clientHeight;
    dpr = Math.min(2, window.devicePixelRatio || 1);
    const needResize = (w !== cw || h !== ch);
    w = cw;
    h = ch;

    if (canvas.width !== w * dpr || canvas.height !== h * dpr) {
      const scale = ctx.getTransform?.().a ?? 1;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      canvas.style.width = w + 'px';
      canvas.style.height = h + 'px';
      if (scale !== 1) ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.scale(dpr, dpr);
    }

    if (needResize && w > 0 && h > 0) {
      ensureLayers();
      layers.forEach((layer, i) => {
        const base = LAYERS[i];
        const charHeight = Math.round(base.fontPx * 1.35);
        const need = Math.max(6, Math.ceil(w / base.colWidth) + 2);
        if (layer.columns.length !== need) {
          layer.columns = [];
          for (let j = 0; j < need; j++) {
            layer.columns.push(buildColumn({ ...base, charHeight, index: i }, j * base.colWidth + (i * 3 % 5)));
          }
        } else {
          layer.columns.forEach((col, j) => {
            col.x = j * base.colWidth + (i * 3 % 5);
          });
        }
        layer.charHeight = charHeight;
      });
    }
    lastResizeW = w;
    lastResizeH = h;
  }

  function start() {
    if (!canvas || !ctx) return;
    resize();
    if (!rafId) rafId = requestAnimationFrame(tick);
  }

  function stop() {
    if (rafId) cancelAnimationFrame(rafId);
    rafId = null;
  }

  const api = {
    setMode(m) { mode = (m === 'idle' || m === 'thinking' || m === 'speaking') ? m : 'idle'; },
    injectText(text) {
      if (typeof text !== 'string') return;
      dataQueue.push(...textToUtf8Bytes(text));
    },
    dataQueue: {
      push(str) { if (typeof str === 'string') dataQueue.push(...textToUtf8Bytes(str)); },
      clear() { dataQueue.length = 0; },
      get length() { return dataQueue.length; }
    },
    start,
    stop,
    resize
  };

  function mount() {
    const wrap = document.getElementById('hex-rain-bg');
    if (!wrap) return;
    canvas = document.createElement('canvas');
    canvas.setAttribute('aria-hidden', 'true');
    wrap.appendChild(canvas);
    ctx = canvas.getContext('2d');
    window.addEventListener('resize', resize);
    start();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }

  window.hexRain = api;
})();
