from fastapi import APIRouter,Request
import logica

router = APIRouter()


@router.post("/signup")
async def registro(request: Request):
    """
    Este endpoint permite al usuario registrarse
    """
    data = await request.json()
    print("data: ", data)
    correo = data["correo"]
    contrasena = data["password"]
    usuario = logica.registro(correo, contrasena)
    return logica.respuesta_exitosa(usuario)