# Avatar Studio v0

## Architecture

All R2 storage operations run inside **Modal** using `modal.Secret.from_name("joi-storage-secret")`.
No R2/Cloudflare credentials are needed on the local machine.

```
Browser → Flask API → modal_worker_client.py → Modal Function → Cloudflare R2 (joi-superai bucket)
```

### Modal Functions (cloud_workers/avatar_studio/modal_avatar_generate.py)

| Function | Description |
|----------|-------------|
| `avatar_upload_photos` | Upload 3 base64-encoded photos to R2, verify round-trip |
| `r2_health_check` | Verify R2 connectivity (list avatars/ prefix) |
| `r2_list_versions` | List all version strings for an avatar |
| `generate_avatar` | (stub) Download source images, write placeholder artifacts |

### API Endpoints (Local Flask)

| Method | Route | Description |
|--------|-------|-------------|
| POST   | `/api/avatar_studio/upload_photos` | Upload 3 photos (multipart form) → Modal → R2 |
| GET    | `/api/avatar_studio/list_versions?avatar_id=...` | List all versions for an avatar |
| GET    | `/api/avatar_studio/health` | Verify R2 credentials and connectivity via Modal |

### R2 Key Layout

```
avatars/source/{avatar_id}/{version}/front.jpg
avatars/source/{avatar_id}/{version}/left.jpg
avatars/source/{avatar_id}/{version}/right.jpg
avatars/build/{avatar_id}/{version}/placeholder.txt   (generate_avatar output)
avatars/final/{avatar_id}/{version}/avatar.vrm         (generate_avatar output)
```

Version format: `YYYYMMDD_HHMMSS`

### UI

- **Route**: `/avatar_studio` (separate page linked from sidebar)
- **Features**: 3 file upload slots with preview, avatar_id field, upload/generate/list buttons, status area, health indicator

## What Does NOT Exist Yet (v0 limitations)

- Multi-view fusion (currently uses front photo only)
- VRM format export (GLB only)
- Paid usage metering in sidebar
- Texture/material refinement

---

# Avatar Studio v1

## What's New

- **Real 3D generation**: TripoSR (single-image-to-3D) running on Modal A10G GPU
- **Async job flow**: POST to generate, poll for status, get result when done
- **GLB output**: Industry-standard 3D format, stored in R2
- **In-browser 3D viewer**: three.js GLTFLoader + OrbitControls
- **Artifact download**: Proxy endpoint serves GLB files from R2

## v1 Modal Functions

| Function | GPU | Description |
|----------|-----|-------------|
| `generate_avatar_v1` | A10G | Download front.jpg from R2, run TripoSR, export GLB, upload GLB + meta.json to R2 |
| `r2_download` | CPU | Download any file from R2 (base64 transport) |

## v1 API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST   | `/api/avatar_studio/generate` | Start async generation job. Body: `{"avatar_id": "...", "version": "..."}`. Returns `job_id`. |
| GET    | `/api/avatar_studio/job/<job_id>` | Poll job status: `running`, `done`, `error`. When done, includes `result.meta` and `result.keys`. |
| GET    | `/api/avatar_studio/artifact?avatar_id=...&version=...&file=model.glb` | Download generated file from R2 (proxied through Flask). |

## v1 R2 Key Layout

```
avatars/generated/{avatar_id}/{version}/model.glb    — 3D model (GLB)
avatars/generated/{avatar_id}/{version}/meta.json    — Generation metadata
```

## v1 Generation Pipeline

```
1. Flask receives POST /api/avatar_studio/generate
2. modal_worker_client.start_generate() spawns background thread
3. Thread calls generate_avatar_v1.remote() on Modal
4. [Inside Modal, A10G GPU]:
   a. Download front.jpg from R2
   b. Load TripoSR model (cached in Modal Volume)
   c. Run inference → trimesh mesh
   d. Export to GLB
   e. Upload GLB + meta.json to R2
5. Flask job tracker updates status to "done"
6. UI polls /job/<id>, gets result, loads 3D viewer
```

## v1 Model Weights Cache

- Modal Volume: `avatar-model-cache`
- HuggingFace cache: `/cache/hf/` (TripoSR weights ~1.5GB + DINOv2)
- rembg model: `/cache/u2net/` (U2Net ~175MB)
- First run downloads all weights; subsequent runs reuse cache

## How to Test v1

```bash
# Deploy (includes GPU function)
modal deploy cloud_workers/avatar_studio/modal_avatar_generate.py

# Start server
python joi_companion.py

# Run v1 generation test
python tools/test_generate_avatar.py
```

## meta.json Format

```json
{
  "avatar_id": "joi_v1",
  "version": "20260210_150000",
  "source_key": "avatars/source/joi_v1/20260210_150000/front.jpg",
  "format": "glb",
  "vertices": 65536,
  "faces": 131072,
  "glb_size_bytes": 5242880,
  "model_load_time_s": 12.3,
  "inference_time_s": 8.5,
  "total_time_s": 25.1,
  "pipeline": "TripoSR",
  "gpu": "A10G",
  "resolution": 256
}
```

## Setup

### 1. Create Modal Secret (one-time)

```bash
modal secret create joi-storage-secret \
  CLOUDFLARE_ACCESS_KEY_ID=your_access_key \
  CLOUDFLARE_SECRET_ACCESS_KEY=your_secret_key \
  CLOUDFLARE_R2_ENDPOINT=https://your_account_id.r2.cloudflarestorage.com
```

### 2. Deploy Modal App

```bash
cd "C:\Users\user\Desktop\AI Joi"
modal deploy cloud_workers/avatar_studio/modal_avatar_generate.py
```

### 3. Start Joi

```bash
python joi_companion.py
```

### 4. Open in Browser

- Main UI: `http://localhost:5000/`
- Avatar Studio: `http://localhost:5000/avatar_studio`
- Or click "Avatar Studio" in the sidebar Navigation section

## How to Test

```bash
cd "C:\Users\user\Desktop\AI Joi"
python joi_companion.py          # start server first (separate terminal)
python tools/test_r2_avatar_upload.py
```

The test script calls Flask API endpoints via HTTP (no local R2 credentials needed).
It tests: health check, upload 3 dummy images, list versions.

## Modal Secret: `joi-storage-secret`

| Key | Required | Description |
|-----|----------|-------------|
| `CLOUDFLARE_ACCESS_KEY_ID` | Yes | R2 API token access key |
| `CLOUDFLARE_SECRET_ACCESS_KEY` | Yes | R2 API token secret key |
| `CLOUDFLARE_R2_ENDPOINT` | Yes* | Full endpoint URL (e.g. `https://<account_id>.r2.cloudflarestorage.com`) |
| `CLOUDFLARE_ACCOUNT_ID` | Alt* | Used to build endpoint URL if `CLOUDFLARE_R2_ENDPOINT` is not set |

*One of `CLOUDFLARE_R2_ENDPOINT` or `CLOUDFLARE_ACCOUNT_ID` is required.

## Dependencies

| Package | Where | Notes |
|---------|-------|-------|
| `modal` | Local + Modal cloud | `pip install modal`. Required locally for `Function.lookup()` and deployment. |
| `boto3` | Modal cloud only | Installed automatically in the Modal image (`modal.Image.debian_slim().pip_install("boto3")`). Not needed locally. |
| `requests` | Local (test script only) | `pip install requests`. Only needed for `tools/test_r2_avatar_upload.py`. |
