from fastapi import APIRouter
from src.utils.init import initialize_bd

router = APIRouter()

@router.get('/init')
async def init_base_endpoint():
    return {"mensagem": initialize_bd()}