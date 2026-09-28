from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import Settings
from routers import story, job
from db.database import create_tables

create_tables()  

app = FastAPI(
    title="choose the game",
    description="A simple game selection API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(story.router, prefix=Settings.API_PREFIX)
app.include_router(job.router, prefix=Settings.API_PREFIX)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
