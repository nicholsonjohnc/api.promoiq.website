from demand_log_log_cross_item import DemandLogLogCrossItem
# import json

from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return 'John Rules!!!!'
    
@app.route("/v1/model", methods=['GET'])
def generate_model():
    return DemandLogLogCrossItem(N_items=3, T_periods=5, type_of_items='substitute', random_state=0).dump_model()
    


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=8080)
