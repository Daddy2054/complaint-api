from fastapi import FastAPI
from resources.routes import api_router
from db import database
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Code that runs before the application starts
    await database.connect()
    yield
    # Shutdown: Code that runs when the application is shutting down
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}