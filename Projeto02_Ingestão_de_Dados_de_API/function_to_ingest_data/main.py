import os
import pandas as pd
import duckdb

from api_connector import APIFreeCurrency
from secret_manager import SecretManager


def collect_data(request):
    secret_manager = SecretManager()
    token = secret_manager.access_secret(secret_id=os.getenv("secret_id"),
                                        version_id=1)

    key_id = os.getenv("chave", None)
    secret = os.getenv("secret", None)

    if not key_id or not secret:
        raise Exception("Segredos HMAC Keys faltantes...")

    duckdb.sql(f"""
                    CREATE SECRET IF NOT EXISTS (
                        TYPE GCS,
                        KEY_ID '{key_id}',
                        SECRET '{secret}');
        """)

    api_client = APIFreeCurrency(token=token)
    response_json = api_client.get_latest_exchange_rates(base_currency="BRL")
    data = response_json["data"]

    table_dict = {
        "currency": [],
        "value_exchange_from_BRL": []
    }
    for key, value in data.items():
        table_dict["currency"].append(key)
        table_dict["value_exchange_from_BRL"].append(value)

    exchange_rates_df = pd.DataFrame.from_dict(table_dict)

    duckdb.sql("""
                CREATE OR REPLACE TABLE exchange_rates AS
                SELECT * FROM exchange_rates_df;
            """)
    duckdb.sql("""
                ALTER TABLE exchange_rates
                ADD COLUMN timestamp_extraction TIMESTAMP
                DEFAULT current_timestamp;
            """)

    duckdb.sql("COPY (SELECT * EXCLUDE(timestamp_extraction), CAST(timestamp_extraction AS VARCHAR) AS timestamp_str FROM exchange_rates) TO 'gs://csvs_to_sheets/1mYDfBCtj3GSm_H1vnocqEcQpcdP3tNy2rumtP4BRB7I.csv' (HEADER, DELIMITER ',');")

    return "Done"
