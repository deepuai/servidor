from src.db.mongodb import DatabaseClient
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from os.path import join
from src.routers import init, applications

DatabaseClient.initialize('deepuai')
app = FastAPI()
app.mount('/models', StaticFiles(directory=join('assets','models')))
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_methods=['*'])
app.include_router(init.router)
app.include_router(applications.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}