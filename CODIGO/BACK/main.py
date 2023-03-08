from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from logicaa import db
from endpoints import taquillas, casillero, tests

app = FastAPI()

# Rutas para taquillas
app.include_router(taquillas.router)

# Rutas para casillero
app.include_router(casillero.router)

# Rutas para tests
app.include_router(tests.router)

# Realizar conexión a la base de datos
db.connect()

# Mount the static files directory at "/static"
def cargar_static(app):
    app.mount("/static", StaticFiles(directory="../FRONT/static"), name="static")

app.mount("/static", StaticFiles(directory="../FRONT/static"), name="static")


@app.get("/")
def index():
    with open("../FRONT/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)


@app.get("/registrarse")
def registrarse():
    with open("../FRONT/registrarse.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)

@app.get("/menu")
def registrarse():
    with open("../FRONT/bienvenida.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)

@app.get("/cafeteria")
def registrarse():
    with open("../FRONT/cafeteria.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)

@app.get("/cafeteria/pedido")
def registrarse():
    with open("../FRONT/cafeteria_pedido.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)