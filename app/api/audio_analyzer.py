from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.frequency_audio import get_frequency_data
from app.services.pitch_service import get_high_low_notes
import librosa
import os

router = APIRouter()

@router.post("/api/notes")
async def api_notes(audio: UploadFile = File(...)):
    file_location = f"temp/{audio.filename}"
    os.makedirs("temp", exist_ok=True)
    with open(file_location, "wb") as f:
        f.write(await audio.read())

    y, sr = librosa.load(file_location)
    low_note, high_note = get_high_low_notes(y, sr)
    os.remove(file_location)
    return {
        "lowest_note": low_note,
        "highest_note": high_note
    }

@router.post("/api/frequency")
async def api_frequency(audio: UploadFile = File(...)):
    file_location = f"temp/{audio.filename}"
    os.makedirs("temp", exist_ok=True)
    with open(file_location, "wb") as f:
        f.write(await audio.read())

    y, sr = librosa.load(file_location)
    freq_data = get_frequency_data(y, sr)
    os.remove(file_location)
    return {
        'frequency_over_time': freq_data
    }
