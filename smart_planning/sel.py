from .controller.DatabaseController import *


def sel_heuristic(rooms_list, apps_list, info_flows_list, ifr_flows_list):
    database_controller = DatabaseController()

    rooms = []
    for r in rooms_list:
        room_object = database_controller.get_entity(r, 'Room')
        print(room_object)