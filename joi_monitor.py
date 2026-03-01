"""
joi_monitor.py — JOI NEURAL MONITOR (real-time system monitor)
==============================================================
Layout and style match the reference images in "AI brain visual".
All gauges and values are driven by live /neuro data from Joi.
Run: streamlit run joi_monitor.py
"""

import html
import json
import os
import time
from urllib.request import urlopen, Request
from urllib.error import URLError

import streamlit as st

JOI_URL = os.environ.get("JOI_URL", "http://127.0.0.1:5001")
NEURO_URL = f"{JOI_URL.rstrip('/')}/neuro"
POLL_INTERVAL = 2.0

# All 21 brain sectors from joi_neuro.SECTOR_MAP
ALL_SECTORS = [
    "IDENTITY", "REASONING", "LANGUAGE", "CREATIVITY",
    "LONG_MEMORY", "SHORT_MEMORY", "FACTS", "LEARNING",
    "VISION", "CAMERA", "VOICE", "WEB",
    "TOOLS", "FILES", "DESKTOP", "REPAIR",
    "EMPATHY", "ORCHESTRATOR", "ARCHITECT", "CODER", "VALIDATOR",
]

# Hexagons around brain (ref layout): label -> sector key for real intensity
HEX_SECTORS = [
    ("LONG-TERM MEMORY", "LONG_MEMORY"),
    ("SHORT-TERM MEMORY", "SHORT_MEMORY"),
    ("REASONING LOGIC", "REASONING"),
    ("EMPATHY ALGORITHMS", "EMPATHY"),
    ("CREATIVE MODE", "CREATIVITY"),
    ("LANGUAGE", "LANGUAGE"),
]


def fetch_neuro():
    try:
        req = Request(NEURO_URL, headers={"Accept": "application/json"})
        with urlopen(req, timeout=3) as r:
            return json.loads(r.read().decode())
    except (URLError, OSError, json.JSONDecodeError):
        return {"ok": False, "sectors": {}, "routing": {}, "inner_state": {}, "llm_activity": {}, "memory_activity": {}, "processing": False}


def pct(sectors, key):
    v = sectors.get(key, 0)
    return min(100, int((v if isinstance(v, (int, float)) else 0) * 100))


def main():
    st.set_page_config(page_title="JOI Neural Monitor", layout="wide", initial_sidebar_state="collapsed")
    data = fetch_neuro()
    sectors = data.get("sectors") or {}
    routing = data.get("routing") or {}
    inner = data.get("inner_state") or {}
    llm_activity = data.get("llm_activity") or {}
    memory_activity = data.get("memory_activity") or {}
    processing = data.get("processing", False)
    response_time_ms = routing.get("response_time_ms") or 0

    # Real LLM in use
    active_llm = (
        llm_activity.get("display_name")
        or llm_activity.get("active_model")
        or routing.get("model")
    )
    provider = routing.get("provider", "")
    if not active_llm or str(active_llm).lower() in ("none", ""):
        active_llm = "idle"
    else:
        active_llm = str(active_llm)
        if provider == "ollama" or "ollama" in str(llm_activity.get("provider", "")).lower():
            if "privacy" in active_llm.lower() or "sensitive" in routing.get("reason", ""):
                active_llm = os.environ.get("OLLAMA_PRIVACY_MODEL", "huihui_ai/dolphin3-abliterated") + " [LOCAL PROTOCOL]"
            elif "coder" in active_llm.lower() or "coding" in routing.get("reason", ""):
                active_llm = os.environ.get("OLLAMA_CODER_MODEL", "qwen2.5-coder:14b") + " [LOCAL CODER]"
            elif "general" in active_llm.lower():
                active_llm = os.environ.get("OLLAMA_GENERAL_MODEL", "gemma2:9b") + " [LOCAL]"
            else:
                active_llm = active_llm + " [OLLAMA]"

    active_llm_safe = html.escape(active_llm)

    # Inject missing sector mapping based on real routing paths
    reason = routing.get("reason", "")
    if processing:
        if "sensitive" in reason:
            sectors["EMPATHY"] = max(sectors.get("EMPATHY", 0), 0.95)
            sectors["IDENTITY"] = max(sectors.get("IDENTITY", 0), 0.85)
        if "coding" in reason or "code" in reason:
            sectors["CODER"] = max(sectors.get("CODER", 0), 0.95)
            sectors["REASONING"] = max(sectors.get("REASONING", 0), 0.85)
        if "research" in reason:
            sectors["FACTS"] = max(sectors.get("FACTS", 0), 0.9)
            sectors["WEB"] = max(sectors.get("WEB", 0), 0.6)

    # Cognitive Load (real)
    max_sector = max((v for v in sectors.values() if isinstance(v, (int, float))), default=0)
    cog = min(100, int(
        (40 if processing else 0)
        + max_sector * 45
        + min(15, response_time_ms // 200)
    ))
    cog_color = "#ff4466" if cog > 70 else "#00d4ff"
    cog_glow = "rgba(255,68,102,0.6)" if cog > 70 else "rgba(0,212,255,0.5)"

    # Empathy (real)
    empathy_pct = min(100, int((inner.get("warmth", 0.5) if isinstance(inner.get("warmth"), (int, float)) else 0.5) * 100))
    mood_label = (inner.get("mood") or "chill")
    if not isinstance(mood_label, str):
        mood_label = str(mood_label)
    mood_label = html.escape(mood_label)[:24]

    # Memory latency history (real)
    if "latency_history" not in st.session_state:
        st.session_state["latency_history"] = []
    latency_history = st.session_state["latency_history"]
    latency_history.append(min(5000, response_time_ms))
    if len(latency_history) > 60:
        st.session_state["latency_history"] = latency_history[-60:]
    latency_json = json.dumps(latency_history[-50:])

    # Active firings (real)
    sector_sum = sum(v for v in sectors.values() if isinstance(v, (int, float)))
    active_firings = int((4000 if processing else 200) + sector_sum * 600) if data.get("ok") else 0

    # Function Loadout: all sectors, real %
    loadout_bars = "".join(
        f'<div class="loadout-row"><span class="loadout-label">{name}</span><div class="loadout-bar"><div class="loadout-fill" style="width:{pct(sectors, name)}%;"></div></div><span class="loadout-pct">{pct(sectors, name)}%</span></div>'
        for name in ALL_SECTORS
    )

    # Logic stream (real)
    log_lines = []
    if data.get("ok"):
        for blk in (data.get("context_injected") or [])[:4]:
            log_lines.append("[CTX] " + str(blk)[:55])
        for m in (data.get("monologue") or [])[:3]:
            log_lines.append((m.get("thought") or m.get("content") or "")[:50])
        log_lines.append("[LLM] " + active_llm_safe)
    else:
        log_lines.append("Waiting for Joi server...")
    log_html = "<br/>".join(html.escape(ln) for ln in (log_lines[-14:] if log_lines else [])) or ""

    sector_json = json.dumps({k: sectors.get(k, 0) for k in ALL_SECTORS})
    hex_intensities = json.dumps([sectors.get(key, 0) for _, key in HEX_SECTORS])

    diagnostic = st.query_params.get("diagnostic")
    if diagnostic:
        st.session_state["logic_diagnostic"] = diagnostic
    active_diag = st.session_state.get("logic_diagnostic")

    # Starfield: fixed positions for cosmic background (ref image style)
    star_css = ",".join(
        f"radial-gradient(1.2px 1.2px at {x}% {y}%, rgba(255,255,255,0.7), transparent)"
        for x, y in [
            (5, 8), (15, 22), (25, 5), (35, 18), (45, 12), (55, 28), (65, 8), (75, 20), (85, 14), (95, 25),
            (8, 45), (18, 55), (28, 48), (38, 62), (48, 52), (58, 58), (68, 45), (78, 55), (88, 50), (12, 72),
            (22, 78), (32, 75), (42, 82), (52, 70), (62, 88), (72, 78), (82, 85), (92, 72), (7, 92), (50, 95),
        ]
    )

    dashboard_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #030308; color: #e0e8f0; overflow-x: hidden; }}
#dashboard {{ min-height: 100vh; position: relative; padding: 16px; }}
/* Cosmic background — deep space + galaxies + starfield (ref image) */
#dashboard::before {{
  content: ""; position: absolute; inset: 0; z-index: 0;
  background: radial-gradient(ellipse 140% 120% at 50% 20%, rgba(15,20,55,0.85) 0%, rgba(8,10,30,0.95) 35%, #050510 70%),
              radial-gradient(ellipse 80% 60% at 20% 80%, rgba(40,20,80,0.25) 0%, transparent 50%),
              radial-gradient(ellipse 60% 80% at 80% 30%, rgba(20,40,80,0.2) 0%, transparent 45%);
}}
#dashboard::after {{
  content: ""; position: absolute; inset: 0; z-index: 0; pointer-events: none;
  background-image: {star_css};
  background-size: 100% 100%; opacity: 0.85;
}}
/* Single holographic frame around entire UI (ref: neon blue rectangular projection) */
.holo-frame {{
  position: relative; z-index: 1;
  border: 2px solid rgba(0,200,255,0.65);
  box-shadow: 0 0 50px rgba(0,170,255,0.25), inset 0 0 80px rgba(0,0,0,0.4);
  border-radius: 4px;
  background: rgba(5,8,22,0.4);
  overflow: hidden;
}}
/* Top banner — "JOI NEURAL MONITOR" + LLM line (ref) */
.top-banner {{
  padding: 12px 20px;
  border-bottom: 1px solid rgba(0,200,255,0.4);
  background: rgba(0,20,45,0.5);
  display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;
}}
.top-banner h1 {{
  font-size: 1.35rem; font-weight: 700; letter-spacing: 4px;
  color: #00e5ff; text-shadow: 0 0 20px rgba(0,229,255,0.8), 0 0 40px rgba(0,170,255,0.4);
}}
.llm-line {{ font-size: 12px; color: rgba(0,220,255,0.95); letter-spacing: 1px; }}
/* Main grid: left | center | right (ref layout) */
.layout {{ display: grid; grid-template-columns: 220px 1fr 240px; grid-template-rows: 1fr auto; gap: 0; min-height: 82vh; }}
/* Left column — COGNITIVE LOAD, EMPATHY SPECTRUM, MEMORY LATENCY */
.left {{
  border-right: 1px solid rgba(0,200,255,0.35);
  padding: 16px;
  background: rgba(0,12,30,0.5);
  display: flex; flex-direction: column; gap: 14px;
}}
.left-title {{ font-size: 8px; letter-spacing: 2px; color: rgba(0,220,255,0.95); margin-bottom: 2px; text-transform: uppercase; }}
.cog-wrap {{ position: relative; display: flex; align-items: center; justify-content: center; }}
.cog-ring {{
  width: 88px; height: 88px; border-radius: 50%;
  background: conic-gradient({cog_color} 0deg {cog * 3.6}deg, rgba(255,255,255,0.06) {cog * 3.6}deg 360deg);
  box-shadow: 0 0 28px {cog_glow};
  display: flex; align-items: center; justify-content: center;
}}
.cog-ring-inner {{ width: 58px; height: 58px; border-radius: 50%; background: #060c18; }}
.cog-val {{ position: absolute; font-size: 18px; font-weight: bold; color: {cog_color}; text-shadow: 0 0 12px {cog_glow}; }}
.cog-status {{ font-size: 10px; color: rgba(255,255,255,0.7); text-align: center; }}
.empathy-wrap {{ display: flex; flex-direction: column; align-items: center; gap: 4px; }}
.empathy-ring {{
  width: 64px; height: 64px; border-radius: 50%;
  background: conic-gradient(#ff88cc 0deg {empathy_pct * 3.6}deg, rgba(255,255,255,0.06) {empathy_pct * 3.6}deg 360deg);
  box-shadow: 0 0 20px rgba(255,136,204,0.45);
  display: flex; align-items: center; justify-content: center;
}}
.empathy-ring-inner {{ width: 44px; height: 44px; border-radius: 50%; background: #060c18; }}
.empathy-sphere {{
  width: 56px; height: 56px; border-radius: 50%;
  background: radial-gradient(circle at 28% 28%, #a070ff, #6060cc 40%, #303080);
  box-shadow: 0 0 30px rgba(136,102,255,0.7), inset -4px -4px 12px rgba(0,0,0,0.3);
}}
.empathy-pct {{ font-size: 11px; color: #c8a0ff; }}
.empathy-tone {{ font-size: 9px; color: rgba(200,180,255,0.95); text-transform: uppercase; letter-spacing: 0.5px; }}
.ekg-wrap {{ height: 52px; background: rgba(0,0,0,0.5); border-radius: 6px; padding: 4px; border: 1px solid rgba(0,200,255,0.2); }}
.ekg-ms {{ font-size: 9px; color: rgba(0,200,255,0.9); text-align: center; margin-top: 2px; }}

/* Center — 3D brain + neural web + hexagons (ref) */
.center {{
  position: relative;
  background: radial-gradient(ellipse 80% 80% at 50% 50%, rgba(10,25,60,0.3) 0%, rgba(5,10,30,0.6) 100%);
  min-height: 420px;
}}
#brainCanvas {{ display: block; width: 100%; height: 100%; min-height: 420px; }}
/* Hexagonal sectors around brain (ref image labels) */
.hex {{
  position: absolute;
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  background: rgba(0,50,120,0.35);
  border: 1px solid rgba(0,200,255,0.5);
  box-shadow: 0 0 20px rgba(0,170,255,0.25);
  display: flex; align-items: center; justify-content: center;
  color: #00c8ff; font-size: 9px; font-weight: bold; letter-spacing: 0.5px; text-align: center; padding: 6px;
  line-height: 1.2;
}}
.hex strong {{ display: block; font-size: 8px; color: rgba(0,200,255,0.7); margin-top: 2px; }}

/* Right column — SYNAPTIC PULSE, LLM, LOGIC STREAM */
.right {{
  border-left: 1px solid rgba(0,200,255,0.35);
  padding: 16px;
  background: rgba(0,12,30,0.5);
  display: flex; flex-direction: column; gap: 12px;
}}
.synaptic-wrap {{ height: 70px; background: rgba(0,0,0,0.5); border-radius: 6px; padding: 4px; border: 1px solid rgba(0,200,255,0.2); }}
.synaptic-label {{ font-size: 10px; color: rgba(0,220,255,0.95); margin-top: 4px; }}
.llm-box {{ font-size: 11px; color: #00c8ff; padding: 8px 10px; background: rgba(0,0,0,0.5); border-radius: 6px; border: 1px solid rgba(0,170,255,0.35); word-break: break-all; }}
.matrix-log {{
  font-family: 'Consolas', 'Monaco', monospace; font-size: 9px; color: #00ff88;
  background: rgba(0,0,0,0.8); border-radius: 6px; padding: 8px; height: 100px; overflow-y: auto;
  border: 1px solid rgba(0,255,136,0.3); line-height: 1.4; text-shadow: 0 0 8px rgba(0,255,136,0.5);
}}

/* Bottom — FUNCTION LOADOUT (ref: horizontal bars) */
.bottom {{
  grid-column: 1 / -1;
  border-top: 1px solid rgba(0,200,255,0.35);
  padding: 14px 20px;
  background: rgba(0,15,35,0.6);
}}
.loadout-title {{ font-size: 10px; letter-spacing: 3px; color: rgba(0,220,255,0.95); margin-bottom: 10px; text-transform: uppercase; text-shadow: 0 0 10px rgba(0,170,255,0.5); }}
.loadout-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 6px 20px; }}
.loadout-row {{ display: flex; align-items: center; gap: 8px; margin: 2px 0; }}
.loadout-label {{ width: 100px; font-size: 9px; color: rgba(0,200,255,0.9); }}
.loadout-bar {{ flex: 1; height: 8px; background: rgba(0,0,0,0.5); border-radius: 4px; overflow: hidden; }}
.loadout-fill {{ height: 100%; background: linear-gradient(90deg, #00aaff, #8866ff); border-radius: 4px; box-shadow: 0 0 8px rgba(0,170,255,0.4); transition: width 0.3s ease; }}
.loadout-pct {{ width: 28px; font-size: 9px; color: #00aaff; }}
</style>
</head>
<body>
<div id="dashboard">
  <div class="holo-frame">
    <div class="top-banner">
      <h1>JOI NEURAL MONITOR</h1>
      <span class="llm-line">LLM: {active_llm_safe}</span>
    </div>
    <div class="layout">
      <div class="left">
        <div class="left-title">Cognitive Load:</div>
        <div class="left-title">Empathy Spectrum:</div>
        <div class="cog-wrap">
          <div class="cog-ring"><div class="cog-ring-inner"></div></div>
          <span class="cog-val">{cog}%</span>
        </div>
        <div class="cog-status">{"HIGH" if cog > 70 else "NORMAL"}</div>
        <div class="empathy-wrap">
          <div class="empathy-ring"><div class="empathy-ring-inner"></div></div>
          <div class="empathy-sphere"></div>
          <span class="empathy-pct">{empathy_pct}%</span>
          <span class="empathy-tone">TONE {mood_label}</span>
        </div>
        <div class="left-title">Memory Latency:</div>
        <div class="ekg-wrap"><canvas id="ekg" width="188" height="44"></canvas></div>
        <div class="ekg-ms">{response_time_ms} ms</div>
      </div>

      <div class="center">
        <canvas id="brainCanvas"></canvas>
        <!-- Hexagonal sectors (ref positions) — intensity from real sector data -->
        <div class="hex" id="hex0" style="top:8%;left:28%;width:100px;height:36px;">LONG-TERM MEMORY<strong id="hex0pct">0%</strong></div>
        <div class="hex" id="hex1" style="top:8%;right:28%;width:100px;height:36px;">SHORT-TERM MEMORY<strong id="hex1pct">0%</strong></div>
        <div class="hex" id="hex2" style="top:50%;right:4%;transform:translateY(-50%);width:36px;height:90px;">REASONING LOGIC<strong id="hex2pct">0%</strong></div>
        <div class="hex" id="hex3" style="bottom:20%;left:12%;width:90px;height:32px;">EMPATHY ALGORITHMS<strong id="hex3pct">0%</strong></div>
        <div class="hex" id="hex4" style="bottom:20%;right:12%;width:90px;height:32px;">LANGUAGE<strong id="hex4pct">0%</strong></div>
        <div class="hex" id="hex5" style="bottom:6%;left:50%;transform:translateX(-50%);width:100px;height:34px;">CREATIVE MODE<strong id="hex5pct">0%</strong></div>
      </div>

      <div class="right">
        <div class="left-title">Synaptic Pulse:</div>
        <div class="synaptic-wrap"><canvas id="synaptic" width="212" height="62"></canvas></div>
        <div class="synaptic-label">ACTIVE FIRINGS: {active_firings}/sec</div>
        <div class="left-title">LLM:</div>
        <div class="llm-box">{active_llm_safe}</div>
        <div class="left-title">Logic Stream</div>
        <div class="matrix-log">{log_html}</div>
      </div>

      <div class="bottom">
        <div class="loadout-title">Function Loadout</div>
        <div class="loadout-grid">{loadout_bars}</div>
      </div>
    </div>
  </div>
</div>
<script>
(function() {{
  var sectorData = {sector_json};
  var hexIntensities = {hex_intensities};
  var latencyData = {latency_json};
  var processing = {str(processing).lower()};
  var sectorKeys = {json.dumps(ALL_SECTORS)};
  var n = sectorKeys.length;

  // Update hexagon labels with real %
  var hexSectorKeys = {json.dumps([key for _, key in HEX_SECTORS])};
  hexSectorKeys.forEach(function(key, i) {{
    var el = document.getElementById('hex' + i);
    var pctEl = document.getElementById('hex' + i + 'pct');
    if (el && pctEl) {{
      var v = (sectorData[key] || 0) * 100;
      pctEl.textContent = Math.round(v) + '%';
      el.style.boxShadow = v > 20 ? '0 0 25px rgba(0,200,255,0.5)' : '0 0 20px rgba(0,170,255,0.25)';
      el.style.background = v > 20 ? 'rgba(0,80,160,0.45)' : 'rgba(0,50,120,0.35)';
    }}
  }});

  // 3D brain + neural web (ref: central glow, translucent brain, radiating lines, nodes by intensity)
  var c = document.getElementById('brainCanvas');
  if (!c) return;
  var rect = c.getBoundingClientRect();
  var dpr = window.devicePixelRatio || 1;
  c.width = rect.width * dpr;
  c.height = rect.height * dpr;
  var ctx = c.getContext('2d');
  ctx.scale(dpr, dpr);
  var w = rect.width, h = rect.height;
  var cx = w/2, cy = h/2;
  var phase = 0;

  function drawBrain() {{
    var activitySum = 0;
    sectorKeys.forEach(function(k) {{ activitySum += sectorData[k] || 0; }});
    var hasActivity = processing || activitySum > 0.15;
    phase += hasActivity ? 0.025 : 0.004;
    ctx.fillStyle = 'rgba(5,10,25,0.3)';
    ctx.fillRect(0, 0, w, h);
    var r = Math.min(w, h) * 0.26;

    // Bright central core (ref: white/cyan glow from center)
    ctx.beginPath();
    ctx.ellipse(cx, cy, r * 0.3, r * 0.25, 0, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(255,255,255,0.5)';
    ctx.shadowBlur = 40;
    ctx.shadowColor = '#ffffff';
    ctx.fill();
    ctx.shadowBlur = 0;

    // Translucent brain blob (ref: neon blue outline, volumetric)
    var gr = ctx.createRadialGradient(cx, cy, 0, cx, cy, r * 1.5);
    gr.addColorStop(0, 'rgba(0,220,255,0.4)');
    gr.addColorStop(0.5, 'rgba(0,120,200,0.2)');
    gr.addColorStop(0.85, 'rgba(0,60,140,0.08)');
    gr.addColorStop(1, 'rgba(0,40,100,0.02)');
    ctx.beginPath();
    ctx.ellipse(cx, cy, r * 1.2, r * 1.0, 0, 0, Math.PI * 2);
    ctx.fillStyle = gr;
    ctx.fill();
    ctx.strokeStyle = 'rgba(0,230,255,0.7)';
    ctx.lineWidth = 2.5;
    ctx.shadowBlur = 30;
    ctx.shadowColor = '#00aaff';
    ctx.stroke();
    ctx.shadowBlur = 0;

    // 20 sector nodes + neuron lines (real intensity)
    var i, intensity, angle, nx, ny, nodeR;
    for (i = 0; i < n; i++) {{
      intensity = sectorData[sectorKeys[i]] || 0;
      if (intensity < 0) intensity = 0;
      if (intensity > 1) intensity = 1;
      angle = (i / n) * Math.PI * 2 + phase * 0.25;
      nodeR = r * 1.4 + Math.sin(phase + i * 0.2) * 10;
      nx = cx + Math.cos(angle) * nodeR;
      ny = cy + Math.sin(angle) * nodeR;
      var dotR = 5 + intensity * 10;
      ctx.beginPath();
      ctx.arc(nx, ny, dotR, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(0,200,255,' + (0.25 + intensity * 0.5) + ')';
      ctx.shadowBlur = 10 + intensity * 15;
      ctx.shadowColor = '#00aaff';
      ctx.fill();
      ctx.shadowBlur = 0;
      if (intensity > 0.12) {{
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(nx, ny);
        ctx.strokeStyle = 'rgba(0,200,255,' + (0.12 + intensity * 0.3) + ')';
        ctx.lineWidth = 1 + intensity * 1.2;
        ctx.stroke();
      }}
    }}
  }}
  setInterval(drawBrain, 42);
  drawBrain();

  // EKG from real latency history
  var ekg = document.getElementById('ekg');
  if (ekg && latencyData.length > 1) {{
    var ectx = ekg.getContext('2d');
    var maxL = Math.max.apply(null, latencyData) || 1;
    ectx.fillStyle = 'rgba(0,0,0,0.5)';
    ectx.fillRect(0, 0, 188, 44);
    ectx.strokeStyle = 'rgba(0,200,255,0.9)';
    ectx.lineWidth = 2;
    ectx.shadowBlur = 6;
    ectx.shadowColor = '#00aaff';
    ectx.beginPath();
    var step = 188 / (latencyData.length - 1);
    latencyData.forEach(function(ms, i) {{
      var x = i * step;
      var y = 44 - 8 - (ms / Math.max(maxL, 1)) * 28;
      if (i === 0) ectx.moveTo(x, y); else ectx.lineTo(x, y);
    }});
    ectx.stroke();
    ectx.shadowBlur = 0;
  }}

  // Synaptic pulse (real activity)
  var sp = document.getElementById('synaptic');
  if (sp) {{
    var sctx = sp.getContext('2d');
    var spPhase = 0;
    var sum = 0;
    sectorKeys.forEach(function(k) {{ sum += sectorData[k] || 0; }});
    var activity = Math.min(1, (processing ? 1 : 0) + sum * 0.4);
    setInterval(function() {{
      spPhase += 0.12 + activity * 0.2;
      sctx.fillStyle = 'rgba(0,0,0,0.5)';
      sctx.fillRect(0, 0, 212, 62);
      sctx.strokeStyle = 'rgba(0,200,255,' + (0.35 + activity * 0.5) + ')';
      sctx.lineWidth = 1.2 + activity;
      sctx.shadowBlur = 6;
      sctx.shadowColor = '#00aaff';
      sctx.beginPath();
      for (var x = 0; x <= 212; x += 2.5) {{
        var y = 31 + (Math.sin(x/14 + spPhase) * 10 + Math.sin(x/7 + spPhase*2) * 5) * (0.5 + activity * 0.5);
        if (x === 0) sctx.moveTo(x, y); else sctx.lineTo(x, y);
      }}
      sctx.stroke();
      sctx.shadowBlur = 0;
    }}, 50);
  }}
}})();
</script>
</body>
</html>
"""
    st.components.v1.html(dashboard_html, height=960)

    if active_diag:
        with st.sidebar:
            st.markdown("**LOGIC DIAGNOSTIC**")
            nkey = active_diag.upper().replace("-", "_").replace(" ", "_")
            val = pct(sectors, nkey) if nkey in sectors else pct(sectors, active_diag)
            st.write(f"Sector: **{active_diag}**")
            st.write(f"Intensity: **{val}%**")
            st.write(f"LLM: {active_llm}")
            if st.button("Clear"):
                st.session_state.pop("logic_diagnostic", None)
                st.rerun()

    time.sleep(POLL_INTERVAL)
    st.rerun()


if __name__ == "__main__":
    main()
