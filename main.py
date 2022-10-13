from fastapi import FastAPI, File, UploadFile
from utils.evaluate_model import evaluate_model
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
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"])
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/{model_name}/eval")
async def evaluate(model_name, img_file: UploadFile = File(...)):
    return evaluate_model(model_name, img_file)