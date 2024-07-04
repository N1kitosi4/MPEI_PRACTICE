from datetime import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor

from app.routers import posts, users, auth, votes
from app.pages.router import router as pages_router
import psycopg2

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


@app.get("/")
def info():
    try:
        conn = psycopg2.connect(host='localhost', database='heh', user='postgres',
                                password='1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
    return {"users": users}
