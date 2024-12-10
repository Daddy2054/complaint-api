from fastapi import FastAPI
import uvicorn
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)