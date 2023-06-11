from fastapi import APIRouter, Request, Query
import logica
import datetime

router = APIRouter(tags=["Aulas"])

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
    aula = logica.actualizar_aula(id_aula, data)
    return logica.respuesta_exitosa(aula)

@router.post("/aulas/{id_aula}/historico")
async def post_historico_aula(id_aula: int, request: Request):
    """
    Inserta un nuevo historico de aula en la base de datos.
    """
    data = await request.json()
    return logica.respuesta_exitosa(logica.insertar_historico_aula(id_aula, data))

@router.get("/aulas/{id_aula}/climatizar")
async def get_climatizar_aula(id_aula: int):
    """
    Según el id de un aula, devuelve si se debe climatizar o no el aula.
    """
    return logica.respuesta_exitosa(logica.obtener_climatizar_aula(id_aula))

"""
A partir de aqui se definen los endpoints para los horarios de las aulas
"""
@router.get("/aulas/asignaturas/{id_aula}")
async def get_asignaturas_aula(id_aula: int):
    """
    Obtiene las asignaturas que se dan en un aula, según su id.
    """
    return logica.respuesta_exitosa(logica.obtener_asignatura_aula(id_aula))


#consultar disponibilidad de aulas
@router.get("/aulas/disponibilidad/{id_aula}")
async def get_clase_proxima(id_aula: int):
    """
    Se utiliza para saber si un aula está en uso en los próximos minutos.
    Principalmente usado por el Arduino para saber si debe encender o apagar el aire acondicionado.
    """
    prox_clase = logica.obtener_clase_proxima(id_aula)
    #si prox_clase es en los proximos 15 minutos devolver true sino false
    fecha_actual = datetime.datetime.now()
    fecha_futura = fecha_actual + datetime.timedelta(minutes=15)
    return fecha_futura >= prox_clase

@router.get("/aulas/horarios/{id_horario}")
async def get_horario(id_horario: int):
    """
    Obtiene una horario en específico, según su id.
    """
    return logica.respuesta_exitosa(logica.obtener_horario(id_horario))

#insertar horario
@router.post("/aulas/horarios")
async def post_horario(request: Request):
    """
    Inserta un nuevo horario de clase en la base de datos.
    """
    data = await request.json()
    return logica.respuesta_exitosa(logica.insertar_horario(data))
