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
    menu_list = C_MENU_VAR_ITEMS_ID
    for key in menu_list.keys():
        temp = []
        temp.append(key)
        temp.append(menu_list[key])
        items.append(temp)

    message_table[ITEMS_VAR] = items

    return message_table

def order_save(params):
    new_items_list = {}
    message_table = {}

    # reads the params received from the UI
    menu_name = params[MENU_VAR]
    items_list = params[ITEMS_VAR]
    order_id = int(params['ID'])

    # calculates the final cost and total number of items to be packed
    initial_cost, final_cost, del_quantity = cost_calculator(items_list, menu_name)

    for key,value in items_list.items():
        if value > 0:
            new_items_list[key] = value

    params_to_be_inserted = {ORDER_ID_VAR: order_id,
                             MENU_VAR:menu_name,
                             NAME_VAR: '',
                             ROOM_VAR: '',
                             PHONE_VAR: '',
                             PAYMENT_MODE_VAR: '',
                             PAYMENT_ID_VAR: '',
                             ITEMS_VAR : new_items_list,
                             INITIAL_COST_VAR:initial_cost,
                             FINAL_COST_VAR:final_cost,
                             PACKING_CHARGE_VAR: (del_quantity*PACKING_CHARGE),
                             }
    utils_nosql.insert_into_db(params_to_be_inserted)

    message_table['message'] = 'success'

    return message_table

def order_dets(params):
    req = {}
    order_id = params
    list_var = utils_nosql.query_from_db()
    for items in list_var:
        if items[ORDER_ID_VAR] == order_id:
            req[ITEMS_VAR] = items[ITEMS_VAR]

    return req

# def order_prices(params):
#     req = {}
#     order_id = params
#     list_var = utils_nosql.query_from_db()
#     for items in list_var:
#         if items[ORDER_ID_VAR] == order_id:
#             req['food'] = items[INITIAL_COST_VAR]
#
#     print(req)
#     return req


def calculated_prices(params):
    req = {}
    temp = []
    order_id = params
    list_var = utils_nosql.query_from_db()
    for items in list_var:
        if items[ORDER_ID_VAR] == order_id:
            temp.append(items[INITIAL_COST_VAR])
            temp.append(items[PACKING_CHARGE_VAR])
            temp.append(DELIVERY_CHARGE)
            temp.append(items[FINAL_COST_VAR])

    req[ITEMS_VAR] = temp

    return req

def details(order_id,name,room,phone,pay_mode,pay_id):
    utils_nosql.uptdate_in_db(order_id,{NAME_VAR:name})
    utils_nosql.uptdate_in_db(order_id, {ROOM_VAR: room})
    utils_nosql.uptdate_in_db(order_id, {PHONE_VAR: phone})
    utils_nosql.uptdate_in_db(order_id, {PAYMENT_MODE_VAR: pay_mode})
    utils_nosql.uptdate_in_db(order_id, {PAYMENT_ID_VAR: pay_id})

    return order_id

def database_request():
    new_items_list = {}
    items_var = []
    message_table = {}
    list_var = utils_nosql.query_from_db()
    for items in list_var:
        print(items)
        temp = []
        temp.append(items[ORDER_ID_VAR])
        temp.append(items[NAME_VAR])
        temp.append(items[ROOM_VAR])
        temp.append(items[PHONE_VAR])
        temp.append(items[PAYMENT_MODE_VAR])
        temp.append(items[PAYMENT_ID_VAR])
        items_list = items[ITEMS_VAR]
        for key, value in items_list.items():
            if value == 1:
                new_items_list[key] = value
        temp.append(new_items_list)
        items_var.append(temp)

    message_table[ITEMS_VAR] = items_var

    return message_table




############################custom designed functions######################

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
        if item_name == 'Veg Triple Rice (Rs 55)':
            del_quantity = (item_quan*2) + del_quantity
        else:
            del_quantity = item_quan + del_quantity

    final_cost = initial_cost + (del_quantity * PACKING_CHARGE) + DELIVERY_CHARGE

    return initial_cost,final_cost,del_quantity

# def gen_order_id():
#     order_id = 0
#     x = utils_nosql.query_from_db()
#     order_id = len(x)
#
#     return order_id

