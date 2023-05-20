from fastapi import APIRouter
from fastapi import Request
import logica

router = APIRouter()

@router.get("/aulas")
async def get_aulas():
    return logica.respuesta_exitosa(logica.obtener_aulas())

@router.get("/aulas/{id_aula}")
async def get_aula(id_aula: int):
    return logica.respuesta_exitosa(logica.obtener_aula(id_aula))

@router.post("/aulas")
async def post_aula(request: Request):
    data = await request.json()
    return logica.respuesta_exitosa(logica.insertar_aula(data))