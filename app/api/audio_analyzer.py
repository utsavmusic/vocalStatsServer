from http.client import HTTPException

from fastapi import APIRouter, UploadFile, File,Query
from starlette.responses import FileResponse

from app.services.pitch_service import get_extreme_notes
import librosa
import shutil
from app.services.audio_service import AudioService
from app.utils.file_utils import create_zip_archive
import os
from pathlib import Path
import uuid
from datetime import datetime

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
    os.makedirs("tmp", exist_ok=True)
    # Generate a unique filename with timestamp and UUID
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    base_name = Path(file.filename).stem
    ext = Path(file.filename).suffix
    unique_filename = f"{base_name}_{timestamp}_{unique_id}{ext}"
    file_location = f"tmp/{unique_filename}"
    print(f"Saving uploaded file to {file_location}")
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    print(f"Starting audio processing with {model} model and {stems} stems...")
    service = AudioService(model_name=model)
    output_dir = service.process_audio(file_location, stems)
    print(f"Output directory: {output_dir}")
    output_path = Path(output_dir)
    files_to_zip = list(output_path.rglob('*.*'))  # Find all files recursively
    print(f"Found {len(files_to_zip)} files to zip:")
    for f in files_to_zip:
        print(f" - {f} (exists: {f.exists()}, size: {f.stat().st_size} bytes)")
    archive_name = f"separated_audio_{base_name}_{timestamp}_{unique_id}"
    print(f"Creating zip archive '{archive_name}' with {len(files_to_zip)} files...")

    file_response = create_zip_archive(
        files=files_to_zip,
        output_dir=output_path,
        archive_name=archive_name
    )

    print("Zip archive created successfully")
    return file_response