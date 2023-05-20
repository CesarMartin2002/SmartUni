from fastapi import APIRouter
from fastapi import Request
import logica

router = APIRouter()

@router.get("/aulas")
async def get_aulas():
    """
    Obtiene todas las aulas registradas en la base de datos.
    """
    return logica.respuesta_exitosa(logica.obtener_aulas())

@router.get("/aulas/{id_aula}")
async def get_aula(id_aula: int):
    """
    Obtiene una aula en específico, según su id.
    """
    return logica.respuesta_exitosa(logica.obtener_aula(id_aula))

@router.post("/aulas")
async def post_aula(request: Request):
    """
    Inserta una nueva aula en la base de datos.
    """
    data = await request.json()
    return logica.respuesta_exitosa(logica.insertar_aula(data))
                                    
@router.put("/aulas/{id_aula}")
async def put_aula(id_aula: int, request: Request):
    """
    Actualiza una aula en la base de datos. El aula a actualizar se especifica según su id en la URL.
    """
    data = await request.json()
    return logica.respuesta_exitosa(logica.actualizar_aula(id_aula, data))