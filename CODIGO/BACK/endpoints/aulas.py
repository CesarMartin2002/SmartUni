from fastapi import APIRouter, Request, Query
import logica
import datetime

router = APIRouter()

@router.get("/aulas")
async def get_aulas(ala: str = Query(default=""),planta: int = Query(default=0),numero: int = Query(default=0)):
    """
    Obtiene todas las aulas registradas en la base de datos.
    """
    return logica.respuesta_exitosa(logica.obtener_aulas(ala, planta, numero))

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


"""
A partir de aqui se definen los endpoints para los horarios de las aulas
"""

#consultar disponibilidad de aulas
@router.get("/aulas/{id_aula}")
async def get_clase_proxima(id_aula: int):
    prox_clase = logica.obtener_clase_proxima(id_aula)
    #si prox_clase es en los proximos 15 minutos devolver true sino false
    fecha_actual = datetime.datetime.now()
    fecha_futura = fecha_actual + datetime.timedelta(minutes=15)
    return fecha_futura >= prox_clase

#insertat horario
@router.post("/aulas/{id_aula}/horarios")
async def post_horario(id_aula: int):
    """
    Inserta un nuevo horario de clase en la base de datos.
    """
    return logica.respuesta_exitosa(logica.insertar_horario(id_aula))
