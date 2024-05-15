import duckdb
from datetime import datetime
import os
from sheet_connector import SheetConnector


def transfer_csv_to_sheets(event, context):
    source_bucket = event["bucket"]
    source_object_name = event["name"]

    source_object_path = f"gs://{source_bucket}/{source_object_name}"
    print(f"{source_object_path=}")

    key_id = os.getenv("chave", None)
    secret = os.getenv("secret", None)

    duckdb.sql(f"""
                CREATE SECRET IF NOT EXISTS (
                    TYPE GCS,
                    KEY_ID '{key_id}',
                    SECRET '{secret}');
    """)

    data = duckdb.sql(
        f"SELECT * FROM read_csv('{source_object_path}', header=true, delim=',');"
    ).fetchall()

    print(source_object_name[0:-4])
    sheet_cnn = SheetConnector(source_object_name[0:-4])
    curr_year = str(datetime.now().year)
    num_lines_to_append = len(data)
    sheet_data = sheet_cnn.append(curr_year, data)
    del data

    while True:
        try:
            next(sheet_data)
        except StopIteration:
            break
    return f"{num_lines_to_append} added in {source_object_name[0:-4]} sheet id"
