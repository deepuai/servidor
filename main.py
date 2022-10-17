from mimetypes import init
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from utils.eval import eval_resnet50
from utils.init_base import init_base
from utils.applications import applications
from fastapi.middleware.cors import CORSMiddleware
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import storage
# cred = credentials.Certificate('path/to/serviceAccountKey.json')
# firebase_admin.initialize_app(cred, {'storageBucket': 'deep-uai.appspot.com'})
# bucket = storage.bucket()
# # 'bucket' is an object defined in the google-cloud-storage Python library.
# # See https://googlecloudplatform.github.io/google-cloud-python/latest/storage/buckets.html
# # for more details.

app = FastAPI()
app.mount("/models", StaticFiles(directory="models"), name="models")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"])
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/resnet50/{weights_name}/eval")
async def eval_endpoint(weights_name, img_file: UploadFile = File(...)):
    return eval_resnet50(weights_name, img_file)

@app.get("/applications/{model_name}")
async def applications_endpoint(model_name):
    return applications(model_name)

@app.get('/init')
async def init_base_endpoint():
    return {"mensagem": init_base()}