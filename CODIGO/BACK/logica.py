from decimal import Decimal
from fastapi import HTTPException
from fastapi import Request
import json
import db
import correos

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
    
    query = "SELECT * FROM alumno WHERE id_alumno = %s"
    parameters = (id_usuario,)
    usuario = db.realizar_consulta(query, params=parameters)
    
    #llamar a la funcion de enviar correo sin bloquear la ejecucion
    enviar_correo_bienvenida([usuario[0]["correo"]])
    return usuario[0]

def obtener_usuario(id_usuario: int):
    """
    Obtiene el usuario con el id especificado de la base de datos y lo devuelve como un diccionario
    """
    #region obtener el usuario con el id especificado
    query = "SELECT * FROM alumno WHERE id_alumno = %s"
    parameters = (id_usuario,)
    usuario = db.realizar_consulta(query, params=parameters)
    #endregion

    #region verificar que se encontró el usuario
    if len(usuario) == 0:
        mensaje = "No se encontró el usuario con id " + str(id_usuario)
        respuesta_fallida(mensaje, 404)
    #endregion

    #region convertir los datos a un diccionario
    usuario = usuario[0]
    #endregion
    return usuario
#endregion

#region funciones de envio de correos
def enviar_correo_bienvenida(destinatarios):
  asunto = '¡Bienvenid@ a SmartUni!'
  cuerpo_html = '''
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Correo Electrónico de SmartUni</title>
    <link href="https://fonts.googleapis.com/css2?family=Asap+Condensed:wght@400;700&display=swap" rel="stylesheet">
    <style>
      /* Estilos generales */
      body {
        margin: 0;
        padding: 0;
        font-family: Arial, sans-serif;
        background-color: #1164ce;
        color: #fff;
      }

      .container {
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
        background-color: #fff;
      }

      /* Estilos del encabezado */
      .header {
        text-align: center;
        margin-bottom: 30px;
      }

      .header img {
        max-width: 200px;
      }

      /* Estilos del contenido */
      .content {
        text-align: center;
        margin-bottom: 30px;
      }

      .content h1 {
        font-family: 'Asap Condensed', sans-serif;
        font-weight: 700;
      }

      /* Estilos del pie de página */
      .footer {
        text-align: center;
        font-size: 12px;
        color: #999;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <img src="https://i.imgur.com/QVRrfct.png" alt="SmartUni Logo">
      </div>

      <div class="content">
        <h1>Bienvenido a SmartUni</h1>
        <p>Estimad@ estudiante,</p>
        <p>Te damos la bienvenida a SmartUni, la plataforma online inteligente de la Universidad de Alcalá. Estamos emocionados de tenerte como parte de nuestra comunidad.</p>
        <p>Con SmartUni, podrás acceder a una amplia gama de recursos y de funcionalidados. Estamos comprometidos a brindarte una experiencia educativa de calidad y apoyarte en tu crecimiento académico y profesional.</p>
        <p>¡Explora nuestra plataforma y descubre nuevas oportunidades de aprendizaje!</p>
        <p>Atentamente,</p>
        <p>El equipo de SmartUni.</p>
      </div>

      <div class="footer">
        <p>Este correo electrónico fue enviado desde la plataforma SmartUni. Por favor, no respondas a este mensaje.</p>
      </div>
    </div>
  </body>
  </html>

  '''
  correos.enviar_correo(destinatarios, asunto, cuerpo_html)
  
def enviar_correo_taquilla_reservada(destinatarios, datos_taquilla):
    asunto = 'Confirmación de reserva de taquilla'
    ala_taquilla = datos_taquilla["ala"]
    piso_taquilla = str(datos_taquilla["piso"])
    numero_taquilla = str(datos_taquilla["id_taquilla"])
    contrasenna_taquilla = str(datos_taquilla["password"])
    cuerpo_html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Confirmación de reserva de taquilla</title>
        <link href="https://fonts.googleapis.com/css2?family=Asap+Condensed:wght@400;700&display=swap" rel="stylesheet">
        <style>
            /* Estilos omitidos para mayor claridad */

            /* Estilos del contenido */
            .content {
                text-align: center;
                margin-bottom: 30px;
            }

            .content h1 {
                font-family: 'Asap Condensed', sans-serif;
                font-weight: 700;
            }

            /* Estilos omitidos para mayor claridad */
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Encabezado y estilos omitidos para mayor claridad -->

            <div class="content">
                <h1>Confirmación de reserva de taquilla</h1>
                <p>Estimad@ estudiante,</p>
                <p>Te informamos que se ha realizado la reserva de una taquilla con éxito.</p>
                <p>Detalles de la reserva:</p>
                <p>Ala: ''' + ala_taquilla + '''</p>
                <p>Piso: ''' + piso_taquilla + '''</p>
                <p>Número de taquilla: ''' + numero_taquilla + '''</p>
                <p>Contraseña de taquilla: ''' + contrasenna_taquilla + '''</p>
                <p>¡Disfruta de tu taquilla!</p>
                <p>Atentamente,</p>
                <p>El equipo de SmartUni</p>
            </div>

            <!-- Pie de página y estilos omitidos para mayor claridad -->
        </div>
    </body>
    </html>
    '''


    correos.enviar_correo(destinatarios, asunto, cuerpo_html)
#endregion

#region funciones de taquillas

def obtener_taquilla(id_taquilla: int, id_alumno = -1):
    # devolverla como un diccionario con sus propiedades (por ejemplo, {'id': 1, 'ocupado': True, 'usuario': None})
    # Si no se encuentra ninguna taquilla con ese id, se debe retornar un error (por ejemplo, {'success': False, 'message': 'No se encontró la taquilla con id 1'})
    query = "SELECT * FROM taquilla WHERE id_taquilla = %s"
    parameters = [id_taquilla]
    taquilla = db.realizar_consulta(query, params=parameters)
    if len(taquilla) == 0:
        respuesta_fallida("No se encontró la taquilla con id " + str(id_taquilla), 404)
    #region para comprobar si esta ocupada y coincide el id_alumno
    if (taquilla[0]['ocupado']):
        if(taquilla[0]['id_alumno_alumno'] != id_alumno):
            respuesta_fallida("La taquilla con id " + str(id_taquilla) + " no pertenece al alumno " + str(id_alumno), 403) 
    #endregion    
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
        

def obtener_todasTaquillas(ala = "", piso = -1, pasillo = -1, ocupado = -1):
    query = "SELECT id_taquilla, piso, ala, pasillo, ocupado FROM taquilla"
    params = []
    if ala != "":
        query += " WHERE ala = %s"
        params.append(ala)
    if piso != -1:
        if len(params) == 0:
            query += " WHERE piso = %s"
        else:
            query += " AND piso = %s"
        params.append(piso)
    if pasillo != -1:
        if len(params) == 0:
            query += " WHERE pasillo = %s"
        else:
            query += " AND pasillo = %s"
        params.append(pasillo)
    if ocupado != -1:
        if len(params) == 0:
            query += " WHERE ocupado = %s"
        else:
            query += " AND ocupado = %s"
        params.append(ocupado)    
    taquillas = db.realizar_consulta(query, params)
    return taquillas


def crear_taquilla(data : dict):
    taquilla = obtener_taquilla(db.realizar_insercion("taquilla", data))
    return taquilla

#funcion para abrir una taquilla
def abrir_taquilla(id_taquilla: int, password:int):
    #region Obtener la taquilla con el id especificado

    query = "SELECT * FROM taquilla WHERE id_taquilla = %s AND password = %s"
    parameters = ([id_taquilla, password])
    taquilla = db.realizar_consulta(query, params=parameters)
    #endregion
    #region Verificar si no se encontró la taquilla con los datos proporcionados
    if len(taquilla) == 0:
        mensaje = f"La contraseña o el id_taquilla no son correctos."
        respuesta_fallida(mensaje, 400)
    #endregion
    return True  # Contraseña correcta


#region funcion para reservar una taquilla
def reservar_taquilla(id_taquilla: int, data: dict):
    
    taquilla = obtener_taquilla(id_taquilla)
    # region Verificar que la taquilla no está ocupada
    if  taquilla[0]['ocupado']:
        respuesta_fallida("La taquilla con id " + str(id_taquilla) + " no está disponible",400)
    #endregion
    
    #region verificar que el alumno no tengo ninguna otra taquilla
    query = "SELECT * FROM taquilla WHERE id_alumno_alumno = %s"
    parameters = ([data["id_alumno_alumno"]])
    taquilla = db.realizar_consulta(query, params=parameters)
    if len(taquilla) != 0:
        respuesta_fallida("El alumno con id " + str(data["id_alumno_alumno"]) + " ya tiene una taquilla",400)
    #endregion
    
    # region Actualizar la taquilla con el id del usuario que la reservó
    db.realizar_actualizacion("taquilla",id_taquilla, data)
    #endregion
    
    #enviamos el correo de confirmacion
    alumno = obtener_usuario(data["id_alumno_alumno"])
    correo = alumno["correo"]
    taquilla = obtener_taquilla(id_taquilla,data["id_alumno_alumno"])[0]
    enviar_correo_taquilla_reservada([correo], taquilla)
    return taquilla
#endregion

#region cancelar una taquilla
def cancelar_taquilla(id_taquilla: int, id_usuario: int) -> dict:
    #region Verificar que la taquilla está reservada por el alumno
    query = "SELECT * FROM taquilla WHERE id_taquilla = %s AND id_alumno_alumno = %s"
    parameters = ([id_taquilla, id_usuario])
    taquilla = db.realizar_consulta(query, params=parameters)
    if len(taquilla) == 0:
        mensaje = f"La taquilla {id_taquilla} no está reservada por el alumno {id_usuario}"
        respuesta_fallida(mensaje, 400)
    #endregion
    
    #region Actualizar la taquilla con el id del usuario que la reservó
    data = {
        "password": None,
        "ocupado": False,
        "id_alumno_alumno": None
    }
    db.realizar_actualizacion("taquilla",id_taquilla,data)
    #endregion

    #region Obtener la información actualizada de la taquilla
    taquilla_actualizada = obtener_taquilla(id_taquilla)
    #endregion

    return taquilla_actualizada
#endregion

#region funcion para eliminar una taquilla a partir de su id y que nos muestre su informacion (de momento no se usa)
def eliminar_taquilla(id_taquilla: int):

    #region Obtener la taquilla con el id especificado
    taquilla = obtener_taquilla(id_taquilla)
    #endregion
    #region Verificar que se encontró la taquilla
    if len(taquilla) == 0:
        mensaje = f"No se encontró la taquilla con id {id_taquilla}"
        respuesta_fallida(mensaje, 404)
    #endregion

    #region Eliminar la taquilla
    query = "DELETE FROM taquilla WHERE id_taquilla = %s"
    parameters = ([id_taquilla])
    db.realizar_modificacion(query, params=parameters)
    #endregion

    return taquilla
#endregion

#region obtener la taquilla que ha reservado el usuario
def obtener_taquilla_reservada_por_alumno(id_alumno:int):
    query = "SELECT * FROM taquilla WHERE id_alumno_alumno = %s"
    parameters = ([id_alumno])
    taquilla = db.realizar_consulta(query, params=parameters)
    return taquilla
#endregion
#endregion
    
#region funciones de las aulas

#region listado de las aulas
def obtener_aulas(ala,planta,numero):
    """
    Lista todas las aulas de la base de datos.
    """
    #region obtener las aulas de la base de datos
    query = "SELECT id_aula, laboratorio, planta, ala, num_ala FROM aula"
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
            query += " WHERE num_ala = %s"
        else:
            query += " AND num_ala = %s"
        params.append(numero)
    aulas = db.realizar_consulta(query, params)
    #endregion
    #region convertir los datos a un diccionario añadiendo los nombres de cada aula.
    for aula in aulas:
            letra_ala = aula['ala'][0]
            nombre_aula = (f"{letra_ala}{'L' if aula['laboratorio'] else 'A'}{aula['num_ala']}").upper()
            aula['nombre'] = nombre_aula
    #endregion
    return aulas
#endregion

#region sacar el aula dado el id
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
    nombre_aula = (f"{letra_ala}{'L' if aula['laboratorio'] else 'A'}{aula['num_ala']}").upper()
    aula['nombre'] = nombre_aula
    #endregion
    return aula
#endregion

#region insertar nueva aula
def insertar_aula(aula: dict):
    return obtener_aula(db.realizar_insercion("aula", aula))
#endregion

#region actualizar aula
def actualizar_aula(id: int, aula: dict):
    return obtener_aula(db.realizar_actualizacion("aula",id,aula))
#endregion

#region obtener asignaturas que se dan en un aula
def obtener_asignatura_aula(id_aula: int=-1):
    #region obtener las asignaturas de la base de datos
    query = "SELECT id_asignatura, descripcion, temperatura, laboratorio, planta, ala, dia, hora_inicio, hora_fin, num_ala from vista_asignaturas"
    params = []
    if id_aula != -1:
        query += " WHERE id_aula = %s"
        params.append(id_aula)
    
    asignaturas = db.realizar_consulta(query,params)
    #endregion
    print(len(asignaturas))
    #region verificar que se encontró la asignatura
    if len(asignaturas) == 0:
        mensaje = "No se encontraron asignaturas en la clase " + str(id_aula)
        respuesta_fallida(mensaje, 404)
    #endregion

    #region convertir los datos a un diccionario añadiendo los nombres de cada aula.
    for asig in asignaturas:
            letra_ala = asig['ala'][0]
            nombre_aula = (f"{letra_ala}{'L' if asig['laboratorio'] else 'A'}{asig['num_ala']}").upper()
            asig['nombre'] = nombre_aula
    #endregion

    return asignaturas

#endregion

#region sacar el horario dado el id
def obtener_horario(id_horario: int):
    """
    Obtiene el horario con el id especificado de la base de datos y lo devuelve como un diccionario
    """
    #region obtener el horario con el id especificado
    query = "SELECT * FROM horario WHERE id_horario = %s"
    parameters = (id_horario,)
    horario = db.realizar_consulta(query, params=parameters)
    #endregion

    #region verificar que se encontró el horario
    if len(horario) == 0:
        print("No se encontró el horario con id " + str(id_horario))
        mensaje = "No se encontró el horario con id " + str(id_horario)
        respuesta_fallida(mensaje, 404)
    #endregion

    #region convertir los datos a un diccionario
    horario = horario[0]
    #endregion
    return horario
#endregion

#region insertar horario
def insertar_horario(horario: dict):
    return obtener_horario(db.realizar_insercion("horario",horario))
#endregion

#region sacar proxima clase
def obtener_clase_proxima(id_aula):
    query= "SELECT fecha_inicio FROM aula INNER JOIN asignatura INNER JOIN horario WHERE id_aula = %s AND fecha_inicio > now() ORDER BY fecha_inicio DESC LIMIT 1"
    #hay que probar la query
    params = (id_aula)
    hora = db.realizar_consulta(query,params)
    return hora
#endregion


#endregion

#region funciones de cafeteria
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

def obtener_pedidos(id_alumno: int = -1):
    """
    Lista todos los pedidos de cafetería.
    """
    #region obtener los pedidos de la base de datos
    query = "SELECT id_pedido, correo_alumno, productos_ids, productos_descripciones, estado from vista_pedidos"
    params = []
    if id_alumno != -1:
        query += " WHERE id_alumno_alumno = %s"
        params.append(id_alumno)
    query += " ORDER BY id_pedido DESC"
    pedidos = db.realizar_consulta(query,params)
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
    productos_sin_duplicar = set(data["productos"])
    for producto in productos_sin_duplicar:
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

    sql = "INSERT INTO pedido_producto (id_pedido_pedido, id_producto_producto) VALUES "
    for producto in data["productos"]:
        sql += f"({id_pedido}, {producto}),"
    sql = sql[:-1] #quitamos la última coma
    db.ejecutar_sentencia(sql)

    #region COMENTADO version anterior sin optimizar pero mas segura
    # for producto in data["productos"]:
    #     data_pedido_producto = {
    #         "id_pedido_pedido": id_pedido,
    #         "id_producto_producto": producto
    #     }
    #     db.realizar_insercion("pedido_producto", data_pedido_producto)
    #endregion

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
    if data["estado"] not in [0, 1, 2, 3, 4]:
        mensaje = "El estado debe ser 0, 1, 2 , 3 y 4"
        respuesta_fallida(mensaje, 400)
    if pedido["estado"] == 4:
        mensaje = "El pedido ya está completado y no se puede modificar"
        respuesta_fallida(mensaje, 400)
    if pedido["estado"] >=  data["estado"] :
        mensaje = "La modificación del estado no es válida"
        respuesta_fallida(mensaje, 400)
    #endregion

    #region actualizaciones de nfc
    #region si el estado es 4, el nfc debe dejar de estar asociado al pedido
    if data["estado"] == 4:
        #region si no hay un nfc asociado, se debe devolver un error
        if pedido["id_nfc"] is None:
            mensaje = "No hay ningún nfc asociado al pedido"
            respuesta_fallida(mensaje, 400)
        #endregion
        data_pedido = {
            "id_pedido_pedido": None
        }
        db.realizar_actualizacion("nfc", pedido["id_nfc"], data_pedido)
        #endregion
    #region si el estado es 1, deberá asociarse un nfc de los disponibles al pedido
    if data["estado"] == 1:
        #region si ya hay un nfc asociado, se debe liberar dicho nfc
        if pedido["id_nfc"] is not None:
            data_pedido = {
                "id_pedido_pedido": None
            }
            db.realizar_actualizacion("nfc", pedido["id_nfc"], data_pedido)
        #endregion
        #region obtener el primer nfc disponible
        query = "SELECT id_nfc FROM nfc WHERE id_pedido_pedido IS NULL LIMIT 1"
        nfcs = db.realizar_consulta(query)
        #endregion

        #region verificar que hay al menos un nfc disponible
        if len(nfcs) == 0:
            mensaje = "No hay ningún nfc disponible"
            respuesta_fallida(mensaje, 400)
        #endregion

        #region asociar el primer nfc disponible al pedido
        data_pedido = {
            "id_pedido_pedido": id_pedido
        }
        db.realizar_actualizacion("nfc", nfcs[0]["id_nfc"], data_pedido)
        #endregion
    #endregion

    #region obtener el pedido actualizado
    pedido = obtener_pedido(id_pedido)
    #endregion

    #region actualizar el pedido
    data_pedido = {
        "estado": data["estado"]
    }
    db.realizar_actualizacion("pedido", id_pedido, data_pedido)
    #endregion


    return pedido


#endregion

def obtener_pedido_estrella(id_alumno: int = -1):
    """
    Lista todos los pedidos de cafetería.
    """
    #region obtener el pedido estrella
    query = "SELECT id_producto, descripcion, COUNT(*) AS cantidad from vista_pedido_estrella"
    params = []
    if id_alumno != -1:
        query += " WHERE id_alumno_alumno = %s"
        params.append(id_alumno)
    
    query += " GROUP BY id_producto, descripcion ORDER BY cantidad DESC LIMIT 1"
    pedido_estrella = db.realizar_consulta(query,params)
    #endregion

    #region verificar que se encontró el pedido estrella
    if len(pedido_estrella) == 0:
        mensaje = "Debes tener al menos un pedido para obtener el pedido estrella"
        respuesta_fallida(mensaje, 404)
    #endregion

    #region convertir los datos a un diccionario
    pedido_estrella = pedido_estrella[0]
    #endregion
    return pedido_estrella

#endregion



#region funciones nfc básicas

def obtener_nfcs():
    """
    Lista todos los NFCs de la base de datos.
    """
    #region obtener los NFCs de la base de datos
    nfcs = db.realizar_consulta("SELECT num_serie FROM nfc")
    #endregion
    return nfcs

def obtener_nfc_por_num_serie(num_serie: str):
    """
    Obtiene el NFC con el num_serie especificado de la base de datos y lo devuelve como un diccionario
    """
    #region obtener el NFC con el num_serie especificado
    query = "SELECT * FROM nfc WHERE num_serie = %s"
    parameters = (num_serie,)
    nfc = db.realizar_consulta(query, params=parameters)
    #endregion

    #region verificar que se encontró el NFC
    if len(nfc) == 0:
        mensaje = "No se encontró el NFC con num_serie " + str(num_serie)
        respuesta_fallida(mensaje, 404)
    #endregion

    #region convertir los datos a un diccionario
    nfc = nfc[0]
    #endregion
    return nfc

def obtener_nfc(id_nfc: int):
    """
    Obtiene el NFC con el id especificado de la base de datos y lo devuelve como un diccionario
    """
    #region obtener el NFC con el id especificado
    query = "SELECT * FROM nfc WHERE id_nfc = %s"
    parameters = (id_nfc,)
    nfc = db.realizar_consulta(query, params=parameters)
    #endregion

    #region verificar que se encontró el NFC
    if len(nfc) == 0:
        mensaje = "No se encontró el NFC con id " + str(id_nfc)
        respuesta_fallida(mensaje, 404)
    #endregion

    #region convertir los datos a un diccionario
    nfc = nfc[0]
    #endregion
    return nfc


def insertar_nfc(nfc: dict):
    #region comprobar que no exista un nfc con el mismo num_serie
    query = "SELECT * FROM nfc WHERE num_serie = %s"
    parameters = (nfc["num_serie"],)
    nfcs = db.realizar_consulta(query, params=parameters)
    if len(nfcs) > 0:
        mensaje = "Ya existe un nfc con num_serie " + str(nfc["num_serie"])
        respuesta_fallida(mensaje, 400)
    #endregion
    return db.realizar_insercion("nfc", nfc)

def actualizar_nfc(id: int, nfc: dict):
    return db.realizar_actualizacion("nfc",id,nfc)

#endregion

#region funciones avanzadas nfc

def actualizar_pedido_nfc(id_pedido: int, data: dict):
    """
    Actualiza el pedido con el id especificado. Solo estará permitido cambiar el estado.
    """
    #region obtener el pedido con el id especificado
    pedido = obtener_pedido(id_pedido)
    #endregion
    #region verificar que el pedido esté asociado a la nfc con el num_serie especificado en el data
    num_serie_nfc = data["num_serie"]
    if (pedido["num_serie"] != num_serie_nfc):
        mensaje = "El pedido no está asociado a la nfc con num_serie " + str(num_serie_nfc)
        respuesta_fallida(mensaje, 400)
    #endregion
    #region actualiar el pedido
    #eliminamos el num_serie del diccionario data
    del data["num_serie"]
    return actualizar_pedido(id_pedido, data) #llamando a este método habrá una query redundante. Se podría mejorar
    #endregion

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


