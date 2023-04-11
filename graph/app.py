from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/data')
def get_data():
    data = [
        {"Customers": "Who are our sales targets and will purchase our offerings?"},
        {"Brand Message": "How should our brand be perceived in order to sell our offerings?"},
        {"Offerings": "What combination of products and services do we offer our target groups?"}
    ]
    return jsonify(data)

if __name__ == '__main__':
    app.run()
