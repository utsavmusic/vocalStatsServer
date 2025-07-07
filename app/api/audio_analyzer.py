from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pitch_service import get_extreme_notes
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
    extreme_notes = get_extreme_notes(y, sr)
    os.remove(file_location)
    return extreme_notes

@router.post("/api/amplitude_time_series")
async def api_amplitude_time_series(audio: UploadFile = File(...)):
    file_location = f"uploads/amplitude_time_series_inputs/{audio.filename}"
    os.makedirs("uploads/amplitude_time_series_inputs", exist_ok=True)
    with open(file_location, "wb") as f:
        f.write(await audio.read())
        
    y, sr = librosa.load(file_location, sr=None)
    os.remove(file_location)
    downsample_rate = 100  # every 100th sample
    # Downsampling is crucial here to reduce the size of the time series data.
    # This is because the amplitude time series can be very large, especially 
    # for long audio files. 
    y_downsampled = y[::downsample_rate]
    return {
        'amplitude_time_series': y_downsampled.tolist(),
        'sample_rate': sr
    }
