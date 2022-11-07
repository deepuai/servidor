from fastapi import APIRouter, Form, UploadFile, File
from src.controllers import models as models_controller

router = APIRouter()

@router.post("/fit_new")
async def fit_endpoint(
    dataset_id: int = Form(),
    model_id: int = Form(),
    version: str = Form(),
    ):
    return await models_controller.fit_from_dataset(
        new_app_version_code=version, model_id=model_id, dataset_id=dataset_id)