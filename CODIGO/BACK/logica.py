from decimal import Decimal
from fastapi import HTTPException
import json
import db


#region Funciones de respuesta
class CustomException(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code

def respuesta_exitosa(data):
    return {"success": True, "code": 200, "message": "OK", "data": data}

def respuesta_fallida(mensaje, code=400):
    raise CustomException(message=mensaje, code=code)

#endregion

#region funciones de la base de datos
def get_connection():
    conn = psycopg2.connect(
        dbname='aotdlhvi',
        user='aotdlhvi',
        password='yJMYPFXps-4hLoQ2KO5iEzXs7o-bJxyJ',
        host='trumpet.db.elephantsql.com',
        port='5432')
    if conn:
        print('Conectado a la base de datos')
    else:
        print('Error al conectar a la base de datos')
    return conn

def realizar_consulta(sql:str, params=None):
    if not sql.upper().startswith("SELECT"):
        raise HTTPException(status_code=400, detail="La consulta debe ser de tipo SELECT")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    column_names = [desc[0] for desc in cursor.description]  # get the column names from the cursor
    results = [dict(zip(column_names, row)) for row in cursor.fetchall()]  # convert each row to a dictionary
    cursor.close()
    conn.close()
    return results

def realizar_consulta_conexion(conn,sql:str, params=None):
    if not sql.upper().startswith("SELECT"):
        raise HTTPException(status_code=400, detail="La consulta debe ser de tipo SELECT")
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params)
    except:
        #print the error message
        import traceback
        traceback.print_exc()  # print the traceback of the error
    column_names = [desc[0] for desc in cursor.description]  # get the column names from the cursor
    results = [dict(zip(column_names, row)) for row in cursor.fetchall()]  # convert each row to a dictionary
    cursor.close()
    return results

def realizar_insercion(nombre_tabla: str, data: dict):
    conn = get_connection()
    #region verificar que la tabla exista
    sql = 'SELECT * FROM %s LIMIT 1'
    table_name = AsIs(nombre_tabla)
    params = (table_name,)
    try:
        realizar_consulta_conexion(conn, sql, params)
    except:
        return {"success": False, "code": 400, "message": f"La tabla {nombre_tabla} no existe"}
    #endregion
    
    #region establecer el valor de pk al nombre de la columna que es clave primaria
    sql_pk = "SELECT kcu.column_name FROM information_schema.key_column_usage kcu JOIN information_schema.table_constraints tc ON kcu.constraint_name = tc.constraint_name WHERE kcu.table_name = %s AND tc.constraint_type = 'PRIMARY KEY';"
    params = (nombre_tabla,)
    pk = realizar_consulta_conexion(conn,sql_pk, params)[0]["column_name"]
    #endregion

    #region Verificar que la columna de la clave primaria no se haya enviado en el diccionario o que su valor sea None
    if pk in data and data[pk] is not None:
        return {"success": False, "code": 400, "message": f"No se puede enviar el valor de la clave primaria '{pk}'"}
      # obtener los nombres de las columnas de la tabla
    sql ='SELECT column_name FROM information_schema.columns WHERE table_name = %s'
    columnas = realizar_consulta_conexion(conn,sql,params)
    columnas = [columna["column_name"] for columna in columnas]
    #endregion

    #region revisar que todas las columnas enviadas existan en la tabla
    for columna in data:
        if columna not in columnas:
            return {"success": False, "code": 400, "message": f"La columna '{columna}' no existe en la tabla '{nombre_tabla}'"}
    #endregion

    #region eliminar las columnas que no estén presentes en data
    columnas = [columna for columna in columnas if columna in data]
    #endregion

    #region agregar columnas que no están presentes en el diccionario como None
    valores = [data.get(columna, None) for columna in columnas]
    #endregion

    #region construir la consulta omitiendo la columna de la clave primaria
    sql = f"INSERT INTO {nombre_tabla} ({', '.join(columna for columna in columnas if columna != pk)}) VALUES ({', '.join(['%s' for columna in columnas if columna != pk])})"
    params = (*valores,)
    try:
        insertar_datos_conexion(conn,sql, valores)
    except IntegrityError:
        return {"success": False, "code": 400, "message": f"Ya existe un registro con la clave primaria '{data[pk]}'"}
    #endregion

    #region obtener el valor de la clave primaria del nuevo registro
    sql = f"SELECT currval(pg_get_serial_sequence('{nombre_tabla}', '{pk}'))"
    pk_value = realizar_consulta_conexion(conn, sql)[0]["currval"]
    #endregion

    #region devolver el registro insertado
    query = 'SELECT * FROM %s WHERE %s = %s'
    params = (table_name, AsIs(pk), pk_value)
    resultado = realizar_consulta_conexion(conn, query, params)
    #endregion
    conn.close()
    return resultado


def insertar_datos_conexion(conn,sql, params=None):
    #revisamos si es un insert y no un select o update o delete...
    #if any of the params is None change it to NULL
    params = [None if param is None else param for param in params]
    if not sql.upper().startswith("INSERT"):
        #si es un insert, obtenemos los datos
        return "Error"
    cursor = conn.cursor()
    #print the query with the params
    print(cursor.mogrify(sql, params))
    cursor.execute(sql, params)
    print("he insertado los datos")
    #si no hay errores retornamos el id del registro insertado
    conn.commit()
    cursor.close()
    return cursor.lastrowid

#endregion

#region funciones de usuarios

def login(correo: str, password: str):
    #region obtener el usuario
    query = "SELECT * FROM alumno WHERE correo = %s AND password = %s" 
    parameters = (correo,password)
    usuario = db.realizar_consulta(query, params=parameters)
    if len(usuario) == 0:
        raise HTTPException(status_code=400, detail="El correo o la contraseña son incorrectos")
    usuario = usuario[0]
    #endregion
    return usuario

def registrar_usuario( data: dict):
    correo = data["correo"]
    contrasena = data["password"]
    #region verificar que el correo no esté registrado
    query = "SELECT * FROM alumno WHERE correo = \"%s\""
    parameters = (correo)
    usuario = db.realizar_consulta(query, parameters)
    if len(usuario) > 0:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    # endregion

    # region insertar el usuario
    query = "INSERT INTO alumno (nombre, correo, password) VALUES (%s, %s, %s)"
    parameters = (correo, contrasena)
    return db.realizar_insercion("alumno", data)

    #endregion

    #region obtener el usuario recién insertado
    query = "SELECT * FROM alumno WHERE correo = %s"
    parameters = (correo)
    usuario = db.realizar_consulta(query, params=parameters)
    #endregion

    return usuario[0]


#endregion

#region funciones de taquillas

#un grupo de taquillas peternece a un casillero
def obtener_casillero(id: int):
    return {"id": id, "nombre": "Casillero 1"}

# me devuelve la informacion de UNA taquilla
def obtener_taquilla(id_taquilla: int):
    # devolverla como un diccionario con sus propiedades (por ejemplo, {'id': 1, 'disponible': True, 'usuario': None})
    # Si no se encuentra ninguna taquilla con ese id, se debe retornar un error (por ejemplo, {'success': False, 'message': 'No se encontró la taquilla con id 1'})
    try:
        query = "SELECT * FROM taquilla WHERE id_taquilla = %s"
        parameters = (id_taquilla,)
        taquilla = db.realizar_consulta(query, params=parameters)
        if len(taquilla) == 0:
            raise CustomException(message="No se encontró la taquilla con id " + str(id_taquilla), code=404)
        return taquilla
    except CustomException as e:
        return HTTPException(status_code=e.code, detail=e.message)

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
    return taquillas


def crear_taquilla(data : dict):
    taquilla = db.realizar_insercion("taquilla", data)
    return taquilla

#funcion para abrir una taquilla
def abrir_taquilla(id_taquilla: int, id_usuario: int):
    try:
        # Obtener la taquilla con el id especificado
        query = "SELECT * FROM taquilla WHERE id_taquilla = %s"
        parameters = (id_taquilla,)
        taquilla = db.realizar_consulta(query, params=parameters)

        # Verificar que se encontró la taquilla
        if len(taquilla) == 0:
            raise CustomException(message="No se encontró la taquilla con id " + str(id_taquilla), code=404)

        # Verificar que la taquilla está disponible
        if not taquilla[0]['disponible']:
            raise CustomException(message="La taquilla con id " + str(id_taquilla) + " no está disponible", code=400)

        # Actualizar la taquilla con el id del usuario que la abrió
        query = "UPDATE taquilla SET disponible = %s, usuario_id = %s WHERE id_taquilla = %s"
        parameters = (False, id_usuario, id_taquilla)
        db.realizar_modificacion(query, params=parameters)

        # Obtener la taquilla actualizada
        query = "SELECT * FROM taquilla WHERE id_taquilla = %s"
        parameters = (id_taquilla,)
        taquilla = db.realizar_consulta(query, params=parameters)

        return taquilla[0]

    except CustomException as e:
        raise HTTPException(status_code=e.code, detail=e.message)


#funcion para reservar una taquilla
def reservar_taquilla(id_taquilla: int, id_usuario: int):
    try:
        # Obtener la taquilla con el id especificado
        query = "SELECT * FROM taquilla WHERE id_taquilla = %s"
        parameters = (id_taquilla,)
        taquilla = db.realizar_consulta(query, params=parameters)

        # Verificar que se encontró la taquilla
        if len(taquilla) == 0:
            raise CustomException(message="No se encontró la taquilla con id " + str(id_taquilla), code=404)

        # Verificar que la taquilla está disponible
        if not taquilla[0]['disponible']:
            raise CustomException(message="La taquilla con id " + str(id_taquilla) + " no está disponible", code=400)

        # Actualizar la taquilla con el id del usuario que la reservó
        query = "UPDATE taquilla SET disponible = %s, usuario_id = %s WHERE id_taquilla = %s"
        parameters = (False, id_usuario, id_taquilla)
        db.realizar_modificacion(query, params=parameters)

        return f"La taquilla {id_taquilla} ha sido reservada por el usuario {id_usuario}."

    except CustomException as e:
        raise HTTPException(status_code=e.code, detail=e.message)

# def reservar_taquilla(id_taquilla: int, id_usuario: int):
#     taquilla = obtener_taquilla(id_taquilla)
#     if taquilla["estado"]:
#         taquilla["estado"] = False
#         taquilla["usuario"] = id_usuario
#         actualizar_taquilla(taquilla, id_usuario)
#         return f"La taquilla {id_taquilla} ha sido reservada por el usuario {id_usuario}."
#     else:
#         return f"La taquilla {id_taquilla} no está disponible en este momento."

#cancelar una taquilla
def cancelar_taquilla(id_taquilla: int, id_usuario: int):
    try:
        # Obtener la taquilla con el id especificado
        query = "SELECT * FROM taquilla WHERE id_taquilla = %s"
        parameters = (id_taquilla,)
        taquilla = db.realizar_consulta(query, params=parameters)

        # Verificar que se encontró la taquilla
        if len(taquilla) == 0:
            raise CustomException(message="No se encontró la taquilla con id " + str(id_taquilla), code=404)

        # Verificar que la taquilla está reservada por el usuario que la quiere cancelar
        if taquilla[0]['usuario_id'] != id_usuario:
            raise CustomException(message="La taquilla con id " + str(id_taquilla) + " NO ESTÁ reservada por el usuario " + str(id_usuario), code=400)

        # Actualizar la taquilla como disponible y sin usuario
        query = "UPDATE taquilla SET disponible = %s, usuario_id = %s WHERE id_taquilla = %s"
        parameters = (True, None, id_taquilla)
        db.realizar_modificacion(query, params=parameters)

        return f"La taquilla {id_taquilla} ha sido CANCELADA por el usuario {id_usuario}."

    except CustomException as e:
        raise HTTPException(status_code=e.code, detail=e.message)

# def cancelar_taquilla(id_taquilla: int, id_usuario: int):
#     taquilla = obtener_taquilla(id_taquilla)
#     if taquilla["usuario"] == id_usuario:
#         taquilla["estado"] = True
#         taquilla["usuario_id"] = None
#         actualizar_taquilla(id_taquilla, id_usuario)
#         return f"La taquilla {id_taquilla} ha sido CANCELADA por el usuario {id_usuario}."
#     else:
#         return f"La taquilla {id_taquilla} NO ESTA reservada por el usuario {id_usuario}."
#endregion
    

def prueba_consulta():
    taquilla_prueba = obtener_taquilla(1)
    #eliminar el id_taquilla para que no se intente insertar
    del taquilla_prueba["id_taquilla"]
    resultado_insercion = db.realizar_insercion('taquilla', taquilla_prueba)
    return respuesta_exitosa(resultado_insercion)

#    def json_serial(obj):
#     """JSON serializer for objects not serializable by default json encoder"""
#     if isinstance(obj, Decimal):
#         return float(obj) if obj % 1 > 0 else int(obj)
#     raise TypeError(f'Type {type(obj)} not serializable')


# def obtener_datos_como_json(sql, params=None):
#     # Llamamos a la función para realizar la consulta
#     datos = db.realizar_consulta(sql, params)

#     if datos == "Error":
#         return "Error"
    
#     # Obtenemos los nombres de las columnas
#     nombres_columnas = [d[0] for d in datos.description]
    
#     # Creamos una lista de diccionarios con los datos
#     lista_datos = [dict(zip(nombres_columnas, d)) for d in datos]
    
#     # Convertimos los Decimals a float o int
#     for d in lista_datos:
#         for k, v in d.items():
#             if isinstance(v, Decimal):
#                 d[k] = float(v) if v % 1 > 0 else int(v)
    
#     # Convertimos la lista de diccionarios a formato JSON
#     datos_json = json.dumps(lista_datos, default=json_serial)
    
#     return  json.loads(datos_json)