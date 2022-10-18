from fastapi import APIRouter
from src.controllers import applications as applications_controller

router = APIRouter()

@router.get("/dataset")
async def get_dataset_imagens(application: str = 'ResNet50', datasetName: str = 'ImageNet'):
    return applications_controller.list_dataset_imagens(application, datasetName)