# todo esto es necesario para que funcione cualquier .py que se encuentre en la carpeta endpoints
from fastapi import APIRouter, Path, Request, Query
import logica

router = APIRouter() 

# a partir de aquí se definen las rutas

@router.get("/taquillas/{id}")
async def get_taquilla(id: int):
    """
    Este endpoint devuelve una taquilla en particular a partir de su id
    """
    taquilla = logica.obtener_taquilla(id)
    return logica.respuesta_exitosa(taquilla)


@router.get("/taquillas") 
async def get_taquillas(ala: str = Query(default=""), piso: int = Query(default=0), pasillo: int = Query(default=0)):
    """
    Este endpoint devuelve todas las taquillas disponibles
    """
    taquillas = logica.obtener_todasTaquillas(ala, piso, pasillo)
    print("taquillas: ", taquillas)
    return logica.respuesta_exitosa(taquillas)

@router.post("/taquillas") 
async def post_taquilla(request: Request):
    """
    Crear una nueva taquilla con los datos recibidos en el body
    """
    #data es un diccionario con los datos que se reciben en el form data
    data = await request.json()
    print("data: ", data)
    taquilla = logica.crear_taquilla(data)
    return logica.respuesta_exitosa(taquilla)

#endpoint abrir taquilla
@router.get("/taquillas/{id_taquilla}/{id_usuario}")
def abrir_taquilla(id_taquilla:int, id_usuario:int):
    """
    Este endpoint permite abrir una taquilla a partir de una taquilla y usuario
    """
    resultado = logica.abrir_taquilla(id_taquilla, id_usuario)
    return logica.respuesta_exitosa(resultado)


#endpoint reservar
@router.put("/reservarTaquilla/{id_taquilla}/{id_usuario}")
def reservar_taquilla(id_taquilla:int, id_usuario:int):
    """
    Este endpoint permite reservar una taquilla a partir de una taquilla y usuario
    """
    resultado = logica.reservar_taquilla(id_taquilla, id_usuario)
    return logica.respuesta_exitosa(resultado)

@router.put("/cancelarTaquilla/{id_taquilla}/{id_usuario}")
def cancelar_taquilla(
    id_taquilla: int = Path(..., title="ID de la taquilla", description="El ID de la taquilla a cancelar"),
    id_usuario: int = Path(..., title="ID del usuario", description="El ID del usuario que cancela la taquilla")
) -> dict:
    """Este Endpoint cancela la reserva o la asignacion al alumno
    Returns:
        dict: Informacion de la taquilla cancelada
    """
    cancelar_taquilla = logica.cancelar_taquilla(id_taquilla, id_usuario)
    return cancelar_taquilla





@router.get("/consulta/")
async def consultita():
    """return logica.obtener_datos_como_json("select * FROM nombretabla", None)"""

@router.get("/holacaca/")
async def consultita():
    return "hola"

