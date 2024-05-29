from flask import Flask
from flask import request, Response

app = Flask(__name__)
print("teste1")

@app.route("/", methods=["GET"])
def test_api():
    print("teste2")
    """Return data of table in reporting dataset connected"""
    return "OK Funcionou", 200
