from fastapi import FastAPI
from app.routers import process

app = FastAPI()  # The FastAPI app
app.include_router(process.router)  # including the router
