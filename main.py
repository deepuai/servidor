from fastapi import FastAPI, File, UploadFile
from utils.evaluate_model import evaluate_model
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"])
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/{model_name}/eval")
async def evaluate(model_name, image: UploadFile = File(...)):
    return evaluate_model(model_name, image)