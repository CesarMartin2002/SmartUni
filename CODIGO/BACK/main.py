from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from endpoints import taquillas, casillero, tests, paginasHTML, aulas, pruebas, sesion

app = FastAPI()

# Middleware to handle all exceptions
@app.middleware("http")
async def exception_handler(request: Request, call_next):
    try:
        response = await call_next(request)
    except RequestValidationError as exc:
        response = JSONResponse(content={"success": False, "code": 400, "message": "Validation Error", "errors": exc.errors()}, status_code=400)
    except HTTPException as exc:
        response = JSONResponse(content={"success": False, "code": exc.status_code, "message": str(exc.detail)}, status_code=exc.status_code)
    except Exception as exc:
        #print the traceback
        import traceback
        traceback.print_exc()
        response = JSONResponse(content={"success": False, "code": 500, "message": "Internal Server Error"}, status_code=500)
    return response

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

# Rutas para sesion
app.include_router(sesion.router)

# CORS settings
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Mount the static files directory at "/static"
app.mount("/static", StaticFiles(directory="FRONT/static"), name="static")