from src.db.mongodb import DatabaseClient
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from os.path import join
from src.routers import init, applications, datasets
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import storage
# cred = credentials.Certificate('path/to/serviceAccountKey.json')
# firebase_admin.initialize_app(cred, {'storageBucket': 'deep-uai.appspot.com'})
# bucket = storage.bucket()
# # 'bucket' is an object defined in the google-cloud-storage Python library.
# # See https://googlecloudplatform.github.io/google-cloud-python/latest/storage/buckets.html
# # for more details.

DatabaseClient.initialize('deepuai')
app = FastAPI()
app.mount('/models', StaticFiles(directory=join('assets','models')))
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_methods=['*'])
app.include_router(init.router)
app.include_router(applications.router)
app.include_router(datasets.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}