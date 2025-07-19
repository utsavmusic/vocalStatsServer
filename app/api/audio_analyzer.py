from fastapi import APIRouter, UploadFile, File,Query
from app.services.pitch_service import get_extreme_notes
import librosa
import shutil
from app.services.audio_service import AudioService
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



@router.post("/analyze")
async def analyze_audio(
    file: UploadFile = File(...),
    stems: int = Query(2, description="Number of stems (e.g., 2 or 5)"),
    model: str = Query("spleeter", description="Model name")
):
    # Save uploaded file temporarily
    input_path = f"/tmp/{file.filename}"
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Call service
    service = AudioService(model_name=model)
    output_dir = service.process_audio(input_path, stems)

    # Clean up input file
    os.remove(input_path)
    return {"message": f"Audio separated into {stems} stems", "output_dir": output_dir}
