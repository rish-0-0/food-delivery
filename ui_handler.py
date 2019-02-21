from constants import *
import utils_nosql


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

def total_calculator(params):
    message_table = {}

    return message_table
def order_dets(params):
    items_list = params[ITEMS_VAR]
