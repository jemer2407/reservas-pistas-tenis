# SCRIPT para manipular hojas de cálculo de Google Sheets

import gspread

class GoogleSheets:
    def __init__(self, credentials, document, sheet_name):
        self.gc = gspread.service_account_from_dict(credentials)    # autenticarnos
        self.sh = self.gc.open(document)    # abrir el documento
        self.sheet = self.sh.worksheet(sheet_name)  # activar la hoja
    
    def write_data(self, range, data):  # metodo para escribir en la hoja de calculo
        self.sheet.update(range, data)
    
    def get_last_row_range(self):   # metodo para saber cual es la ultima fila con datos
        last_row = len(self.sheet.get_all_values()) + 1 # primera fila vacia para escribir un registro
        data = self.sheet.get_values()  # todos los valores de la hoja de calculo
        range_start = f"A{last_row}"    # rango de inicio
        range_end = f"{chr(ord('A') + len(data[0]) - 1)}{last_row}"    # rango final
        #range_end = f"G{last_row}"
        return f"{range_start}:{range_end}"