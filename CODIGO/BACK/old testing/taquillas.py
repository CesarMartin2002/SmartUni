from enum import Enum
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Form, Response, status
from pydantic import BaseModel
import logica

app = FastAPI()

@app.get("/taquilla")
async def get_taquillas(planta: Optional[int] = None, ala: Optional[str] = None, pasillo: Optional[int] = None):
    """
    Este endpoint retorna las taquillas que se encuentran en el sistema, con la opción de filtrar por planta, ala y pasillo.

    ## Parameters
    - **planta**: Planta en la que se encuentran las taquillas.
    - **ala**: Ala en la que se encuentran las taquillas.
    - **pasillo**: Pasillo en el que se encuentran las taquillas.

    ## Returns
    - **200 OK** - La lista de taquillas filtrada.
    """
    if planta is not None and not isinstance(planta, int):
        raise HTTPException(status_code=400, detail="Planta debe ser un entero")
    if ala is not None and not isinstance(ala, str):
        raise HTTPException(status_code=400, detail="Ala debe ser una cadena")
    if pasillo is not None and pasillo not in [1, 2]:
        raise HTTPException(status_code=400, detail="Pasillo debe ser 1 o 2")

    taquillas = logica.listar_taquillas(planta=planta, ala=ala, pasillo=pasillo)
    return taquillas


@app.get("/taquilla/{id}")
async def obtener_taquilla(id: int) -> logica.Taquilla:
    """
    Este point retornará los valores de una taquilla en concreto.

    ## Parameters
    - **id**: Identificador de la taquilla.

    ## Returns
    - **200 OK** - La taquilla.
    - **404 Not Found** - La taquilla no existe.
    """
    taquilla = logica.obtener_taquilla(id)
    return taquilla



@app.post("/taquilla")
async def crear_taquilla(
    ala: str = Form(None),
    planta: int = Form(None),
    pasillo: int = Form(None)
) -> logica.Taquilla:
    """
    Crea una nueva taquilla en el sistema.

    ## Parameters
    - **ala**: Ala en la que se encuentra la taquilla.
    - **planta**: Planta en la que se encuentra la taquilla.
    - **pasillo**: Pasillo en el que se encuentra la taquilla.

    ## Returns
    - **201 Created** - La taquilla ha sido creada correctamente.
    - **400 Bad Request** - La taquilla ya existe o los datos introducidos no son válidos.
    """
    if not ala or not isinstance(planta, int) or not pasillo in [1,2]:
        raise HTTPException(status_code=400, detail="Datos introducidos no válidos")


    try:
        nueva_taquilla=logica.crear_taquilla(ala, planta, pasillo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return nueva_taquilla

@app.put("/taquilla/{id}")
async def actualizar_taquilla(id: int, alumno: Optional[int] = Form(None)) -> logica.Taquilla:
    """
    Actualiza el valor de una taquilla diciendo sídicha taquilla está siendo ocupada por un alumno o no.
    En el caso de que Se envíe en los formatos para el identificador de un alumno, se actualizará el valor de la taquilla a ocupada y se asignará el identificador del alumno a la taquilla.
    En el caso de que no se envíe ningún identificador de alumno, se actualizará el valor de la taquilla a desocupada y se eliminará el identificador del alumno de la taquilla.

    ## Parameters
    - **id**: Identificador de la taquilla a actualizar.
    - **alumno**: Identificador del alumno que ocupa la taquilla.

    ## Returns
    - **200 OK** - La taquilla ha sido actualizada correctamente.
    - **404 Not Found** - La taquilla no existe o el alumno no existe.
    """
    taquilla = logica.actualizar_taquilla(id, alumno)
    return taquilla

@app.delete("/taquilla/{id}")
async def eliminar_taquilla(id: int) -> Response:
    """
    Elimina una taquilla en el sistema.

    ## Parameters
    - **id**: Identificador de la taquilla a eliminar.

    ## Returns
    - **204 No Content** - La taquilla ha sido eliminada correctamente.
    - **404 Not Found** - La taquilla no existe o no se puede eliminar.
    """
    try:
        taquillas=logica.eliminar_taquilla(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    # return Response(status_code=status.HTTP_204_NO_CONTENT, taquillas)
    return {"taquillas": taquillas}

