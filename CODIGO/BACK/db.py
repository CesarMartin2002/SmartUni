import psycopg2
# AsIs from psycopg2.sql
from psycopg2.extensions import AsIs
from psycopg2 import IntegrityError
from fastapi import HTTPException
import logica
import json

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
        mensaje = "La consulta debe ser de tipo SELECT"
        logica.respuesta_fallida(mensaje)
    conn = get_connection()
    cursor = conn.cursor()
    print("sql: ", sql)
    print("params: ", params)
    cursor.execute(sql, params)
    column_names = [desc[0] for desc in cursor.description]  # get the column names from the cursor
    results = [dict(zip(column_names, row)) for row in cursor.fetchall()]  # convert each row to a dictionary
    cursor.close()
    conn.close()
    return results

def realizar_consulta_conexion(conn,sql:str, params=None):
    if not sql.upper().startswith("SELECT"):
        mensaje = "La consulta debe ser de tipo SELECT"
        logica.respuesta_fallida(mensaje)
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
        mensaje = f"La tabla {nombre_tabla} no existe"
        logica.respuesta_fallida(mensaje)
    #endregion
    
    #region establecer el valor de pk al nombre de la columna que es clave primaria
    sql_pk = "SELECT kcu.column_name FROM information_schema.key_column_usage kcu JOIN information_schema.table_constraints tc ON kcu.constraint_name = tc.constraint_name WHERE kcu.table_name = %s AND tc.constraint_type = 'PRIMARY KEY';"
    params = (nombre_tabla,)
    pk = realizar_consulta_conexion(conn,sql_pk, params)[0]["column_name"]
    #endregion

    #region Verificar que la columna de la clave primaria no se haya enviado en el diccionario o que su valor sea None
    if pk in data and data[pk] is not None:
        mensaje = f"No se puede enviar el valor de la clave primaria '{pk}'. El valor se establece automáticamente"
        logica.respuesta_fallida(mensaje)
    # obtener los nombres de las columnas de la tabla
    sql ='SELECT column_name FROM information_schema.columns WHERE table_name = %s'
    columnas = realizar_consulta_conexion(conn,sql,params)
    columnas = [columna["column_name"] for columna in columnas]
    #endregion

    #region revisar que todas las columnas enviadas existan en la tabla
    for columna in data:
        if columna not in columnas:
            mensaje = f"La columna '{columna}' no existe en la tabla '{nombre_tabla}'"
            logica.respuesta_fallida(mensaje)
    #endregion

    #region eliminar las columnas que no estén presentes en data
    columnas = [columna for columna in columnas if columna in data]
    #endregion

    #region Verificar que no falten campos requeridos que no pueden ser nulos en la base de datos
    campos_no_nulos = obtener_campos_no_nulos(nombre_tabla,conn)
    for campo in campos_no_nulos:
        if (campo not in data or data[campo] is None) and campo != pk:
            mensaje = f"No se proporcionó un valor para el campo requerido '{campo}'"
            logica.respuesta_fallida(mensaje)
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
        mensaje = f"Ya existe un registro con la clave primaria '{pk}'. Revise los seriales "
        logica.respuesta_fallida(mensaje)
    #endregion

    #region obtener el valor de la clave primaria del nuevo registro
    sql = f"SELECT currval(pg_get_serial_sequence('{nombre_tabla}', '{pk}'))"
    pk_value = realizar_consulta_conexion(conn, sql)[0]["currval"]
    #endregion

    conn.close()
    return pk_value

def insertar_datos_conexion(conn,sql, params=None):
    #revisamos si es un insert y no un select o update o delete...
    #if any of the params is None change it to NULL
    params = [None if param is None else param for param in params]
    if not sql.upper().startswith("INSERT"):
        #si es un insert, obtenemos los datos
        mensaje = "La consulta debe ser de tipo INSERT"
        logica.respuesta_fallida(mensaje)
    cursor = conn.cursor()
    #print the query with the params
    print(cursor.mogrify(sql, params))
    cursor.execute(sql, params)
    print("Datos insertados correctamente")
    #si no hay errores retornamos el id del registro insertado
    conn.commit()
    cursor.close()
    return cursor.lastrowid

def actualizar_datos_conexion(conn,sql, params=None):
    #revisamos si es un insert y no un select o update o delete...
    #if any of the params is None change it to NULL
    params = [None if param is None else param for param in params]
    if not sql.upper().startswith("UPDATE"):
        #si es un insert, obtenemos los datos
        mensaje = "La consulta debe ser de tipo UPDATE"
        logica.respuesta_fallida(mensaje)
    cursor = conn.cursor()
    #print the query with the params
    print(cursor.mogrify(sql, params))
    cursor.execute(sql, params)
    print("Datos actualizados correctamente")
    #si no hay errores retornamos el id del registro insertado
    conn.commit()
    cursor.close()
    return cursor.lastrowid

def obtener_campos_no_nulos(nombre_tabla: str, conn: psycopg2.extensions.connection):
    sql = "SELECT column_name FROM information_schema.columns WHERE table_name = %s AND is_nullable = 'NO'"
    params = (nombre_tabla,)
    resultados = realizar_consulta_conexion(conn, sql, params)
    campos_no_nulos = [resultado['column_name'] for resultado in resultados]

    return campos_no_nulos

def realizar_actualizacion(nombre_tabla: str,id: int, data: dict):
    """
    Realiza una actualización en la base de datos de acuerdo a los datos enviados en el diccionario data.
    El diccionario data no debe contener la clave primaria del registro a actualizar, ya que esta se establece por el path parameter.
    Aquellos campos que no se envíen en el diccionario se dejarán con el valor que tengan actualmente en la base de datos.
    """
    conn = get_connection()
    # region verificar que la tabla exista
    sql = 'SELECT * FROM %s LIMIT 1'
    table_name = AsIs(nombre_tabla)
    params = (table_name,)
    try:
        realizar_consulta_conexion(conn, sql, params)
    except:
        mensaje = f"La tabla {nombre_tabla} no existe"
        logica.respuesta_fallida(mensaje)
    # endregion

    # region establecer el valor de pk al nombre de la columna que es clave primaria
    sql_pk = "SELECT kcu.column_name FROM information_schema.key_column_usage kcu JOIN information_schema.table_constraints tc ON kcu.constraint_name = tc.constraint_name WHERE kcu.table_name = %s AND tc.constraint_type = 'PRIMARY KEY';"
    params = (nombre_tabla,)
    pk = realizar_consulta_conexion(conn, sql_pk, params)[0]["column_name"]
    # endregion

    # region Verificar que la columna de la clave primaria no se haya enviado en el diccionario y su valor no sea None
    if pk in data or id is None:
        mensaje = f"No debe enviar el valor de la clave primaria '{pk}' en el data. El valor se establece por el path parameter"
        logica.respuesta_fallida(mensaje)
    # endregion

    # region Obterner las columnas de la tabla
    sql = 'SELECT column_name FROM information_schema.columns WHERE table_name = %s'
    columnas = realizar_consulta_conexion(conn, sql, params)
    columnas = [columna["column_name"] for columna in columnas]
    #endregion

    # # IGNORAR region Verificar que la columna de la clave primaria exista en la tabla
    # if pk not in columnas:
    #     mensaje = f"La columna de la clave primaria '{pk}' no existe en la tabla '{nombre_tabla}'"
    #     logica.respuesta_fallida(mensaje)
    # # endregion

    #region verifiar que exista un registro con el id enviado
    sql = f"SELECT * FROM {nombre_tabla} WHERE {pk} = %s"
    params = (id,)
    if not realizar_consulta_conexion(conn, sql, params):
        mensaje = f"No existe un registro con la clave primaria '{pk}' = {id}"
        logica.respuesta_fallida(mensaje)
    #endregion

    # region Verificar que las columnas enviadas existan en la tabla
    for columna in data:
        if columna not in columnas:
            mensaje = f"La columna '{columna}' no existe en la tabla '{nombre_tabla}'"
            logica.respuesta_fallida(mensaje)
    # endregion

    # region Verificar que los campos con valor None puedan ser nulos en la base de datos
    campos_no_nulos = obtener_campos_no_nulos(nombre_tabla, conn)
    for campo, valor in data.items():
        if valor is None:
            if campo in campos_no_nulos:
                mensaje = f"No se puede asignar un valor None al campo no nulo '{campo}'"
                logica.respuesta_fallida(mensaje)
    # endregion

    # region Construir la consulta de actualización y los valores a actualizar
    columnas_actualizar = []
    valores_actualizar = []
    for columna in columnas:
        if columna != pk:
            if columna in data:
                columnas_actualizar.append(columna)
                valores_actualizar.append(data[columna])

    sql = f"UPDATE {nombre_tabla} SET {', '.join([columna + ' = %s' for columna in columnas_actualizar])} WHERE {pk} = %s"
    valores = valores_actualizar + [id]
    try:
        actualizar_datos_conexion(conn, sql, valores)
    except IntegrityError:
        mensaje = f"No se puede realizar la actualización. Ya existe un registro con la clave primaria '{pk}'"
        logica.respuesta_fallida(mensaje)
    # endregion

    conn.close()
    return id

    
    