from google.cloud import storage
from google.oauth2 import service_account
import json
import duckdb

# CONEXÃO COM O CLOUD STORAGE E BUCKET
with open("interact_with_gcs/credentials.json", "r") as f:
    credentials = json.loads(f.read())

credentials = service_account.Credentials.from_service_account_info(credentials)

storage_client = storage.Client(credentials=credentials)

bucket_example_apoena = storage_client.bucket("example-apoena")

# CONSUMO DE DADOS
# blob = bucket_example_apoena.blob("objetos/apoena.txt")
# blob.download_to_filename(filename="apoena_from_gcs.txt")

# ENVIO DE DADOS
# blob = bucket_example_apoena.blob("objetos/dados.csv")
# blob.upload_from_filename("interact_with_gcs/teste.csv")

# CONEXÃO COM O DUCKDB
duckdb.sql("INSTALL httpfs")
duckdb.sql("""CREATE SECRET IF NOT EXISTS (
    TYPE GCS,
    KEY_ID 'CHAVE',
    SECRET 'SECRET'
);""")

print(duckdb.sql("SELECT * FROM read_csv('gs://example-apoena/objetos/dados.csv')").show())
