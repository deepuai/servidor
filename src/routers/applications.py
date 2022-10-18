import json
from fastapi import APIRouter, UploadFile, File
from src.utils.eval import eval_resnet50
from src.controllers import applications as applications_controller

router = APIRouter()

@router.post("/resnet50/{weights_name}/eval")
async def eval_endpoint(weights_name, img_file: UploadFile = File(...)):
    return eval_resnet50(weights_name, img_file)

@router.get("/applications")
async def list_applications():
    return applications_controller.list_all()