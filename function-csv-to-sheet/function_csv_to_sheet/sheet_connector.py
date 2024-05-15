import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials


class SheetConnector:
    def __init__(self, id_sheet) -> None:
        scope = ["",
                 "https://www.googleapis.com/auth/script.external_request",
                 "https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/script.container.ui",
                 'https://spreadsheets.google.com/feeds',
                 "https://mail.google.com/",
                 " https://www.googleapis.com/auth/drive"]

        credentials_dict = {
            "type": os.getenv("type", None),
            "project_id": os.getenv("project_id", None),
            "private_key_id": os.getenv("private_key_id", None),
            "private_key": os.getenv("private_key", None).replace("\\n", "\n"),
            "client_email": os.getenv("client_email", None),
            "client_id": os.getenv("client_id", None),
            "auth_uri": os.getenv("auth_uri", None),
            "token_uri": os.getenv("token_uri", None),
            "auth_provider_x509_cert_url": os.getenv("auth_provider_x509_cert_url", None),
            "client_x509_cert_url": os.getenv("client_x509_cert_url", None),
            "universe_domain": os.getenv("universe_domain", None)
        }
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
        self.gc = gspread.authorize(credentials)

        self.sh = self.gc.open_by_url(f'https://docs.google.com/spreadsheets/d/{id_sheet}')

    def get_data(self, worksheet):
        try:
            worksheet = self.sh.worksheet(worksheet)
            return worksheet.get_all_values()
        except gspread.exceptions.WorksheetNotFound:
            print(f"Worksheet {worksheet} not exists...")

    def get_all_worksheets(self):
        return self.sh.worksheets()

    def append(self, worksheet, data):
        try:
            worksheet = self.sh.worksheet(worksheet)
            values = worksheet.get_all_values()
            num_columns = len(values[0])
            num_lines_to_append = len(data)
            i = 1
            while i < num_lines_to_append:
                record = data[i]
                worksheet.append_row(record,
                                    table_range=f"A1:{chr(97 + num_columns)}1") 
                i += 1
                print(f"Line {i} appended..")
                yield
        except gspread.exceptions.WorksheetNotFound:
            print(f"Worksheet {worksheet} not exists...")
