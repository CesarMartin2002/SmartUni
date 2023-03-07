# todo esto es necesario para que funcione cualquier .py que se encuentre en la carpeta endpoints
from fastapi import APIRouter
import logica

router = APIRouter()

# a partir de aquí se definen las rutas

@router.get("/taquillas/{id}")  # ruta que va a tener el endpoint. Puede ser de cualquier tipo. En este caso es de tipo GET. Para especificar el tipo de ruta se usa el decorador @router.TIPO
async def get_taquilla(id: int):    # función que va a ser ejecutada cuando se llame a la ruta. En este caso es una función asíncrona. El parámetro id es el que se va a recibir en la ruta
    """
    """
    print("id: ", id)
    taquilla = logica.obtener_taquilla(id)
    return taquilla

@router.get("/imei/{imei}")
def get_taquilla(imei: str):
    print("imei: ", imei)
    return imei

@router.get("/consulta/")
async def consultita():
    return logica.obtener_datos_como_json("select * FROM nombretabla", None)

@router.get("/holacaca/")
async def consultita():
    return "hola"

@router.get("/djmariio/")
async def consultita():
    return "soy retrasadoooo"