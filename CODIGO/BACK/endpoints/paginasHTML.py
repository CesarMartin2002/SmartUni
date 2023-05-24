from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import logica

router = APIRouter()


@router.get("/")
def index():
    with open("FRONT/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)


@router.get("/registrarse")
def registrarse():
    with open("FRONT/registrarse.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)

@router.get("/menu")
def registrarse():
    with open("FRONT/bienvenida.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)

@router.get("/cafeteria")
def registrarse():
    with open("FRONT/cafeteria.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)

@router.get("/cafeteria/pedido")
def registrarse():
    with open("FRONT/cafeteria_pedido.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)

@router.get("/nfc")
def pagina_nfc():
    with open("FRONT/nfc.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)

@router.get("/notification")
def pagina_notif():
    with open("FRONT/notif.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)