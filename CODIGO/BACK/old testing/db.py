import psycopg2

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

def realizar_consulta(sql, params=None):
    #revisamos si es una query y no un insert o update o delete...
    if not sql.upper().startswith("SELECT"):
        #si es una query, obtenemos los datos
        return "Error"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    #guardamos los datos en una variable
    datos = cursor.fetchall()
    #imprimimos los datos
    conn.commit()
    cursor.close()
    conn.close()
    return datos

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
    

    