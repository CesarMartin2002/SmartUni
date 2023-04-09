from fastapi import APIRouter
import logica

router = APIRouter()

@router.get("/casilleros/{id}")
def get_casillero(id: int):
    '''
    Este endpoint devuelve un casillero en particular
    '''
    casillero = logica.obtener_casillero(id)
    return casillero

