from flask import Flask
from flask import request, Response
from api_cloudrun.src.cloud_storage import CloudStorage

app = Flask(__name__)


@app.route("/", methods=["GET"])
def test_api():
    """Return data of table in reporting dataset connected"""
    return "OK Funcionou", 200


@app.route("/currencies", methods=["GET"])
def pick_currencies():
    """Return data of table in reporting dataset connected"""
    try:
        gcs = CloudStorage()
        return gcs.pick_object("gs://csvs_to_sheets/1mYDfBCtj3GSm_H1vnocqEcQpcdP3tNy2rumtP4BRB7I.csv"), 200
    except Exception as e:
        return str(e), 500