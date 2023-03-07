from fastapi import APIRouter
import logica

router = APIRouter()


@router.get("/probarInsert/")
async def get_casillero(id: int):
    diccionario = {"nombreColumna": 33,"nombre": "Casillero 1"}
    return logica.db.insertDB("nombreTabla", diccionario)
    