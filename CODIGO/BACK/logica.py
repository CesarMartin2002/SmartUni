from decimal import Decimal
import json
from logicaa.db import connect
import db

def json_serial(obj):
    """JSON serializer for objects not serializable by default json encoder"""
    if isinstance(obj, Decimal):
        return float(obj) if obj % 1 > 0 else int(obj)
    raise TypeError(f'Type {type(obj)} not serializable')



def obtener_datos_como_json(sql, params=None):
    # Llamamos a la función para realizar la consulta
    datos = db.realizar_consulta(sql, params)

    if datos == "Error":
        return "Error"
    
    # Obtenemos los nombres de las columnas
    nombres_columnas = [d[0] for d in datos.description]
    
    # Creamos una lista de diccionarios con los datos
    lista_datos = [dict(zip(nombres_columnas, d)) for d in datos]
    
    # Convertimos los Decimals a float o int
    for d in lista_datos:
        for k, v in d.items():
            if isinstance(v, Decimal):
                d[k] = float(v) if v % 1 > 0 else int(v)
    
    # Convertimos la lista de diccionarios a formato JSON
    datos_json = json.dumps(lista_datos, default=json_serial)
    
    return  json.loads(datos_json)



def obtener_casillero(id: int):
    return {"id": id, "nombre": "Casillero 1"}

# me devuelve la informacion de UNA taquilla
def obtener_taquilla(id: int):
    return {"id": id, "nombre": "Taquilla 1", "estado": "ocupado"}

# me devuelve la informacion de TODAS las taquillas
def obtener_todasTaquillas():
    taquillas = [{
            "id": 1,
            "nombre": "Taquilla 1",
            "estado": "ocupado"
        },
        {
            "id": 2,
            "nombre": "Taquilla 2",
            "estado": "ocupado"
        },
        {
            "id": 3,
            "nombre": "Taquilla 3",
            "estado": "libre"
        }]
    return taquillas

#
    