from constants import *


def a_menu():
    message_table = {}
    items = []
    menu_list = A_MENU_VAR_ITEMS
    for key in menu_list.keys():
        items.append(key)

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
    message_table = {}

    name = params[NAME_VAR]
    room = params[ROOM_VAR]
    phone = params[PHONE_VAR]
    order_id = params[ORDER_ID_VAR]
    pay_mode = params[PAYMENT_MODE_VAR]

    per_details_file_writer(order_id,name,room,phone,pay_mode)


    return message_table
def order_dets(params):
    message_table = {}

    #reads the params received from the UI
    menu_name = params[MENU_VAR]
    items_list = params[ITEMS_VAR]

    #calculates the final cost and total number of items to be packed
    initial_cost, final_cost, del_quantity = cost_calculator(items_list,menu_name)

    #generates and saves order id
    order_id = gen_order_id()

    #writes the order details to a unique txt file based on order id
    details_file_writer(order_id,final_cost,del_quantity)

    message_table[INITIAL_COST_VAR] = initial_cost
    message_table[FINAL_COST_VAR] = final_cost
    message_table[DELIVERY_CHARGE_VAR] = DELIVERY_CHARGE
    message_table[PACKING_CHARGE_VAR] = int(del_quantity * PACKING_CHARGE)
    message_table[ORDER_ID_VAR] = order_id

    return message_table

def cost_calculator(items_list,menu_name):
    #checks which mess
    if menu_name == A_MENU_VAR:
        menu_list = A_MENU_VAR_ITEMS
    else:
        menu_list = C_MENU_VAR_ITEMS
    initial_cost = 0
    del_quantity = 0

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
    order_id_file = open('./text_documents/order_id.txt', 'r')
    order_id = len(order_id_file.readline())
    order_id_file.close()
    order_id_file = open('./text_documents/order_id.txt', 'w')
    order_id_file.write(order_id)
    order_id_file.close()

    return order_id

def details_file_writer(order_id,final_cost,del_quantity):
    text_file_name = 'order_dets_%s.txt' % (str(order_id))
    text_file = open(text_file_name, 'w')
    text_file.write(final_cost)
    text_file.write(del_quantity * PACKING_CHARGE)
    text_file.close()

def per_details_file_writer(order_id,name,room,phone,pay):
    text_file_name = 'order_dets_%s.txt' % (str(order_id))
    text_file = open(text_file_name, 'w')
    text_file.write(name)
    text_file.write(room)
    text_file.write(phone)
    text_file.write(pay)
    text_file.close()
