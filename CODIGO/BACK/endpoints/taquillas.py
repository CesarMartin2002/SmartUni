# todo esto es necesario para que funcione cualquier .py que se encuentre en la carpeta endpoints
from fastapi import APIRouter, Path, Request, Query
import logica
import random


router = APIRouter(tags=["Taquillas"]) 

# a partir de aquí se definen las rutas


@router.get("/taquillas/{id_taquilla}")
async def get_taquilla(id_taquilla: int, id_alumno: int = Query(default=-1)):
    """
    Este endpoint devuelve una taquilla en particular a partir de su id
    """
    taquilla = logica.obtener_taquilla(id_taquilla,id_alumno)
    return logica.respuesta_exitosa(taquilla)


@router.get("/taquillas") 
async def get_taquillas(ala: str = Query(default=""), piso: int = Query(default=-1), pasillo: int = Query(default=-1), ocupado: bool = Query(default=-1)):
    """
    Este endpoint devuelve todas las taquillas.
    Se puede filtrar por:
    - ala
    - piso
    - pasillo
    - ocupacion
    """
    taquillas = logica.obtener_todasTaquillas(ala, piso, pasillo, ocupado)
    return logica.respuesta_exitosa(taquillas)


@router.post("/taquillas") 
async def post_taquilla(request: Request):
    """
    Crear una nueva taquilla con los datos recibidos en el body
    """
    #data es un diccionario con los datos que se reciben en el form data
    data = await request.json()
    #eliminar campo password de la tabla taquillas
    data.pop("password", None)
    print("data: ", data)
    taquilla = logica.crear_taquilla(data)
    return logica.respuesta_exitosa(taquilla)


#endpoint abrir taquilla
@router.post("/taquillas/{id_taquilla}")
async def abrir_taquilla(id_taquilla: int, request: Request):
    """
    Este endpoint permite abrir una taquilla a partir de una taquilla, y password
    """
    data = await request.json()
    password = data["password"]
    resultado = logica.abrir_taquilla(id_taquilla, password)
    return logica.respuesta_exitosa(resultado)


#endpoint reservar taquilla
@router.put("/taquillas/reservar/{id_taquilla}")
async def reservar_taquilla(id_taquilla:int, request: Request):
    """
    Este endpoint permite reservar una taquilla a partir de una taquilla y alumno y genera una contraseña
    """
    numero = random.randint(1000, 9999)
    data = await request.json()
    id_alumno = data["id_alumno"]
    json = {"password": numero,
            "id_alumno_alumno": id_alumno,
            "ocupado": True
            }

    #numero_str = str(numero).zfill(4)      para el cambio a string
    # resultado = logica.reservar_taquilla(id_taquilla, id_alumno, numero)
    resultado = logica.reservar_taquilla(id_taquilla, json)
    
    return logica.respuesta_exitosa(resultado)


#endpoint cancelar taquilla
@router.put("/taquillas/cancelar/{id_taquilla}/{id_alumno}")
def cancelar_taquilla(id_taquilla : int, id_alumno:int) -> dict:
    """Este Endpoint cancela la reserva o la asignacion al alumno
    Returns:
        dict: Informacion de la taquilla cancelada
    """
    cancelar_taquilla = logica.cancelar_taquilla(id_taquilla, id_alumno)
    return logica.respuesta_exitosa(cancelar_taquilla)


@router.get("/taquilla/Alumno/{id_alumno}")
async def obtener_taquilla_reservada(id_alumno: int):
    """
    Este endpoint devuelve la taquilla reservada por el alumno
    """
    taquilla_reservada = logica.obtener_taquilla_reservada_por_alumno(id_alumno)
    if taquilla_reservada:
        return logica.respuesta_exitosa(taquilla_reservada)
    else:
        return logica.respuesta_fallida("No se encontró una taquilla reservada para el alumno con id: " + str(id_alumno))

