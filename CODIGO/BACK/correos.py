import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE
import concurrent.futures

def enviar_correo(destinatarios, asunto, cuerpo_html):
    # Configuración de los datos de conexión SMTP de Gmail
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    usuario = 'smartuniubicua@gmail.com'
    contrasena = 'jakldowsuaxsblzj'

    # Crea el mensaje MIME
    mensaje = MIMEMultipart('alternative')
    mensaje['From'] = usuario
    mensaje['To'] = COMMASPACE.join(destinatarios)
    mensaje['Subject'] = asunto

    # Crea la parte HTML del mensaje
    parte_html = MIMEText(cuerpo_html, 'html')
    mensaje.attach(parte_html)

    def enviar(destinatario):
        with smtplib.SMTP(smtp_host, smtp_port) as servidor_smtp:
            servidor_smtp.starttls()
            servidor_smtp.login(usuario, contrasena)
            servidor_smtp.sendmail(usuario, [destinatario], mensaje.as_string())

    # Crea un ThreadPoolExecutor para ejecutar las tareas en paralelo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Envía correos a los destinatarios en paralelo
        futures = [executor.submit(enviar, destinatario) for destinatario in destinatarios]

        # Espera a que se completen todas las tareas
        concurrent.futures.wait(futures)


# def enviar_correo(destinatarios, asunto, cuerpo_html):
#     # Configuración de los datos de conexión SMTP de Gmail
#     smtp_host = 'smtp.gmail.com'
#     smtp_port = 587
#     usuario = 'smartuniubicua@gmail.com'
#     contrasena = 'jakldowsuaxsblzj'

#     # Crea el mensaje MIME
#     mensaje = MIMEMultipart('alternative')
#     mensaje['From'] = usuario
#     mensaje['To'] = COMMASPACE.join(destinatarios)
#     mensaje['Subject'] = asunto

#     # Crea la parte HTML del mensaje
#     parte_html = MIMEText(cuerpo_html, 'html')
#     mensaje.attach(parte_html)

#     # Conexión y envío del correo electrónico
#     with smtplib.SMTP(smtp_host, smtp_port) as servidor_smtp:
#         servidor_smtp.starttls()
#         servidor_smtp.login(usuario, contrasena)
#         servidor_smtp.sendmail(usuario, destinatarios, mensaje.as_string())

# # Ejemplo de uso
# destinatarios = ['cmartin2502@gmail.com']
# asunto = 'Prueba de correo electrónico'
# cuerpo_html = '''
# <!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8">
#   <meta http-equiv="X-UA-Compatible" content="IE=edge">
#   <meta name="viewport" content="width=device-width, initial-scale=1.0">
#   <title>Correo Electrónico de SmartUni</title>
#   <link href="https://fonts.googleapis.com/css2?family=Asap+Condensed:wght@400;700&display=swap" rel="stylesheet">
#   <style>
#     /* Estilos generales */
#     body {
#       margin: 0;
#       padding: 0;
#       font-family: Arial, sans-serif;
#       background-color: #1164ce;
#       color: #fff;
#     }

#     .container {
#       max-width: 600px;
#       margin: 0 auto;
#       padding: 20px;
#       background-color: #fff;
#     }

#     /* Estilos del encabezado */
#     .header {
#       text-align: center;
#       margin-bottom: 30px;
#     }

#     .header img {
#       max-width: 200px;
#     }

#     /* Estilos del contenido */
#     .content {
#       text-align: center;
#       margin-bottom: 30px;
#     }

#     .content h1 {
#       font-family: 'Asap Condensed', sans-serif;
#       font-weight: 700;
#     }

#     /* Estilos del pie de página */
#     .footer {
#       text-align: center;
#       font-size: 12px;
#       color: #999;
#     }
#   </style>
# </head>
# <body>
#   <div class="container">
#     <div class="header">
#       <img src="https://i.imgur.com/QVRrfct.png" alt="SmartUni Logo">
#     </div>

#     <div class="content">
#       <h1>Bienvenido a SmartUni</h1>
#       <p>Estimado estudiante,</p>
#       <p>Te damos la bienvenida a SmartUni, la plataforma online inteligente de la Universidad de Alcalá. Estamos emocionados de tenerte como parte de nuestra comunidad.</p>
#       <p>Con SmartUni, podrás acceder a una amplia gama de recursos y de funcionalidados. Estamos comprometidos a brindarte una experiencia educativa de calidad y apoyarte en tu crecimiento académico y profesional.</p>
#       <p>¡Explora nuestra plataforma y descubre nuevas oportunidades de aprendizaje!</p>
#       <p>Atentamente,</p>
#       <p>El equipo de SmartUni</p>
#     </div>

#     <div class="footer">
#       <p>Este correo electrónico fue enviado desde la plataforma SmartUni. Por favor, no respondas a este mensaje.</p>
#     </div>
#   </div>
# </body>
# </html>

# '''

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
        <p>El equipo de SmartUni</p>
      </div>

      <div class="footer">
        <p>Este correo electrónico fue enviado desde la plataforma SmartUni. Por favor, no respondas a este mensaje.</p>
      </div>
    </div>
  </body>
  </html>

  '''
  enviar_correo(destinatarios, asunto, cuerpo_html)
