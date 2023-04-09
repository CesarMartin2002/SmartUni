from decimal import Decimal
import json
import db

def respuesta_exitosa(data):
    return {"success": True, "code": 200, "message": "OK", "data": data}

def respuesta_fallida(mensaje):
    return {"success": False, "code": 400, "message": mensaje}

def json_serial(obj):
    """JSON serializer for objects not serializable by default json encoder"""
    if isinstance(obj, Decimal):
        return float(obj) if obj % 1 > 0 else int(obj)
    raise TypeError(f'Type {type(obj)} not serializable')


def prueba_consulta ():
    sql = "SELECT * FROM taquilla"
    return db.realizar_consulta(sql)



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


#un grupo de taquillas peternece a un casillero
def obtener_casillero(id: int):
    return {"id": id, "nombre": "Casillero 1"}

# me devuelve la informacion de UNA taquilla
def obtener_taquilla(id_taquilla: int):
    # devolverla como un diccionario con sus propiedades (por ejemplo, {'id': 1, 'disponible': True, 'usuario': None})
    # Si no se encuentra ninguna taquilla con ese id, puedes devolver None o lanzar una excepción, dependiendo de tu preferencia.
    query = "SELECT * FROM taquilla WHERE id_taquilla = %s"
    params = (id_taquilla,)
    taquilla = db.realizar_consulta(query, params)
    if len(taquilla) == 0:
        return respuesta_fallida("No se encontró la taquilla con id " + str(id_taquilla))
    return respuesta_exitosa(taquilla)

def obtener_usuario_de_taquilla(id_taquilla: int):
    taquilla = obtener_taquilla(id_taquilla) 
    if taquilla['estado']: #si la taquilla esta disponible no retornas 
        return None
    else: #si esta ocupado es que tiene un alumno asociado
        return taquilla['usuario']
    
def actualizar_taquilla(id_taquilla: int, id_usuario :int):
    # Aquí implementar la lógica para actualizar la información de la taquilla en la base de datos
    # a partir del diccionario que se recibe como parámetro (por ejemplo, actualizando los valores de las propiedades
    # 'disponible' y 'usuario')
    taquilla = obtener_taquilla(id_taquilla)
    #si la taquilla esta disponible
    if taquilla['estado']:
        estado = False
        taquilla["estado"]=estado
        taquilla["usuario"]=id_usuario
        return taquilla
    else:
        return f"La taquilla {id_taquilla} no está disponible en este momento, esta asociado al alumno con id {id_usuario}."
        

def obtener_todasTaquillas():
    taquillas = db.realizar_consulta("SELECT * FROM taquilla")
    return respuesta_exitosa(taquillas)


#funcion para reservar una taquilla
def reservar_taquilla(id_taquilla: int, id_usuario: int):
    taquilla = obtener_taquilla(id_taquilla)
    if taquilla["estado"]:
        taquilla["estado"] = False
        taquilla["usuario"] = id_usuario
        actualizar_taquilla(taquilla, id_usuario)
        return f"La taquilla {id_taquilla} ha sido reservada por el usuario {id_usuario}."
    else:
        return f"La taquilla {id_taquilla} no está disponible en este momento."

#cancelar una taquilla
def cancelar_taquilla(id_taquilla: int, id_usuario: int):
    taquilla = obtener_taquilla(id_taquilla)
    if taquilla["usuario"] == id_usuario:
        taquilla["estado"] = True
        taquilla["usuario_id"] = None
        actualizar_taquilla(id_taquilla, id_usuario)
        return f"La taquilla {id_taquilla} ha sido CANCELADA por el usuario {id_usuario}."
    else:
        return f"La taquilla {id_taquilla} NO ESTA reservada por el usuario {id_usuario}."

    