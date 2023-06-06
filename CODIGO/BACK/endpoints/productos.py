from fastapi import APIRouter,Request
from fastapi import Query
import logica

router = APIRouter(tags=["Productos"])

@router.get("/cafeteria/productos")
async def get_productos(filtro: str = Query(default="")):
    """
    Obtiene todos los productos que están disponibles en la cafetería.
    Puede filtrar los productos según su nombre, dado un parámetro de búsqueda.
    Si no se especifica un parámetro de búsqueda, se obtienen todos los productos.
    """
    return logica.respuesta_exitosa(logica.obtener_productos(filtro))

@router.get("/cafeteria/productos/{id_producto}")
async def get_producto(id_producto: int):
    """
    Detalla toda la información de un producto en específico de la cafetería.
    """
    return logica.respuesta_exitosa(logica.obtener_producto(id_producto))