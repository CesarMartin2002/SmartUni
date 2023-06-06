from fastapi import APIRouter,Request
import logica

router = APIRouter(tags=["Manejo NFC"])

@router.get("/nfc")
async def nfc():
    """
    Obtiene todos los NFCs que están registrados en la cafetería.
    """
    return logica.respuesta_exitosa(logica.obtener_nfcs())

@router.get("/nfc/{id}")
async def nfc(id: int):
    """
    Detalla toda la información de un NFC en específico de la cafetería.
    """
    return logica.respuesta_exitosa(logica.obtener_nfc(id))

@router.post("/nfc")
async def post_nfc(request: Request):
    """
    Este endpoint permite a la cafetería registrar un NFC.
    """
    data = await request.json()
    id_nfc = logica.insertar_nfc(data)
    return logica.respuesta_exitosa(logica.obtener_nfc(id_nfc))

@router.put("/nfc/{id}")
async def put_nfc(id: int, request: Request):
    """
    Este endpoint permite a la cafetería actualizar un NFC.
    """
    data = await request.json()
    return logica.respuesta_exitosa(logica.actualizar_nfc(id, data))

@router.put("/cafeteria/pedidos/nfc/{id_pedido}")
async def put_pedido_nfc(id_pedido: int, request: Request):
    """
    Este endpoint permite a la cafetería o a los alumnos actualizar un pedido a partir del escanéo de un NFC.
    Se puede actualizar el estado del pedido.
    En concreto, los alumnos pueden actualizar el estado del pedido a 3 -> "Entregado (comiendo)".
    La cafetería puede actualizar el estado del pedido a 4 -> "Finalizado (comido)" lo cual desvincula el NFC del pedido y lo deja disponible para ser usado en otro pedido.
    """

    data = await request.json()
    pedido = logica.actualizar_pedido_nfc(id_pedido, data)
    return logica.respuesta_exitosa(pedido)