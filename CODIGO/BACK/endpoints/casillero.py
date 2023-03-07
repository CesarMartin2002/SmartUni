from fastapi import APIRouter
import logica

router = APIRouter()

@router.get("/casilleros/{id}")
def get_casillero(id: int):
    casillero = logica.obtener_casillero(id)
    return casillero

