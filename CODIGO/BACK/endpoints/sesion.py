from fastapi import APIRouter,Request
import logica

router = APIRouter()

@router.post("/login")
async def login(request: Request):
    """
    Este endpoint permite al usuario loguearse
    """
    data = await request.json()
    print("data: ", data)
    correo = data["correo"]
    contrasena = data["password"]
    usuario = logica.login(correo, contrasena)
    return logica.respuesta_exitosa(usuario)