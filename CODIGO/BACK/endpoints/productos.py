from fastapi import APIRouter,Request
import logica

router = APIRouter()

@router.get("/cafeteria/productos")
async def get_productos():
    """
    Obtiene todos los productos que están disponibles en la cafetería
    """
    return logica.respuesta_exitosa(logica.obtener_productos())

@router.get("/cafeteria/productos/{id_producto}")
async def get_producto(id_producto: int):
    """
    Detalla toda la información de un producto en específico de la cafetería.
    """
    return logica.respuesta_exitosa(logica.obtener_producto(id_producto))
