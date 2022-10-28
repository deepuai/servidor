from fastapi import APIRouter
from src.utils.init import initialize_models

router = APIRouter()

@router.get('/init')
async def init_models_available():
    return {"mensagem": initialize_models()}