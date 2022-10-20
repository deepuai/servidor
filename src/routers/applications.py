from fastapi import APIRouter, UploadFile, File
import src.utils.processing as processing
from src.controllers import applications as applications_controller

router = APIRouter()

@router.post("/{model_name}/{weights_name}/eval")
async def eval_endpoint(model_name: str = 'resnet50', weights_name: str = 'imagenet', img_file: UploadFile = File(...)):
    return processing.eval(model_name, weights_name, img_file)

@router.post("/{model_name}/{weights_name}/fit")
async def fit_endpoint(model_name: str = 'resnet50', weights_name: str = 'imagenet', zip_file: UploadFile = File(...)):
    return applications_controller.fit(model_name, weights_name, zip_file)

@router.get("/applications")
async def list_applications():
    return applications_controller.list_all()