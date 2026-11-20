"""
NPL Studio CapCut TTS bridge.
Unofficial community SDK wrapper. Run on a trusted server, never expose CapCut
cookies/bearer tokens in browser JavaScript or an APK.
"""
import os, uuid, re
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from capcut_tts_api import CapCutClient

APP_DIR = Path(__file__).resolve().parent
AUDIO_DIR = APP_DIR / "generated_audio"
AUDIO_DIR.mkdir(exist_ok=True)
NPL_API_KEY = os.getenv("NPL_API_KEY", "")
app = FastAPI(title="NPL Studio CapCut TTS Bridge", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
                   allow_credentials=False, allow_methods=["GET","POST"], allow_headers=["*"])

def authorize(auth: Optional[str]):
    if NPL_API_KEY and auth != f"Bearer {NPL_API_KEY}":
        raise HTTPException(401, "NPL API key không hợp lệ")

def client():
    return CapCutClient(timeout=60)

class PreviewRequest(BaseModel):
    provider: str = "capcut"
    text: str = Field(min_length=1, max_length=5000)
    voice: str = "BV421_vivn_streaming"
    resourceId: Optional[str] = None
    language: str = "vi-VN"
    rate: float = 1.0

class Cue(BaseModel):
    startMs: int
    endMs: int
    text: str

class SRTRequest(BaseModel):
    provider: str = "capcut"
    cues: list[Cue]
    voice: str = "BV421_vivn_streaming"
    voiceType: Optional[str] = None
    resourceId: Optional[str] = None
    language: str = "vi-VN"
    rate: float = 1.0
    keepTimestamps: bool = True

@app.get("/health")
def health():
    return {"ok": True, "service": "NPL Studio CapCut TTS bridge"}

@app.get("/tts/voices")
def voices(provider: str = "capcut", language: str = "vi-VN",
           authorization: Optional[str] = Header(default=None)):
    authorize(authorization)
    if provider != "capcut":
        raise HTTPException(400, "Bridge này chỉ xử lý provider=capcut")
    try:
        items = client().list_voices(lang=language)
        return {"voices": [
            {"voiceType": v.voice_type, "voice_type": v.voice_type,
             "resourceId": v.resource_id, "resource_id": v.resource_id,
             "name": v.display_name, "display_name": v.display_name,
             "lang": getattr(v, "lang", language)}
            for v in items
        ]}
    except Exception as e:
        raise HTTPException(502, f"Không tải được danh sách giọng: {e}")

def make_audio(text: str, voice: str, resource_id: Optional[str]):
    c = client()
    selected = resource_id or voice
    try:
        result = c.generate_speech(text, voice=voice, resource_id=resource_id, timeout=180)
        out = AUDIO_DIR / f"{uuid.uuid4().hex}.mp3"
        c.download_tts_audio(result, str(out))
        if not out.exists() or out.stat().st_size == 0:
            raise RuntimeError("SDK không tạo được file audio")
        return out
    except Exception as e:
        raise HTTPException(502, f"CapCut TTS thất bại: {e}")

@app.post("/tts/preview")
def preview(req: PreviewRequest, authorization: Optional[str] = Header(default=None)):
    authorize(authorization)
    if req.provider != "capcut":
        raise HTTPException(400, "Chỉ hỗ trợ provider=capcut")
    path = make_audio(req.text, req.voice, req.resourceId)
    return {"audioUrl": f"/audio/{path.name}", "fileName": path.name, "provider": "capcut"}

@app.post("/tts/srt")
def synthesize_srt(req: SRTRequest, authorization: Optional[str] = Header(default=None)):
    authorize(authorization)
    if req.provider != "capcut":
        raise HTTPException(400, "Chỉ hỗ trợ provider=capcut")
    audio_files = []
    for i, cue in enumerate(req.cues):
        text = cue.text.strip()
        if not text:
            continue
        path = make_audio(text, req.voiceType or req.voice, req.resourceId)
        audio_files.append({"index": i, "startMs": cue.startMs, "endMs": cue.endMs,
                            "text": text, "audioUrl": f"/audio/{path.name}",
                            "fileName": path.name})
    return {"provider": "capcut", "audioFiles": audio_files,
            "cues": audio_files, "keepTimestamps": req.keepTimestamps,
            "note": "Audio từng câu; cần FFmpeg/native renderer để ghép đúng timestamp và xuất MP4."}

@app.get("/audio/{filename}")
def audio(filename: str):
    if not re.fullmatch(r"[a-f0-9]{32}\.mp3", filename):
        raise HTTPException(404, "Không tìm thấy audio")
    path = AUDIO_DIR / filename
    if not path.exists():
        raise HTTPException(404, "Audio đã hết hạn hoặc không tồn tại")
    return FileResponse(path, media_type="audio/mpeg", filename=filename)
