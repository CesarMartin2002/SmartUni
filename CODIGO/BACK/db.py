import psycopg2
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


def realizar_consulta(sql, params=None):
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



def insertar_datos(sql, params=None):
    #revisamos si es un insert y no un select o update o delete...
    if not sql.upper().startswith("INSERT"):
        #si es un insert, obtenemos los datos
        return "Error"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    #si no hay errores retornamos el id del registro insertado
    conn.commit()
    cursor.close()
    conn.close()
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


    
    