# todo esto es necesario para que funcione cualquier .py que se encuentre en la carpeta endpoints
from fastapi import APIRouter
import logica

router = APIRouter() 

# a partir de aquí se definen las rutas

@router.get("/taquilla/{id}")  # ruta que va a tener el endpoint. Puede ser de cualquier tipo. En este caso es de tipo GET. Para especificar el tipo de ruta se usa el decorador @router.TIPO
async def get_taquilla(id: int):    # función que va a ser ejecutada cuando se llame a la ruta. En este caso es una función asíncrona. El parámetro id es el que se va a recibir en la ruta
    """
    Este endpoint devuelve una taquilla en particular
    """
    print("id: ", id)
    taquilla = logica.obtener_taquilla(id)
    return taquilla

@router.get("/taquillas") 
async def get_taquillas():
    """
    Este endpoint devuelve todas las taquillas disponibles
    """
    taquillas = logica.obtener_todasTaquillas()
    return taquillas

# @router.put("/reservarTaquilla/{id_taquilla}/{id_usuario}")
# def reservar_taquilla(id_taquilla:int, id_usuario:int):
#     """Este endpoint reserva una taquilla a partir de una id dada

#     Args:
#         id_taquilla, id_usuario

#     Returns:
#         la informacion detallada de esa taquilla 
#     """
    





@router.get("/consulta/")
async def consultita():
    """return logica.obtener_datos_como_json("select * FROM nombretabla", None)"""

@router.get("/holacaca/")
async def consultita():
    return "hola"

