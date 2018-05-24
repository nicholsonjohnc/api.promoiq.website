from demand_log_log_cross_item import DemandLogLogCrossItem
from price_discrete import PriceDiscrete
from plot_promotion_plan import PlotPromotionPlan
import json
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
    params = request.get_json()
    return DemandLogLogCrossItem(N_items=params['N_items'], T_periods=params['T_periods'], type_of_items=params['type_of_items']).dump_model()

@app.route("/v1/plot", methods=['POST'])
def plot():
    params = request.get_json()
    model = DemandLogLogCrossItem().load_model(json.dumps(params))
    price = PriceDiscrete(model=model)
    plot = PlotPromotionPlan(model=model, price=price).plot()
    # return plot
    return Response(plot, mimetype='text/xml')
    # return jsonify(price.gamma_decision_variable)
 
if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True, port=80)
    app.run(host='127.0.0.1', debug=True, port=8080)
