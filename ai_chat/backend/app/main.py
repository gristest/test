
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import api

app = FastAPI()

# CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173", # Vite default port
    "http://localhost:8887", # 添加你的前端实际运行端口
    "http://192.168.20.32:8887", # 添加你的前端实际运行端口
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_locale_to_request(request: Request, call_next):
    locale = request.cookies.get("locale", "en")
    request.state.locale = locale
    response = await call_next(request)
    return response

app.include_router(api.api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to AI-Chat API"}
