import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .routers.tickets import router as tickets_router
from .routers.auth import router as auth_router
from .ws import router as ws_router

load_dotenv()
app = FastAPI(title="TeamBoard API", version="1.0.0")

origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["ETag"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(tickets_router, prefix="/tickets", tags=["Tickets"])
app.include_router(ws_router, tags=["Live updates"])

@app.get("/")
def root():
    return {"message": "Welcome to TeamBoard API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}
