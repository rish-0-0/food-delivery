from constants import *
import utils_nosql


def a_menu():
    message_table = {}
    items = []
    menu_list = A_MENU_VAR_ITEMS_ID
    for key in menu_list.keys():
        temp = []
        temp.append(key)
        temp.append(menu_list[key])
        items.append(temp)

    message_table[ITEMS_VAR] = items

    return message_table


def c_menu():
    message_table = {}
    items = []
    menu_list = C_MENU_VAR_ITEMS
    for key in menu_list.keys():
        items.append(key)

    message_table[ITEMS_VAR] = items

    return message_table

def details(params):

    name = params[NAME_VAR]
    room = params[ROOM_VAR]
    phone = params[PHONE_VAR]
    order_id = params[ORDER_ID_VAR]
    pay_mode = params[PAYMENT_MODE_VAR]
    pay_id = params[PAYMENT_ID_VAR]

    utils_nosql.uptdate_in_db(order_id,{NAME_VAR:name})
    utils_nosql.uptdate_in_db(order_id, {ROOM_VAR: room})
    utils_nosql.uptdate_in_db(order_id, {PHONE_VAR: phone})
    utils_nosql.uptdate_in_db(order_id, {PAYMENT_MODE_VAR: pay_mode})
    utils_nosql.uptdate_in_db(order_id, {PAYMENT_ID_VAR: pay_id})

    return order_id

def order_dets(params):
    req = {}
    order_id = params['order_id']
    list_var = utils_nosql.query_from_db()
    for item in list_var:
        if item[ORDER_ID_VAR] == order_id:
            req = item

    return req

def cost_calculator(items_list_ui,menu_name):
    items_list = []

    #checks which mess
    if menu_name == A_MENU_VAR:
        menu_list = A_MENU_VAR_ITEMS
    else:
        menu_list = C_MENU_VAR_ITEMS
    initial_cost = 0
    del_quantity = 0

    for value in items_list_ui.items():
        temp = list(value)
        items_list.append(temp)

    #loops through each item ordered by user and adds corresponding cost
    for item in items_list:
        item_name = item[0]
        item_quan = item[1]
        temp_cost = int(menu_list[item_name]) * int(item_quan)
        initial_cost = initial_cost + temp_cost
        if item_name == 'Veg Triple Rice (Rs.55)':
            del_quantity = (item_quan*2) + del_quantity
        else:
            del_quantity = item_quan + del_quantity

    final_cost = initial_cost + (del_quantity * PACKING_CHARGE) + DELIVERY_CHARGE

    return initial_cost,final_cost,del_quantity

def gen_order_id():
    order_id = 0
    x = utils_nosql.query_from_db()
    order_id = len(x)

    return order_id

def order_save(params):
    message_table = {}

    # reads the params received from the UI
    menu_name = params[MENU_VAR]
    items_list = params[ITEMS_VAR]

    # calculates the final cost and total number of items to be packed
    initial_cost, final_cost, del_quantity = cost_calculator(items_list, menu_name)

    # generates and saves order id
    order_id = gen_order_id()

    params_to_be_inserted = {ORDER_ID_VAR: order_id,
                             NAME_VAR: '',
                             ROOM_VAR: '',
                             PHONE_VAR: '',
                             PAYMENT_MODE_VAR: '',
                             PAYMENT_ID_VAR: '',
                             INITIAL_COST_VAR:initial_cost,
                             FINAL_COST_VAR:final_cost,
                             PACKING_CHARGE_VAR: (del_quantity*PACKING_CHARGE),
                             }
    utils_nosql.insert_into_db(params_to_be_inserted)

    message_table['message'] = 'success'
    message_table['order_id'] = int(order_id)

    return message_table
