import streamlit as st
from streamlit_option_menu import option_menu
from send_email import send_email # type: ignore
import re
from google_sheets import GoogleSheets # type: ignore
import uuid
from google_calendar import GoogleCalendar # type: ignore
import numpy as np
import datetime as dt
from datetime import datetime, timedelta

page_title = "Reservas Escuderia Alba"
page_icon = "assets/icono_escuderia_alba.ico"
layout="centered"

horas = ["09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00"]
pistas = ["Pista 1","Pista 2","Pista 3","Pista 4"]

document = "gestion-reservas-tenis"
sheet = "reservas"
credentials = st.secrets["google"]["credentials_google"]
idcalendar = 'webseocordoba@gmail.com'
idcalendar2 = 'f1eb15ac3d2fa90c99f66cda5d68982dea3412cf555a658e907f6699022b29b9@group.calendar.google.com'
idcalendar3 = 'ff8e01d3b42da6c6e827f6b871a55fb2de998e5b22d11c9d913f27a6b546e576@group.calendar.google.com'
idcalendar4 = 'dcd2e2c1eded2fa3877ef32a2cb7b38e28b3715bfec6c87cf4b3960aeb39c3a6@group.calendar.google.com'
time_zone = 'Europe/Madrid'

# -------- FUNCIONES --------
# funcion para validar formato del email
def formatocorreo(correo):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(patron, correo):
        return True
    else:
        return False

def generate_uid():
    return str(uuid.uuid4())


def sumar_una_hora(hora_str):
    # Convertir la cadena de hora a un objeto datetime
    hora = dt.datetime.strptime(hora_str, '%H:%M')
    
    # Sumar una hora
    nueva_hora = hora + dt.timedelta(hours=1)
    
    # Convertir el objeto datetime de nuevo a una cadena con el mismo formato
    return nueva_hora.strftime('%H:%M')
# ---------------------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.image("assets/banner.jpg")
st.title("Club de Tenis Córdoba")
st.text("Calle Los Tenistas de Córdoba, nº 10")

opcion = option_menu(menu_title=None, options=["Reservar","Pistas","Detalles"],icons=["calendar-date","building","clipboard-minus"], orientation="horizontal")

if opcion=="Detalles":
    
    
    st.subheader("Ubicación")
    st.markdown("""<iframe src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d1227.5487766992082!2d-4.8053174!3d37.9124114!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd6cdf2e179aba81%3A0x6eb276d3beff43c5!2sEscuder%C3%ADa%20Alba%20de%20C%C3%B3rdoba!5e1!3m2!1ses-419!2ses!4v1719469549986!5m2!1ses-419!2ses" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>""", unsafe_allow_html=True)

    
    st.subheader("Horarios")
    dia,hora = st.columns(2)

    dia.text("Lunes")
    hora.text("10:00 - 23:00")
    dia.text("Martes")
    hora.text("10:00 - 23:00")
    dia.text("Miercoles")
    hora.text("10:00 - 23:00")
    dia.text("Jueves")
    hora.text("10:00 - 23:00")
    dia.text("Viernes")
    hora.text("10:00 - 23:00")
    dia.text("Sábado")
    hora.text("09:00 - 23:00")
    dia.text("Domingo")
    hora.text("09:00 - 23:00")    

    st.subheader("Contacto")
    st.text("📞 957275098")
    st.subheader("Facebook")
    st.markdown("Síguenos [aquí](https://www.facebook.com/clubescuderiaalba?locale=es_ES) en Facebook")    

if opcion == "Pistas":

    st.image("assets/pista1.jpg", caption="Pista 1")
    st.image("assets/pista2.jpg", caption="Pista 2")
    st.image("assets/pista3.jpg", caption="Pista 3")
    st.image("assets/pista4.jpg", caption="Pista 4")

if opcion == "Reservar":

    st.subheader("Reservar")

    c1, c2 = st.columns(2)

    nombre = c1.text_input("Tu nombre*")
    email = c2.text_input("Tu email*")
    fecha = c1.date_input("Fecha")
    pista = c1.selectbox("Pista",pistas)
    if fecha:
        if pista == "Pista 1":
            id = idcalendar
        elif pista == "Pista 2":
            id = idcalendar2
        elif pista == "Pista 3":
            id = idcalendar3
        elif pista == "Pista 4":
            id = idcalendar4
        calendar = GoogleCalendar(credentials, id)  # nos autenticamos
        hours_blocked = calendar.get_events_start_time(str(fecha))
        result_hours = np.setdiff1d(horas, hours_blocked)
    hora = c2.selectbox("Hora",result_hours)
    
    notas = c2.text_area("Notas")

    enviar = st.button("Enviar")

    # ---------- BACKEND ----------

    if enviar: # si se pulsa el botón enviar

        with st.spinner("Cargando..."):

            if nombre == "":
                st.warning("Introduzca el nombre")
            elif email == "":
                st.warning("Introduzca el email")
            elif not formatocorreo(email):
                st.warning("Formato de email incorrecto")              
            else:
                # Crear evento en google calendar

                parsed_time = dt.datetime.strptime(hora, "%H:%M").time()
                hours1 = parsed_time.hour
                minutes1 = parsed_time.minute
                
                end_hours = sumar_una_hora(hora)

                parsed_time2 = dt.datetime.strptime(end_hours, "%H:%M").time()
                hours2 = parsed_time2.hour
                minutes2 = parsed_time2.minute

                start_time = dt.datetime(fecha.year,fecha.month,fecha.day,hours1,minutes1).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                end_time = dt.datetime(fecha.year,fecha.month,fecha.day,hours2,minutes2).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                calendar = GoogleCalendar(credentials, id)  # nos autenticamos
                calendar.create_event(nombre, start_time, end_time, time_zone)

                # Crear registro en google sheets
                uid = generate_uid()
                data = [[nombre,email,pista,str(fecha),hora,notas,uid]]
                gs = GoogleSheets(credentials, document, sheet)
                range = gs.get_last_row_range()
                gs.write_data(range,data)

                # enviar email al usuario
                send_email(email,nombre,fecha,hora,pista)

                st.success("Su pista ha sido reservada con éxito")

    