import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = '189UzdG5vAlmprVxlSmewp-T7vfPfUPl6vIyWf4SR5xk'
SAMPLE_RANGE_NAME = 'A:H'  # Specify the range A to H to get all columns

def main():
    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)  # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                     range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])
    print(values_input)

        # if not values_input and not values_expansion:
        #     print('No data found.')


    # df = pd.DataFrame(values_input, columns=values_input[0])
    df = pd.DataFrame(values_input)
    df = df.fillna(0)


    # df.to_excel('./excel.xlsx', index=False, header=False)

 # Verifica si values_input no está vacío (ya existe data)
    if values_input:
        # Crea una nueva fila con los valores deseados
        new_row_values = ["New Value 1", "New Value 2", "New Value 3", "New Value 4", "New Value 5", "New Value 6", "New Value 7", "New Value 8"]  # Reemplaza con tus valores reales

        # Encuentra la última fila no vacía en la hoja de cálculo
        last_row = len(values_input) + 1

        # Construye el nuevo rango para agregar la fila sin espacio
        new_range = f'A{last_row}:H{last_row}'

        # Actualiza los valores en la hoja de cálculo
        response = sheet.values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
            range=new_range,
            valueInputOption='RAW',
            body={'values': [new_row_values]}
        ).execute()

        print(f'Nueva fila agregada con respuesta: {response}')

main()






