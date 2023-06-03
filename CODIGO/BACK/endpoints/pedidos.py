from fastapi import APIRouter,Request, Query
import logica

router = APIRouter()

@router.get("/cafeteria/pedidos")
async def get_pedidos(id_alumno: int = Query(default=-1)):
    """
    Obtiene todos los pedidos que se han realizado en la cafetería.
    """
    return logica.respuesta_exitosa(logica.obtener_pedidos(id_alumno))

@router.get("/cafeteria/pedidos/{id_pedido}")
async def get_pedido(id_pedido: int):
    """
    Detalla toda la información de un pedido en específico de la cafetería.
    """
    return logica.respuesta_exitosa(logica.obtener_pedido(id_pedido))

@router.post("/cafeteria/pedidos")
async def post_pedido(request: Request):
    """
    Este endpoint permite al usuario realizar un pedido.
    """
    data = await request.json()
    pedido = logica.crear_pedido(data)
    return logica.respuesta_exitosa(pedido)

@router.put("/cafeteria/pedidos/{id_pedido}")
async def put_pedido(id_pedido: int, request: Request):
    """
    Este endpoint permite a la cafetería actualizar un pedido.
    Se puede actualizar el estado del pedido.
    """
    data = await request.json()
    pedido = logica.actualizar_pedido(id_pedido, data)
    return logica.respuesta_exitosa(pedido)

@router.get("/cafeteria/pedidos/estrella")
async def get_pedido_estrella(id_alumno: int = Query(default=-1)):
    """
    Detalla la descripción del producto más pedido.
    """
    return logica.respuesta_exitosa(logica.obtener_pedido_estrella(id_alumno))
