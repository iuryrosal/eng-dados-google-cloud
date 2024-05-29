from flask import Flask
from flask import request, Response

app = Flask(__name__)

@app.route("/", methods=["GET"])
def test_api():
    """Return data of table in reporting dataset connected"""
    return "OK Funcionou", 200