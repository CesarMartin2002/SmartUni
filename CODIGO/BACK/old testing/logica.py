from enum import Enum
from typing import Optional, List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Form, Response, status



# Definición de modelos de datos

class Ala(str, Enum):
    NORTE = "norte"
    SUR = "sur"
    ESTE = "este"
    OESTE = "oeste"

class Taquilla(BaseModel):
    id: int
    ocupada: bool = False
    alumno: Optional[int]
    ala: Ala
    planta: int
    pasillo: int

    def __init__(self, id: int, ala: Ala, planta: int, pasillo: int, ocupada: bool = False, alumno: Optional[int] = None):
        super().__init__(id=id, ocupada=ocupada, alumno=alumno, ala=ala, planta=planta, pasillo=pasillo)

# Inicialización de la lista de taquillas en memoria
taquillas = [
    Taquilla(id=1, ala=Ala.NORTE, planta=1, pasillo=1),
    Taquilla(id=2, ala=Ala.NORTE, planta=1, pasillo=2),
    Taquilla(id=3, ala=Ala.SUR, planta=1, pasillo=1),
    Taquilla(id=4, ala=Ala.SUR, planta=1, pasillo=2),
    Taquilla(id=5, ala=Ala.ESTE, planta=1, pasillo=1),
    Taquilla(id=6, ala=Ala.ESTE, planta=1, pasillo=2),
    Taquilla(id=7, ala=Ala.OESTE, planta=1, pasillo=1),
    Taquilla(id=8, ala=Ala.OESTE, planta=1, pasillo=2),
    Taquilla(id=9, ala=Ala.NORTE, planta=2, pasillo=1),
    Taquilla(id=10, ala=Ala.NORTE, planta=2, pasillo=2),
    Taquilla(id=11, ala=Ala.SUR, planta=2, pasillo=1),
    Taquilla(id=12, ala=Ala.SUR, planta=2, pasillo=2),
    Taquilla(id=13, ala=Ala.ESTE, planta=2, pasillo=1),
    Taquilla(id=14, ala=Ala.ESTE, planta=2, pasillo=2),
    Taquilla(id=15, ala=Ala.OESTE, planta=2, pasillo=1),
    Taquilla(id=16, ala=Ala.OESTE, planta=2, pasillo=2)
]

def listar_taquillas(planta: Optional[int] = None, ala: Optional[Ala] = None, pasillo: Optional[int] = None) -> List[Taquilla]:
    lista_filtrada = taquillas
    if planta is not None:
        lista_filtrada = [t for t in lista_filtrada if t.planta == planta]
    if ala is not None:
        lista_filtrada = [t for t in lista_filtrada if t.ala == ala]
    if pasillo is not None:
        lista_filtrada = [t for t in lista_filtrada if t.pasillo == pasillo]
    return lista_filtrada


def obtener_taquilla(id: int) -> Taquilla:
    taquilla = next((t for t in taquillas if t.id == id), None)
    if taquilla is None:
        raise HTTPException(status_code=404, detail="Taquilla no encontrada")
    return taquilla


def crear_taquilla(ala: Ala, planta:int, pasillo:int) -> Taquilla:
    taquilla = Taquilla(taquillas[-1].id+1, ala=ala, planta=planta, pasillo=pasillo)
    taquillas.append(taquilla)
    return taquilla


def actualizar_taquilla(id: int, alumno: Optional[int] = None) -> Taquilla:
    taquilla = next((t for t in taquillas if t.id == id), None)
    if taquilla is None:
        raise HTTPException(status_code=404, detail="Taquilla no encontrada")
    taquilla.ocupada = alumno is not None
    taquilla.alumno = alumno
    return taquilla

def eliminar_taquilla(id: int) -> List[Taquilla]:
    taquilla = next((t for t in taquillas if t.id == id), None)
    if taquilla is None:
        raise HTTPException(status_code=404, detail="Taquilla no encontrada")

    elif taquilla.ocupada:
        raise HTTPException(status_code=400, detail="La taquilla está ocupada")
    else:
        taquillas.remove(taquilla)
        return listar_taquillas()
