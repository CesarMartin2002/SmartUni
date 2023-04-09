from fastapi import APIRouter
import logica

router = APIRouter()

@router.get("/pruebaConsulta")
def prueba_consulta():
    '''
    Este endpoint devuelve un casillero en particular
    '''
    casillero = logica.prueba_consulta()
    return casillero