import imaplib
import email
from email.header import decode_header
import os
# import gspread
import pygsheets

# from oauth2client.service_account import ServiceAccountCredentials

# Configura tus credenciales de Gmail
email_address = "camorcillos@gmail.com"
password = "jayb ilui iwct kaew"

# Conéctate al servidor IMAP de Gmail
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(email_address, password)

# Selecciona la bandeja de entrada
mail.select("inbox")

# Define el criterio de búsqueda (en este caso, buscar correos con un texto específico en el cuerpo)
search_criteria = '(BODY "#18228")'

save_directory = "./files"

if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Realiza la búsqueda y obtén el ID del correo que contiene el adjunto
status, email_ids = mail.search(None, search_criteria)

if status == "OK":
    email_ids = email_ids[0].split()  # Convierte los IDs de correo en una lista de números
    if len(email_ids) > 0:
        # Obtén el primer correo que cumple con el criterio de búsqueda
        email_id = email_ids[0]

        # Descarga el correo completo
        status, msg_data = mail.fetch(email_id, "(RFC822)")

        if status == "OK":
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Recorre las partes del correo para buscar adjuntos
            for part in msg.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                if part.get("Content-Disposition") is None:
                    continue

                # Si es un adjunto, descárgalo
                filename = part.get_filename()
                if filename:
                    # Decodifica el nombre del archivo si es necesario
                    filename = email.header.decode_header(filename)[0][0]
                    if filename:
                        # Construye la ruta completa al archivo en la carpeta "files"
                        file_path = os.path.join(save_directory, filename)
                        
                        # Extrae el número del nombre del archivo descargado
                        numero_de_orden = filename.split("TicketOrder")[1].split(".")[0]

                        print(f"Número de Orden del archivo descargado: {numero_de_orden}")

                        # Guarda el adjunto en la carpeta "files"
                        with open(file_path, "wb") as f:
                            f.write(part.get_payload(decode=True))
else:
    print("Error al buscar correos.")

# Cierra la conexión
mail.logout()

# # Obtiene el ID de la hoja de cálculo
# spreadsheet_url  = "https://docs.google.com/spreadsheets/d/189UzdG5vAlmprVxlSmewp-T7vfPfUPl6vIyWf4SR5xk/edit?usp=sharing"

# # spreadsheet = gspread.open_by_url(spreadsheet_id)
# # Abre la hoja de cálculo
# # spreadsheet = gspread.open_by_url(spreadsheet_id)

# # # Obtiene la primera hoja de cálculo
# # worksheet = spreadsheet.get_worksheet(0)

# # # Escribe en la celda A1
# # worksheet.update_cell(2, 2, numero_de_orden)

# # # Guarda los cambios
# # worksheet.save()

# gc = pygsheets.authorize()
# # spreadsheet = gc.open_by_url(spreadsheet_url)
# sh = gc.open(spreadsheet_url)
# # Selecciona la primera hoja de cálculo
# worksheet = sh.sheet1

# # Escribe en la celda B2
# worksheet.update_value("B2", numero_de_orden)
