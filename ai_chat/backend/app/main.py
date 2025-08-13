
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import api

app = FastAPI()

# CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173", # Vite default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to AI-Chat API"}
