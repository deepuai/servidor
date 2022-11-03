from src.db.postgres import DatabaseClient
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from os.path import join
from src.routers import init, applications, datasets
from constants import DATASETS_URL

DatabaseClient.initialize('deepuai')
app = FastAPI()
app.mount(DATASETS_URL, StaticFiles(directory=join('assets','dataset')), name='dataset')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_methods=['*'])
app.include_router(init.router)
app.include_router(applications.router)
app.include_router(datasets.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}