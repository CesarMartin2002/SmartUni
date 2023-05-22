from decimal import Decimal
from fastapi import HTTPException
from fastapi import Request
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

#region printerrupt
class PrintInterruptException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

def printerrupt(message):
    """
    Interrumpe la ejecución de la función y devuelve el mensaje como respuesta al cliente.
    Muy útil para depurar código.
    """
    raise PrintInterruptException(str(message))
    # def decorator(func):
    #     async def wrapper(*args, **kwargs):
    #         # Obtener la solicitud actual del contexto
    #         request: Request = next(arg for arg in args if isinstance(arg, Request))

    #         # Interrumpir la ejecución y devolver el mensaje como respuesta
    #         raise PrintInterruptException(message)

    #     return wrapper

    # return decorator
#endregion

#region funciones de usuarios

def login(correo: str, password: str):
    #region obtener el usuario
    query = "SELECT * FROM alumno WHERE correo = %s AND password = %s" 
    parameters = (correo,password)
    usuario = db.realizar_consulta(query, params=parameters)
    if len(usuario) == 0:
        mensaje = f"El correo o la contraseña son incorrectos."
        respuesta_fallida(mensaje, 400)
    usuario = usuario[0]
    #endregion
    return usuario

def registrar_usuario( data: dict):
    correo = data["correo"]
    contrasena = data["password"]
    #region verificar que el correo no esté registrado
    query = "SELECT * FROM alumno WHERE correo = %s"
    parameters = ([correo])
    usuario = db.realizar_consulta(query, parameters)
    if len(usuario) > 0:
        mensaje = f"El correo {correo} ya está registrado."
        respuesta_fallida(mensaje, 400)
    # endregion

    # region insertar el usuario

    id_usuario = db.realizar_insercion("alumno", data)

    #endregion
    # printerrupt(data)
    query = "SELECT * FROM alumno WHERE id_alumno = %s"
    parameters = (id_usuario,)
    usuario = db.realizar_consulta(query, params=parameters)
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
    query = "SELECT * FROM taquilla WHERE id_taquilla = %s"
    parameters = (id_taquilla,)
    taquilla = db.realizar_consulta(query, params=parameters)
    if len(taquilla) == 0:
        respuesta_fallida(message="No se encontró la taquilla con id " + str(id_taquilla), code=404)
    return taquilla

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
        

def obtener_todasTaquillas(ala = "", piso = 0, pasillo = 0):
    query = "SELECT * FROM taquilla"
    params = []
    if ala != "":
        query += " WHERE ala = %s"
        params.append(ala)
    if piso != 0:
        if len(params) == 0:
            query += " WHERE piso = %s"
        else:
            query += " AND piso = %s"
        params.append(piso)
    if pasillo != 0:
        if len(params) == 0:
            query += " WHERE pasillo = %s"
        else:
            query += " AND pasillo = %s"
        params.append(pasillo)
    taquillas = db.realizar_consulta(query, params)
    return taquillas


def crear_taquilla(data : dict):
    taquilla = obtener_taquilla(db.realizar_insercion("taquilla", data))
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
    
#region funciones de las aulas

def obtener_aulas(ala,planta,numero):
    """
    Lista todas las aulas de la base de datos.
    """
    #region obtener las aulas de la base de datos
    query = "SELECT id_aula, laboratorio, planta, ala, num_aula FROM aula"
    params = []
    if ala != "":
        query += " WHERE ala = %s"
        params.append(ala)
    if planta != 0:
        if len(params) == 0:
            query += " WHERE planta = %s"
        else:
            query += " AND planta = %s"
        params.append(planta)
    if numero != 0:
        if len(params) == 0:
            query += " WHERE num_aula = %s"
        else:
            query += " AND num_aula = %s"
        params.append(numero)
    aulas = db.realizar_consulta(query, params)
    #endregion
    #region convertir los datos a un diccionario añadiendo los nombres de cada aula.
    for aula in aulas:
            letra_ala = aula['ala'][0]
            nombre_aula = f"{letra_ala}{'L' if aula['laboratorio'] else 'A'}{aula['num_aula']}"
            aula['nombre'] = nombre_aula
    #endregion
    return aulas

def obtener_aula(id_aula: int):
    """
    Obtiene el aula con el id especificado de la base de datos y lo devuelve como un diccionario
    """
    #region obtener el aula con el id especificado
    query = "SELECT * FROM aula WHERE id_aula = %s"
    parameters = (id_aula,)
    aula = db.realizar_consulta(query, params=parameters)
    #endregion

    #region verificar que se encontró el aula
    if len(aula) == 0:
        print("No se encontró el aula con id " + str(id_aula))
        mensaje = "No se encontró el aula con id " + str(id_aula)
        respuesta_fallida(mensaje, 404)
    #endregion

    #region convertir los datos a un diccionario añadiendo el nombre del aula.
    aula = aula[0]
    letra_ala = aula['ala'][0]
    nombre_aula = f"{letra_ala}{'L' if aula['laboratorio'] else 'A'}{aula['num_aula']}"
    aula['nombre'] = nombre_aula
    #endregion
    return aula

def insertar_aula(aula: dict):
    return obtener_aula(db.realizar_insercion("aula", aula))

def actualizar_aula(id: int, aula: dict):
    return obtener_aula(db.realizar_actualizacion("aula",id,aula))


#endregion

#region funciones de la cafeteria

def obtener_productos(filtro: str = ""):
    """
    Lista todos los productos de cafetería.
    """
    query = "SELECT id_producto, descripcion, precio FROM producto"
    params = []
    if filtro != "":
        query += " WHERE descripcion LIKE %s"
        params.append(f"%{filtro}%")
    #region obtener los productos de la base de datos
    productos = db.realizar_consulta(query,params)
    #endregion
    return productos

def obtener_producto(id_producto: int):
    """
    Obtiene el producto con el id especificado de la base de datos y lo devuelve como un diccionario
    """
    #region obtener el producto con el id especificado
    query = "SELECT * FROM producto WHERE id_producto = %s"
    parameters = (id_producto,)
    producto = db.realizar_consulta(query, params=parameters)
    #endregion

    #region verificar que se encontró el producto
    if len(producto) == 0:
        mensaje = "No se encontró el producto con id " + str(id_producto)
        respuesta_fallida(mensaje, 404)
    #endregion

    #region convertir los datos a un diccionario
    producto = producto[0]
    #endregion
    return producto

def obtener_pedidos():
    """
    Lista todos los pedidos de cafetería.
    """
    #region obtener los pedidos de la base de datos
    pedidos = db.realizar_consulta("SELECT * from vista_pedidos")
    #endregion
    for pedido in pedidos:
        pedido["productos_ids"] = pedido["productos_ids"].split("|")
        pedido["productos_ids"] = [int(id) for id in pedido["productos_ids"]]
        pedido["productos_descripciones"] = pedido["productos_descripciones"].split("|")
        pedido["estado"]= int(pedido["estado"])
    return pedidos

def obtener_pedido(id_pedido: int):
    """
    Obtiene el pedido con el id especificado de la base de datos y lo devuelve como un diccionario
    """
    #region obtener el pedido con el id especificado
    query = "SELECT * FROM vista_pedidos WHERE id_pedido = %s"
    parameters = (id_pedido,)
    pedido = db.realizar_consulta(query, params=parameters)
    #endregion

    #region verificar que se encontró el pedido
    if len(pedido) == 0:
        mensaje = "No se encontró el pedido con id " + str(id_pedido)
        respuesta_fallida(mensaje, 404)
    #endregion

    #region convertir los datos a un diccionario
    pedido = pedido[0]
    #hacemos un split de los productos para obtener una lista de ids de productos
    pedido["productos_ids"] = pedido["productos_ids"].split("|")
    pedido["productos_ids"] = [int(id) for id in pedido["productos_ids"]]
    pedido["productos_descripciones"] = pedido["productos_descripciones"].split("|")
    pedido["estado"]= int(pedido["estado"])
    #endregion
    return pedido

def crear_pedido(data: dict):
    """
    Crea un nuevo pedido. El parámetro data debe ser un diccionario que contenga la información del pedido.
    """
    #region verificar que el pedido tenga al menos un producto
    if len(data["productos"]) == 0:
        mensaje = "El pedido debe tener al menos un producto"
        respuesta_fallida(mensaje, 400)
    #endregion

    #region verificar que todos los productos existan
    for producto in data["productos"]:
        if obtener_producto(producto) is None:
            mensaje = f"No se encontró el producto con id {producto['id_producto']}"
            respuesta_fallida(mensaje, 404)
    #endregion

    #region insertar el pedido
    #creamos el diccionario con los datos del pedido
    data_pedido = {
        "id_alumno_alumno": data["id_alumno"],
        "estado": 0 #estado 0 es pendiente de aprobar
    }
    id_pedido = db.realizar_insercion("pedido", data_pedido)
    #endregion

    #region insertar los productos del pedido
    for producto in data["productos"]:
        data_pedido_producto = {
            "id_pedido": id_pedido,
            "id_producto": producto
        }
        db.realizar_insercion("pedido_producto", data_pedido_producto)
    #endregion

    #region obtener el pedido insertado
    pedido = obtener_pedido(id_pedido)
    #endregion

    return pedido

def actualizar_pedido(id_pedido: int, data: dict):
    """
    Actualiza el pedido con el id especificado. Solo estará permitido cambiar el estado.
    """
    #region obtener el pedido con el id especificado
    pedido = obtener_pedido(id_pedido)
    #endregion

    #region verificar que se encontró el pedido
    if pedido is None:
        mensaje = "No se encontró el pedido con id " + str(id_pedido)
        respuesta_fallida(mensaje, 404)
    #endregion
    #region verificar que solo nos haya enviado el estado y el id del alumno
    if len(data) != 2:
        mensaje = "Solo se puede enviar el estado y el id del alumno"
        respuesta_fallida(mensaje, 400)
    if "id_alumno" not in data:
        mensaje = "Debe enviar el id del alumno"
        respuesta_fallida(mensaje, 400)
    if "estado" not in data:
        mensaje = "Debe enviar el estado"
        respuesta_fallida(mensaje, 400)
    #endregion

    #region el pedido debe pertenecer al alumno que lo está modificando
    if pedido["id_alumno_alumno"] != data["id_alumno"]:
        mensaje = "El pedido no pertenece al alumno con id " + str(data["id_alumno"])
        respuesta_fallida(mensaje, 400)
    #endregion

    #region verificar que el estado sea válido
    if data["estado"] not in [0, 1, 2, 3]:
        mensaje = "El estado debe ser 0, 1, 2 o 3"
        respuesta_fallida(mensaje, 400)
    # if pedido["estado"] == 3:
    #     mensaje = "El pedido ya está completado y no se puede modificar"
    #     respuesta_fallida(mensaje, 400)
    if pedido["estado"] >=  data["estado"] :
        mensaje = "La modificación del estado no es válida"
        respuesta_fallida(mensaje, 400)
    #endregion

    #region actualizar el pedido
    data_pedido = {
        "estado": data["estado"]
    }
    db.realizar_actualizacion("pedido", id_pedido, data_pedido)
    #endregion

    #region obtener el pedido actualizado
    pedido = obtener_pedido(id_pedido)
    #endregion

    return pedido


#endregion

#region codigo antiguo que se borrará más adelante

#region funciones de la base de datos
# def get_connection():
#     conn = psycopg2.connect(
#         dbname='aotdlhvi',
#         user='aotdlhvi',
#         password='yJMYPFXps-4hLoQ2KO5iEzXs7o-bJxyJ',
#         host='trumpet.db.elephantsql.com',
#         port='5432')
#     if conn:
#         print('Conectado a la base de datos')
#     else:
#         print('Error al conectar a la base de datos')
#     return conn

# def realizar_consulta(sql:str, params=None):
#     if not sql.upper().startswith("SELECT"):
#         raise HTTPException(status_code=400, detail="La consulta debe ser de tipo SELECT")
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute(sql, params)
#     column_names = [desc[0] for desc in cursor.description]  # get the column names from the cursor
#     results = [dict(zip(column_names, row)) for row in cursor.fetchall()]  # convert each row to a dictionary
#     cursor.close()
#     conn.close()
#     return results

# def realizar_consulta_conexion(conn,sql:str, params=None):
#     if not sql.upper().startswith("SELECT"):
#         raise HTTPException(status_code=400, detail="La consulta debe ser de tipo SELECT")
#     cursor = conn.cursor()
#     try:
#         cursor.execute(sql, params)
#     except:
#         #print the error message
#         import traceback
#         traceback.print_exc()  # print the traceback of the error
#     column_names = [desc[0] for desc in cursor.description]  # get the column names from the cursor
#     results = [dict(zip(column_names, row)) for row in cursor.fetchall()]  # convert each row to a dictionary
#     cursor.close()
#     return results

# def realizar_insercion(nombre_tabla: str, data: dict):
#     conn = get_connection()
#     #region verificar que la tabla exista
#     sql = 'SELECT * FROM %s LIMIT 1'
#     table_name = AsIs(nombre_tabla)
#     params = (table_name,)
#     try:
#         realizar_consulta_conexion(conn, sql, params)
#     except:
#         return {"success": False, "code": 400, "message": f"La tabla {nombre_tabla} no existe"}
#     #endregion
    
#     #region establecer el valor de pk al nombre de la columna que es clave primaria
#     sql_pk = "SELECT kcu.column_name FROM information_schema.key_column_usage kcu JOIN information_schema.table_constraints tc ON kcu.constraint_name = tc.constraint_name WHERE kcu.table_name = %s AND tc.constraint_type = 'PRIMARY KEY';"
#     params = (nombre_tabla,)
#     pk = realizar_consulta_conexion(conn,sql_pk, params)[0]["column_name"]
#     #endregion

#     #region Verificar que la columna de la clave primaria no se haya enviado en el diccionario o que su valor sea None
#     if pk in data and data[pk] is not None:
#         return {"success": False, "code": 400, "message": f"No se puede enviar el valor de la clave primaria '{pk}'"}
#       # obtener los nombres de las columnas de la tabla
#     sql ='SELECT column_name FROM information_schema.columns WHERE table_name = %s'
#     columnas = realizar_consulta_conexion(conn,sql,params)
#     columnas = [columna["column_name"] for columna in columnas]
#     #endregion

#     #region revisar que todas las columnas enviadas existan en la tabla
#     for columna in data:
#         if columna not in columnas:
#             return {"success": False, "code": 400, "message": f"La columna '{columna}' no existe en la tabla '{nombre_tabla}'"}
#     #endregion

#     #region eliminar las columnas que no estén presentes en data
#     columnas = [columna for columna in columnas if columna in data]
#     #endregion

#     #region agregar columnas que no están presentes en el diccionario como None
#     valores = [data.get(columna, None) for columna in columnas]
#     #endregion

#     #region construir la consulta omitiendo la columna de la clave primaria
#     sql = f"INSERT INTO {nombre_tabla} ({', '.join(columna for columna in columnas if columna != pk)}) VALUES ({', '.join(['%s' for columna in columnas if columna != pk])})"
#     params = (*valores,)
#     try:
#         insertar_datos_conexion(conn,sql, valores)
#     except IntegrityError:
#         return {"success": False, "code": 400, "message": f"Ya existe un registro con la clave primaria '{data[pk]}'"}
#     #endregion

#     #region obtener el valor de la clave primaria del nuevo registro
#     sql = f"SELECT currval(pg_get_serial_sequence('{nombre_tabla}', '{pk}'))"
#     pk_value = realizar_consulta_conexion(conn, sql)[0]["currval"]
#     #endregion

#     #region devolver el registro insertado
#     query = 'SELECT * FROM %s WHERE %s = %s'
#     params = (table_name, AsIs(pk), pk_value)
#     resultado = realizar_consulta_conexion(conn, query, params)
#     #endregion
#     conn.close()
#     return resultado


# def insertar_datos_conexion(conn,sql, params=None):
#     #revisamos si es un insert y no un select o update o delete...
#     #if any of the params is None change it to NULL
#     params = [None if param is None else param for param in params]
#     if not sql.upper().startswith("INSERT"):
#         #si es un insert, obtenemos los datos
#         return "Error"
#     cursor = conn.cursor()
#     #print the query with the params
#     print(cursor.mogrify(sql, params))
#     cursor.execute(sql, params)
#     print("he insertado los datos")
#     #si no hay errores retornamos el id del registro insertado
#     conn.commit()
#     cursor.close()
#     return cursor.lastrowid

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

#endregion
