from fastapi import APIRouter,Request
import logica

router = APIRouter()

@router.get("/nfc")
async def nfc():
    return logica.respuesta_exitosa(logica.obtener_nfcs())

@router.get("/nfc/{id}")
async def nfc(id: int):
    return logica.respuesta_exitosa(logica.obtener_nfc(id))

@router.post("/nfc")
async def post_nfc(request: Request):
    data = await request.json()
    id_nfc = logica.insertar_nfc(data)
    return logica.respuesta_exitosa(logica.obtener_nfc(id_nfc))

@router.put("/nfc/{id}")
async def put_nfc(id: int, request: Request):
    data = await request.json()
    return logica.respuesta_exitosa(logica.actualizar_nfc(id, data))

@router.put("/cafeteria/pedidos/nfc/{id_pedido}")
async def put_pedido_nfc(id_pedido: int, request: Request):
    data = await request.json()
    pedido = logica.actualizar_pedido_nfc(id_pedido, data)
    return logica.respuesta_exitosa(pedido)