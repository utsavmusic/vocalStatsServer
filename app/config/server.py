from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def configure_cors(app: FastAPI) -> None:
  origins = [
    "http://localhost:3000",  # Local frontend dev
    # TODO: Add test and production origins
  ]

  allowed_methods = ["GET", "POST", "PUT", "DELETE"]

  app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=allowed_methods,
    allow_headers=["*"]
  )
