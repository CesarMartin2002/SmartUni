from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import taquillas

app = FastAPI()

# Mount the static files directory at "/static"
def cargar_static(app):
    app.mount("/static", StaticFiles(directory="../FRONT/static"), name="static")

@app.get("/")
def index():
    with open("../FRONT/index.html", "r") as f:
        html = f.read()
    return HTMLResponse(html)


@app.get("/registrarse")
def registrarse():
    with open("../FRONT/registrarse.html", "r") as f:
        html = f.read()
    return HTMLResponse(html)

@app.get("/hola")
def miFuncion():
    return {"mensaje": "Hola mundoooooo"}

@app.get("/adios")
def miFuncion():
    return {"mensajeDespedida": "Adios amegoooaaaooo"}

cargar_static(app)