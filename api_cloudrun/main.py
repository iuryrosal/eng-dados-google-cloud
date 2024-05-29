from flask import Flask
from src.cloud_storage import CloudStorage

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health_check():
    return "OK Funcionou", 200


@app.route("/curriencies", methods=["GET"])
def get_curriencies():
    gcs = CloudStorage(bucket_name="csvs_to_sheets")
    str_content = gcs.pick_object(blob_name="1mYDfBCtj3GSm_H1vnocqEcQpcdP3tNy2rumtP4BRB7I.csv")
    return str_content, 200
