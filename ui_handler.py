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
    initial_cost, del_quantity = cost_calculator(items_list, menu_name)

    for key,value in items_list.items():
        if value > 0:
            new_items_list[key] = value

    params_to_be_inserted = {ORDER_ID_VAR: order_id,
                             MENU_VAR:menu_name,
                             NAME_VAR: '',
                             'hostel': '',
                             ROOM_VAR: '',
                             PHONE_VAR: '',
                             PAYMENT_MODE_VAR: '',
                             PAYMENT_ID_VAR: '',
                             ITEMS_VAR : new_items_list,
                             INITIAL_COST_VAR:initial_cost,
                             FINAL_COST_VAR:0,
                             PACKING_CHARGE_VAR: (del_quantity*PACKING_CHARGE),
                             DELIVERY_CHARGE_VAR : 0,
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
            temp.append(int(items[DELIVERY_CHARGE_VAR]))
            temp.append(items[FINAL_COST_VAR])

    req[ITEMS_VAR] = temp

    return req

def details(order_id,name,phone,pay_mode,pay_id):
    utils_nosql.uptdate_in_db(order_id,{NAME_VAR:name})
    utils_nosql.uptdate_in_db(order_id, {PHONE_VAR: phone})
    utils_nosql.uptdate_in_db(order_id, {PAYMENT_MODE_VAR: pay_mode})
    utils_nosql.uptdate_in_db(order_id, {PAYMENT_ID_VAR: pay_id})

    return order_id

def hostel_details(order_id,hostel,room):
    utils_nosql.uptdate_in_db(order_id,{'hostel':hostel})
    utils_nosql.uptdate_in_db(order_id, {ROOM_VAR: room})

    list_var = utils_nosql.query_from_db()

    for items in list_var:
        if int(items[ORDER_ID_VAR]) == order_id:
            menu_name = items[MENU_VAR]
            intial_cost = items[INITIAL_COST_VAR]
            pack_char = items[PACKING_CHARGE_VAR]

    final_cost,delivery_charge = final_cost_calc(menu_name,intial_cost,pack_char,hostel)

    utils_nosql.uptdate_in_db(order_id, {FINAL_COST_VAR: final_cost})
    utils_nosql.uptdate_in_db(order_id, {DELIVERY_CHARGE_VAR: delivery_charge})

    return order_id

def database_request():
    items_var = []
    message_table = {}
    list_var = utils_nosql.query_from_db()
    for items in list_var:
        temp = []
        if items[NAME_VAR] == '':
            continue
        else:
            temp.append(items[MENU_VAR])
            temp.append(items[FINAL_COST_VAR])
            temp.append(items[NAME_VAR])
            temp.append(items[ROOM_VAR])
            temp.append(items[PHONE_VAR])
            temp.append(items[PAYMENT_MODE_VAR])
            temp.append(items[PAYMENT_ID_VAR])
            items_list = items[ITEMS_VAR]
            temp.append(items_list)
            items_var.append(temp)

    message_table[ITEMS_VAR] = items_var
    print(message_table)

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
        if item_name == 'Veg Triple Rice (Rs 55)' or item_name == 'Chicken Triple Rice (Rs 75)' or item_name =='Chicken Triple Fried Rice (Rs 76)' or item_name == 'Veg Triple Fried Rice (Rs 55)':
            del_quantity = (item_quan*2) + del_quantity
        elif item_name in DRINKS_LIST:
            del_quantity = del_quantity
        else:
            del_quantity = item_quan + del_quantity

    return initial_cost,del_quantity

def final_cost_calc(menu_name,initial_cost,packing_charge,hostel):
    total_intial_cost = initial_cost + packing_charge

    if hostel in BRACKET1:
        delivery_charge_var = DELIVERY_CHARGE_1
        del_per = DELIVER_PERCENT_1
    elif hostel in BRACKET2:
        delivery_charge_var = DELIVERY_CHARGE_2
        del_per = DELIVER_PERCENT_2
    elif hostel in BRACKET3:
        delivery_charge_var = DELIVERY_CHARGE_3
        del_per = DELIVER_PERCENT_3
    else:
        delivery_charge_var = 10
        del_per = 0.1

    if total_intial_cost < 150:
        delivery_charge = delivery_charge_var
    else:
        delivery_charge = (del_per * total_intial_cost)

    if menu_name == A_MENU_VAR:
        if hostel in C_SIDE:
            cross = EXTRA_DELIVERY_CHARGE
        else:
            cross = 0
    else:
        if hostel in A_SIDE:
            cross = EXTRA_DELIVERY_CHARGE
        else:
            cross = 0

    delivery_charge = delivery_charge + cross

    final_cost = initial_cost + packing_charge + delivery_charge

    return final_cost,delivery_charge

# def gen_order_id():
#     order_id = 0
#     x = utils_nosql.query_from_db()
#     order_id = len(x)
#
#     return order_id

