from app.config.exceptions import add_exception_handlers
from app.config.logger import get_logger
from app.config.server import configure_cors
from fastapi import FastAPI, HTTPException
from fastapi import APIRouter
from app.api.audio_analyzer import router as audio_router
from app.utils.file_utils import cleanup_temp_and_tmp
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler

router = APIRouter()
app = FastAPI(debug=True)
logger = get_logger(__name__)

# Configure CORS and exception handlers
configure_cors(app)
add_exception_handlers(app)

# Call the new cleanup function at startup
cleanup_temp_and_tmp()

# Set up APScheduler to run cleanup every 15 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_temp_and_tmp, 'interval', minutes=15)
scheduler.start()

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