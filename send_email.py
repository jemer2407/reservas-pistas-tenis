import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

def send_email(email, nombre, fecha, hora, pista):

    # credenciales
    user = st.secrets["emails"]["smtp_user"]
    password = st.secrets["emails"]["smtp_password"]

    sender_email = "Club de Tenis Córdoba"

    # configuracion del servidor
    msg = MIMEMultipart()

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # parametros del mensaje
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Reserva de pista"

    # Cuerpo del mensaje
    mensaje = f"""
    Hola {nombre},
    Su reserva ha sido realizada con éxito.
    Fecha: {fecha}
    Hora: {hora}
    Pista: {pista}

    Gracias por confiar en nosotros.
    Un saludo.
    """

    msg.attach(MIMEText(mensaje,'plain'))

    # Conexión al servidor
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)   # configuracion servidor
        server.starttls()   # inicializamos el servidor
        server.login(user,password) # nos logueamos
        server.sendmail(sender_email, email, msg.as_string())   # envio de correo
        server.quit()   # cerramos la conexion con el servidor
    except smtplib.SMTPException as e:
        st.error("Error al enviar el email")



