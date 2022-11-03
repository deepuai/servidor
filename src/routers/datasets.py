from fastapi import APIRouter, UploadFile, File
from src.controllers import datasets as datasets_controller

router = APIRouter()

@router.post("/dataset/upload")
async def save_dataset(zip_file: UploadFile = File(...)):
    return await datasets_controller.save(zip_file)