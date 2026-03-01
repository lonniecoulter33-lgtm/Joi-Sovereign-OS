# PATCH NOTES — Sidebar UX + Avatar Studio v0

## Date: 2026-02-10

---

## NEW FILES CREATED

| File | Purpose |
|------|---------|
| `modules/cloud_r2_client.py` | Cloudflare R2 storage client (boto3 S3-compatible). Upload/download/list/health. **No longer used by Avatar Studio** (kept for other potential uses). |
| `modules/avatar_studio_api.py` | Flask API: `/api/avatar_studio/upload_photos`, `list_versions`, `health`. All R2 ops via Modal. |
| `modules/modal_worker_client.py` | Modal function client. Calls deployed Modal functions via `modal.Function.lookup()`. |
| `cloud_workers/__init__.py` | Package init for cloud_workers directory. |
| `cloud_workers/avatar_studio/__init__.py` | Package init for avatar_studio sub-package. |
| `cloud_workers/avatar_studio/modal_avatar_generate.py` | Modal serverless workers: `avatar_upload_photos`, `r2_health_check`, `r2_list_versions`, `generate_avatar`. All R2 access runs inside Modal. |
| `avatar_studio.html` | Avatar Studio v0 UI — upload 3 photos, list versions, health check. |
| `tools/test_r2_avatar_upload.py` | End-to-end test via Flask endpoints (no local R2 credentials needed). |
| `docs/AVATAR_STUDIO_V0.md` | Documentation for Avatar Studio v0. |
| `PATCH_NOTES.md` | This file. |

## EXISTING FILES MODIFIED

### `joi_ui.html`

**Changes:**

1. **Header simplified** (was line ~365–383):
   - Removed all `header-controls` nav buttons (Projects, History, Proposals, Research, Memory, Diagnostics, Settings, Logout)
   - Added hamburger button `☰` (toggleSidebar) + status dot
   - Voice credits div preserved

2. **Sidebar HTML added** (after header, before content-wrapper):
   - `#sidebar-overlay` — click-outside-to-close overlay
   - `#main-sidebar` with 4 sections:
     1. **Quick Status**: model, cloud mode, presence with green/yellow/red dots
     2. **Cloud Controls**: Modal spend meter, paid extension meter (hidden), toggles, budget banner, action buttons
     3. **Navigation**: Projects, History, Proposals, Research, Memory, Diagnostics, Avatar Studio, Settings, Logout
     4. **Avatar/Identity**: avatar thumbnail, voice label, Open Avatar Studio + Change avatar buttons

3. **Sidebar CSS added** (before MODALS section):
   - `#main-sidebar` — fixed left drawer, 280px, transform slide
   - `#sidebar-overlay` — semi-transparent backdrop
   - All section styles: `.sb-section`, `.sb-status-row`, `.sb-dot`, `.sb-meter`, `.sb-toggle`, `.sb-nav-item`, `.sb-avatar-panel`
   - Responsive: `@media (min-width: 900px)` pushes content; `@media (max-width: 899px)` overlay only
   - Hamburger button style

4. **Sidebar JavaScript added** (before PROJECTS SIDEBAR section):
   - `toggleSidebar()`, `closeSidebar()` — open/close with overlay
   - `sidebarNav(target)` — dispatches to existing show* functions + avatar-studio
   - `refreshSidebarStatus()` — fetches manifest for model/provider info
   - `sbToggle()`, `enablePaidUsage()`, `stayLocal()` — toggle/budget handlers

5. **Minor fix**: `toggleProjects()` and `toggleHistory()` — removed references to `projects-toggle` / `history-toggle` buttons (no longer exist in header)

### `joi_companion.py`

**Changes:**

1. **Added** `AVATAR_STUDIO_PATH` constant + `/avatar_studio` route (serves `avatar_studio.html`)
   - Location: after the existing `index()` route (~line 264)
   - Pattern matches existing UI serving approach (read from disk each request)

**No other existing files were modified.**

---

## MODAL-ONLY R2 MIGRATION (2026-02-10)

### Architecture Change

**Before**: Flask API → `cloud_r2_client.py` (local boto3 + local R2_* env vars)
**After**: Flask API → `modal_worker_client.py` → Modal functions (R2 access inside Modal only)

All R2 operations now run inside Modal using `modal.Secret.from_name("joi-storage-secret")`.
No R2/Cloudflare credentials are needed on the local machine.

### Files Modified

| File | Change |
|------|--------|
| `cloud_workers/avatar_studio/modal_avatar_generate.py` | Rewrote: 4 Modal functions (`avatar_upload_photos`, `r2_health_check`, `r2_list_versions`, `generate_avatar`). Uses `CLOUDFLARE_*` env var names from Modal secret. Shared `_get_r2_client()` helper. `modal.Image.debian_slim().pip_install("boto3")` for R2 access. |
| `modules/modal_worker_client.py` | Rewrote: Real Modal client using `modal.Function.lookup()`. Functions: `upload_photos()`, `health_check()`, `list_versions()`, `start_avatar_generate_job()`. Base64 encodes images for transport. |
| `modules/avatar_studio_api.py` | Rewrote imports: `from modules.modal_worker_client import ...` (was `from modules.cloud_r2_client`). All 3 route handlers now delegate to Modal. |
| `tools/test_r2_avatar_upload.py` | Rewrote: Uses `requests` library to call Flask API endpoints. No local R2 imports. Tests health, upload, list-versions via HTTP. |
| `PATCH_NOTES.md` | Added this section. |

### Data Flow

```
User (browser)
  → POST /api/avatar_studio/upload_photos (Flask)
    → modal_worker_client.upload_photos()
      → base64 encode images
      → modal.Function.lookup("joi-avatar-studio", "avatar_upload_photos").remote()
        → [Inside Modal] _get_r2_client() using CLOUDFLARE_* from secret
        → [Inside Modal] s3.put_object() to joi-superai bucket
        → [Inside Modal] s3.get_object() to verify round-trip
      ← {"ok": True, "keys": {...}}
    ← JSON response to browser
```

### Modal Secret: `joi-storage-secret`

Required env vars inside the Modal secret:

| Key | Description |
|-----|-------------|
| `CLOUDFLARE_ACCESS_KEY_ID` | R2 API token access key |
| `CLOUDFLARE_SECRET_ACCESS_KEY` | R2 API token secret key |
| `CLOUDFLARE_R2_ENDPOINT` | Full endpoint URL (e.g. `https://<account_id>.r2.cloudflarestorage.com`) |

Optional: `CLOUDFLARE_ACCOUNT_ID` (used to build endpoint if `CLOUDFLARE_R2_ENDPOINT` is not set).

### Setup

```bash
# 1. Create Modal secret (one-time)
modal secret create joi-storage-secret \
  CLOUDFLARE_ACCESS_KEY_ID=your_key \
  CLOUDFLARE_SECRET_ACCESS_KEY=your_secret \
  CLOUDFLARE_R2_ENDPOINT=https://your_account_id.r2.cloudflarestorage.com

# 2. Deploy Modal app
modal deploy cloud_workers/avatar_studio/modal_avatar_generate.py

# 3. Start Joi (no R2 env vars needed locally)
python joi_companion.py

# 4. Test
python tools/test_r2_avatar_upload.py
```

## DEPENDENCIES

| Package | Required By | Notes |
|---------|-------------|-------|
| `boto3` | `cloud_r2_client.py` (legacy), Modal worker image | R2 S3-compatible API. Installed inside Modal image automatically. |
| `modal` | `modal_worker_client.py`, `modal_avatar_generate.py` | Required locally for `Function.lookup()` + deployment. Install: `pip install modal` |
| `requests` | `tools/test_r2_avatar_upload.py` | For HTTP test calls. Install: `pip install requests` |

## ENVIRONMENT VARIABLES

**Local `.env`**: No R2/Cloudflare credentials needed.

**Modal Secret** (`joi-storage-secret`): `CLOUDFLARE_ACCESS_KEY_ID`, `CLOUDFLARE_SECRET_ACCESS_KEY`, `CLOUDFLARE_R2_ENDPOINT`

## HOW TO TEST

1. **Deploy Modal app**: `modal deploy cloud_workers/avatar_studio/modal_avatar_generate.py`
2. **Start Joi**: `python joi_companion.py`
3. **Open browser**: `http://localhost:5000/`
4. **Click ☰** → sidebar opens → navigate via sidebar
5. **Avatar Studio**: Click "Avatar Studio" in sidebar, or go to `http://localhost:5000/avatar_studio`
6. **Upload Test**: `python tools/test_r2_avatar_upload.py`
7. **Generate Test**: `python tools/test_generate_avatar.py`

---

## AVATAR STUDIO V1 — 3D GENERATION (2026-02-10)

### New Capability

Real 3D model generation from a single reference photo using **TripoSR** on **Modal A10G GPU**.
Output: GLB file stored in Cloudflare R2, viewable in-browser with three.js.

### Files Modified

| File | Change |
|------|--------|
| `cloud_workers/avatar_studio/modal_avatar_generate.py` | Added `generate_avatar_v1()` (TripoSR GPU pipeline), `r2_download()`. New `gpu_image` with torch/TripoSR deps. `model_cache` Volume for weights. |
| `modules/modal_worker_client.py` | Added `start_generate()` (thread-based async), `poll_generate()`, `download_artifact()`. Job tracking via `_jobs` dict. |
| `modules/avatar_studio_api.py` | Added 3 routes: `POST /generate`, `GET /job/<job_id>`, `GET /artifact`. Total: 6 routes. |
| `avatar_studio.html` | Wired Generate button to async flow with polling. Embedded three.js GLB viewer (loaded from CDN). Download link. Version badge updated to v1. |

### New Files

| File | Purpose |
|------|---------|
| `tools/test_generate_avatar.py` | E2E test: upload → generate → poll → verify artifact |

### Updated Docs

| File | Change |
|------|--------|
| `docs/AVATAR_STUDIO_V0.md` | Added full v1 section: pipeline, API, meta.json format, caching |
| `PATCH_NOTES.md` | This section |

### GPU Pipeline Details

- **Model**: TripoSR (stabilityai/TripoSR on HuggingFace)
- **GPU**: NVIDIA A10G (via Modal)
- **Input**: Front reference photo (front.jpg from R2)
- **Output**: GLB mesh (256 resolution marching cubes)
- **Typical time**: ~20-40s (first run includes model download)
- **Weight cache**: Modal Volume `avatar-model-cache` persists HF + rembg weights

### New API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/api/avatar_studio/generate` | Start generation. Body: `{"avatar_id":"...","version":"..."}`. Returns `job_id`. |
| GET | `/api/avatar_studio/job/<job_id>` | Poll: `{status:"running\|done\|error", result:{...}}` |
| GET | `/api/avatar_studio/artifact` | Download generated file. Params: `avatar_id`, `version`, `file` |
