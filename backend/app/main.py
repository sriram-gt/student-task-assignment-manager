from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, tasks
from app.models import user, task
Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="Student Task & Assignment Manager",
    description="Manage your assignments and tasks efficiently",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "STAM API is running"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, tasks
from app.models import user, task
from prometheus_fastapi_instrumentator import Instrumentator

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Task & Assignment Manager",
    description="Manage your assignments and tasks efficiently",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)

Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    return {"message": "STAM API is running"}