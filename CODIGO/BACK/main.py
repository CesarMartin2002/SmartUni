from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from endpoints import taquillas, casillero, tests, paginasHTML, aulas, pruebas

app = FastAPI()

# Rutas para taquillas
app.include_router(taquillas.router)

# Rutas para casillero
app.include_router(casillero.router)

# Rutas para tests
app.include_router(tests.router)

# Rutas para paginas HTML
app.include_router(paginasHTML.router)

# Rutas para aulas
app.include_router(aulas.router)

# Rutas para pruebas
app.include_router(pruebas.router)


#Mount the static files directory at "/static"
app.mount("/static", StaticFiles(directory="FRONT/static"), name="static")
