import psycopg2
# AsIs from psycopg2.sql
from psycopg2.extensions import AsIs
from psycopg2 import IntegrityError
from fastapi import HTTPException
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

# def realizar_consulta(sql, params=None):
#     #revisamos si es una query y no un insert o update o delete...
#     if not sql.upper().startswith("SELECT"):
#         #si es una query, obtenemos los datos
#         return "Error"
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute(sql, params)
#     #guardamos los datos en una variable
#     datos = cursor.fetchall()
#     #imprimimos los datos
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return datos


def realizar_consulta(sql:str, params=None):
    if not sql.upper().startswith("SELECT"):
        raise HTTPException(status_code=400, detail="La consulta debe ser de tipo SELECT")
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
        return {"success": False, "code": 404, "message": f"La tabla {nombre_tabla} no existe"}
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
        return {"success": False, "code": 400, "message": f"Ya existe un registro con la clave primaria '{pk}' "}
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


# def insertDB(nombreTabla, data):
#     conn = db.get_connection()
#     # verificar que la tabla exista
#     sql = f"SELECT * FROM {nombreTabla} LIMIT 1"
#     try:
#         cursor = db.realizar_consulta(sql)
#         cursor.close()
#     except:
#         return {"success": False, "code": 400, "message": f"La tabla {nombreTabla} no existe"}

#     # obtener los nombres de las columnas de la tabla
#     sql = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{nombreTabla}'"
#     cursor = db.realizar_consulta(sql)
#     columnas = [columna[0] for columna in cursor.fetchall()]
#     cursor.close()

#     # verificar que no haya campos sobrantes
#     if set(data.keys()) - set(columnas):
#         sobrantes = list(set(data.keys()) - set(columnas))
#         mensaje = f"La(s) columna(s) {', '.join(sobrantes)} no existe(n) en la tabla {nombreTabla}"
#         return {"success": False, "code": 400, "message": mensaje}

#     # obtener los campos que no son clave primaria
#     sql = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{nombreTabla}' and column_key != 'PRI'"
#     cursor = db.realizar_consulta(sql)
#     campos_no_clave = [columna[0] for columna in cursor.fetchall()]
#     cursor.close()

#     # agregar valores nulos para los campos no clave que falten
#     for campo in campos_no_clave:
#         if campo not in data:
#             data[campo] = None

#     # obtener los campos clave primaria
#     sql = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{nombreTabla}' and column_key = 'PRI'"
#     cursor = db.realizar_consulta(sql)
#     campos_clave = [columna[0] for columna in cursor.fetchall()]
#     cursor.close()

#     # verificar que haya campos clave primaria
#     if not campos_clave:
#         mensaje = f"No se encontraron campos clave primaria en la tabla {nombreTabla}"
#         return {"success": False, "code": 400, "message": mensaje}

#     # verificar que estén todos los campos clave
#     if set(campos_clave) - set(data.keys()):
#         faltantes = list(set(campos_clave) - set(data.keys()))
#         mensaje = f"Falta(n) el/los campo(s) clave {', '.join(faltantes)} en la tabla {nombreTabla}"
#         return {"success": False, "code": 400, "message": mensaje}

#     # verificar si el registro a insertar ya existe
#     condiciones = [f"{campo} = '{data[campo]}'" for campo in campos_clave]
#     sql = f"SELECT * FROM {nombreTabla} WHERE {' AND '.join(condiciones)}"
#     cursor = db.realizar_consulta(sql)
#     if cursor.fetchall():
#         cursor.close()
#         mensaje = f"Ya existe un registro en la tabla {nombreTabla} con los valores {json.dumps(data)}"
#         return {"success": False, "code": 400, "message": mensaje}

#     #insertar el registro
#     columnas = ",".join(data.keys())
#     valores = tuple(data.values())

#     sql = f"INSERT INTO {nombreTabla} ({columnas}) VALUES ({','.join(['%s'] * len(valores))}) RETURNING *"

#     try:
#         cursor.execute(sql, valores)
#         conn.commit()
#         data = cursor.fetchone()
#         if not data:
#             raise ValueError("No se pudo obtener el registro insertado")
#         # Formatear la respuesta con los campos solicitados
#         respuesta = {
#             "success": True,
#             "code": 201,
#             "message": "Registro insertado exitosamente",
#             "data": {
#                 "id": data[0],
#                 "nombre": data[1]
#             }
#         }
#     except ValueError as ve:
#         respuesta = {
#             "success": False,
#             "code": 400,
#             "message": str(ve)
#         }
#     except Exception as e:
#         respuesta = {
#             "success": False,
#             "code": 400,
#             "message": f"Error insertando el registro: {str(e)}"
#         }

#     cursor.close()
#     conn.close()

#     return respuesta

def insertDB(nombreTabla, data):
    conn = get_connection()
    # verificar que la tabla exista
    sql = f"SELECT * FROM {nombreTabla} LIMIT 1"
    try:
        cursor = realizar_consulta(sql)
        cursor.close()
    except:
        return {"success": False, "code": 400, "message": f"La tabla {nombreTabla} no existe"}

    # obtener los nombres de las columnas de la tabla
    sql = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{nombreTabla}'"
    cursor = realizar_consulta(sql)
    columnas = [columna[0] for columna in cursor.fetchall()]
    cursor.close()

    # verificar que no haya campos sobrantes
    if set(data.keys()) - set(columnas):
        sobrantes = list(set(data.keys()) - set(columnas))
        mensaje = f"La(s) columna(s) {', '.join(sobrantes)} no existe(n) en la tabla {nombreTabla}"
        return {"success": False, "code": 400, "message": mensaje}

    # obtener los campos que no son clave primaria
    sql = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{nombreTabla}' and column_key != 'PRI'"
    cursor = realizar_consulta(sql)
    campos_no_clave = [columna[0] for columna in cursor.fetchall()]
    cursor.close()

    # agregar valores nulos para los campos no clave que falten
    for campo in campos_no_clave:
        if campo not in data:
            data[campo] = None

    # obtener los campos clave primaria
    sql = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{nombreTabla}' and column_key = 'PRI'"
    cursor = realizar_consulta(sql)
    campos_clave = [columna[0] for columna in cursor.fetchall()]
    cursor.close()

    # verificar que haya campos clave primaria
    if not campos_clave:
        mensaje = f"No se encontraron campos clave primaria en la tabla {nombreTabla}"
        return {"success": False, "code": 400, "message": mensaje}

    # verificar que estén todos los campos clave
    if set(campos_clave) - set(data.keys()):
        faltantes = list(set(campos_clave) - set(data.keys()))
        mensaje = f"Falta(n) el/los campo(s) clave {', '.join(faltantes)} en la tabla {nombreTabla}"
        return {"success": False, "code": 400, "message": mensaje}

    # verificar si el registro a insertar ya existe
    condiciones = [f"{campo} = '{data[campo]}'" for campo in campos_clave]
    sql = f"SELECT * FROM {nombreTabla} WHERE {' AND '.join(condiciones)}"
    cursor = realizar_consulta(sql)
    if cursor.fetchall():
        cursor.close()
        mensaje = f"Ya existe un registro en la tabla {nombreTabla} con los valores {json.dumps(data)}"
        return {"success": False, "code": 400, "message": mensaje}

    #insertar el registro
    columnas = ",".join(data.keys())
    valores = tuple(data.values())

    sql = f"INSERT INTO {nombreTabla} ({columnas}) VALUES ({','.join(['%s'] * len(valores))}) RETURNING *"

    try:
        cursor.execute(sql, valores)
        conn.commit()
        data = cursor.fetchone()
        if not data:
            raise ValueError("No se pudo obtener el registro insertado")
        # Formatear la respuesta con los campos solicitados
        respuesta = {
            "success": True,
            "code": 201,
            "message": "Registro insertado exitosamente",
            "data": {
                "id": data[0],
                "nombre": data[1]
            }
        }
    except ValueError as ve:
        respuesta = {
            "success": False,
            "code": 400,
            "message": str(ve)
        }
    except Exception as e:
        respuesta = {
            "success": False,
            "code": 400,
            "message": f"Error insertando el registro: {str(e)}"
        }

    cursor.close()
    conn.close()

    return respuesta


    
    