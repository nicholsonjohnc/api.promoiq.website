from demand_log_log_cross_item import DemandLogLogCrossItem
from price_discrete import PriceDiscrete
from plot_promotion_plan import PlotPromotionPlan
# import json
# from demand import Demand
from flask import Flask, jsonify, Response, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

#from demand import Demand

@app.route("/", methods=['GET'])
def hello():
    return 'John Rules!'
    
@app.route("/v1/create", methods=['POST'])
def create():
    # params = request.get_json()
    # return DemandLogLogCrossItem(N_items=params['N_items'], T_periods=params['T_periods'], type_of_items=params['type_of_items']).dump_model()
    # return DemandLogLogCrossItem(N_items=3, T_periods=13, type_of_items='substitute').dump_model()
    return jsonify(method=request.data)

@app.route("/v1/plot", methods=['GET'])
def plot():
    demand = DemandLogLogCrossItem(N_items=3, T_periods=5, type_of_items='substitute')
    price = PriceDiscrete(demand.model)
    plot = PlotPromotionPlan(model=demand.model, price=price).plot()
    # return plot
    return Response(plot, mimetype='text/xml')
 
if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True, port=80)
    app.run(host='127.0.0.1', debug=True, port=8080)
