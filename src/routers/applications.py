from fastapi import APIRouter, Form, UploadFile, File
import src.utils.processing as processing
from src.controllers import applications as applications_controller

router = APIRouter()

@router.post("/{model_name}/{weights_name}/eval")
async def eval_endpoint(model_name: str = 'resnet50', weights_name: str = 'imagenet', img_file: UploadFile = File(...)):
    return processing.eval(model_name, weights_name, img_file)

@router.post("/{model_name}/{weights_name}/fit/file")
async def fit_from_zip_endpoint(
    model_name: str = 'resnet50',
    weights_name: str = 'imagenet',
    parent_id: int = Form(),
    deepuai_app: str = Form(),
    version: str = Form(),
    model_id: int = Form(),
    zip_file: UploadFile = File(...)
    ):
    return await applications_controller.fit_from_file(model_name, weights_name, parent_id, deepuai_app, version, model_id, zip_file)

@router.post("/{model_name}/{weights_name}/fit/dataset")
async def fit_from_dataset_endpoint(
    model_name: str = 'resnet50',
    weights_name: str = 'imagenet',
    parent_id: int = Form(),
    deepuai_app: str = Form(),
    version: str = Form(),
    model_id: int = Form(),
    dataset_id: int = Form(),
    ):
    return await applications_controller.fit_from_dataset(model_name, weights_name, parent_id, deepuai_app, version, model_id, dataset_id)