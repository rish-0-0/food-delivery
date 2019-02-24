from flask import Flask, render_template, request
from flask import jsonify
import ui_handler
import json
from flask_cors import CORS
import utils_nosql
from constants import *

utils_nosql.drop_col()
params_to_be_inserted = {ORDER_ID_VAR: 0,
                             NAME_VAR: '',
                             ROOM_VAR: '',
                             PHONE_VAR: '',
                             PAYMENT_MODE_VAR: '',
                             PAYMENT_ID_VAR: '',
                             INITIAL_COST_VAR: 1,
                             FINAL_COST_VAR: 2,
                             PACKING_CHARGE_VAR: (2 * PACKING_CHARGE),
                             }
utils_nosql.insert_into_db(params_to_be_inserted)

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['POST'])
def handle_request():
    response = ""
    json_response = ""

    # Get the json from the request

    req = request.get_json()

    # Get the command from the json
    action = req.get('command')

    if action == 'a_menu':
        response = ui_handler.a_menu()
        print(response)
        json_response = jsonify(response)

    elif action == 'c_menu':
        json_response = jsonify(ui_handler.c_menu())

    elif action == 'order_dets_save':
        params = req.get('params')
        json_response = jsonify(ui_handler.order_save(params))

    elif action == 'order_dets_saved_request':
        params = req.get('params')
        json_response = jsonify(ui_handler.order_dets(params))

    elif action == 'order_prices':
        params = req.get('params')
        json_response = jsonify(ui_handler.order_prices(params))

    elif action == 'calculated_prices':
        params =req.get('params')
        json_response = jsonify(ui_handler.calculated_prices(params))

    return json_response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s' % page_name)

@app.route('/form-handler',methods=['POST'])
def form():
    name = request.form[NAME_VAR]
    room = request.form[ROOM_VAR]
    phone = request.form[PHONE_VAR]
    pay_mode = request.form[PAYMENT_MODE_VAR]
    pay_id = request.form[PAYMENT_ID_VAR]

    ui_handler.details(order_id,name,room,phone,pay_mode,pay_id)

    json_res = jsonify({})
    return json_res


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)
