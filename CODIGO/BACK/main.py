from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import PlainTextResponse

#importamos todos los endpoints
from endpoints import taquillas, casillero, paginasHTML, aulas, sesion, productos, pedidos, nfc
import logica

app = FastAPI()

#region manejo de errores
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

@app.exception_handler(logica.CustomException)
async def custom_exception_handler(request, exc):
    print("\nERROR CAPTURADO:\nCode: ", exc.code, "\nMessage: ", str(exc), "\n")
    return JSONResponse(
        status_code=exc.code,
        content={"success": False, "code": exc.code, "message": str(exc)}
    )
#endregion

#region manejo de printerrupt
@app.exception_handler(logica.PrintInterruptException)
async def print_interrupt_exception_handler(request, exc):
    return_message = "PRINTERRUPT:\n\n"+exc.message
    print(return_message)
    return PlainTextResponse(return_message)
    # return JSONResponse(
    #     status_code=200,
    #     content={"PRINTERRUPT": exc.message}
    # )
#endregion

#region rutas de los endpoints
# Rutas para taquillas
app.include_router(taquillas.router)

# Rutas para casillero
app.include_router(casillero.router)

# Rutas para paginas HTML
app.include_router(paginasHTML.router)

# Rutas para aulas
app.include_router(aulas.router)

# Rutas para sesion
app.include_router(sesion.router)

# Rutas para productos
app.include_router(productos.router)

# Rutas para pedidos
app.include_router(pedidos.router)
#endregion

#region rutas para nfc
app.include_router(nfc.router)
#endregion

#region cosas que no entiendo del todo pero que prefiero no tocar por si acaso
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
#endregion

#Mount the static files directory at "/static"
#Esto se usa básicamente para poder tener todo el fonrtend en una carpeta aparte y que el backend pueda acceder a ella
app.mount("/static", StaticFiles(directory="FRONT/static"), name="static")