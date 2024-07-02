from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import posts, users, auth, votes
from app.pages.router import router as pages_router

app = FastAPI(title="MPEI_PRACTICE")

origins=["http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
app.include_router(pages_router)
