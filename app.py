from flask import Flask
from flask import jsonify


app = Flask(__name__)


@app.route("/")
def get_app_version():
    app_data = {
        "service": "NHS Emergency Department Wait Times Aggregator API",
        "github": "https://github.com/smart-plymouth/aggregator-nhs-ed-wait-times",
        "version": 1.0
    }
    return jsonify(app_data)
