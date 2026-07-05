from fastapi import FastAPI

from app.api.results import router as results_router

app = FastAPI()

app.include_router(results_router)