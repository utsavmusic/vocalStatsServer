from app.config.exceptions import add_exception_handlers
from app.config.logger import get_logger
from app.config.server import configure_cors
from app.services.frequency_audio import get_frequency_data
from app.services.pitch_service import get_high_low_notes
from fastapi import File, UploadFile
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.audio_analyzer import api_notes,api_frequency
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from app.api.audio_analyzer import router as audio_router

router = APIRouter()
app = FastAPI()

logger = get_logger(__name__)

# Configure CORS and exception handlers
configure_cors(app)
add_exception_handlers(app)

# Root endpoint to verify server is running
@app.get("/")
def read_root():
  logger.info("Root endpoint accessed")
  return {"Msg": "Hello World!"}

# Example endpoint to demonstrate a successful response
@app.get("/fail")
def fail_endpoint():
  raise HTTPException(status_code=404, detail="This item was not found.")

# Example endpoint to demonstrate exception handling
@app.get("/explode")
def explode():
  return 1 / 0

app.include_router(audio_router)