
from fastapi import APIRouter
from .endpoints import chats

api_router = APIRouter()
api_router.include_router(chats.router, prefix="/chats", tags=["chats"])
