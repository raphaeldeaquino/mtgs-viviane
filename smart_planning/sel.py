import json

from .controller.DatabaseController import *
from .model.Room import *


def sel_heuristic(rooms_list, apps_list, info_flows_list, ifr_flows_list):
    database_controller = DatabaseController()

    rooms = []
    for r in rooms_list:
        room_object = database_controller.get_entity(r, 'Room')
        room_dict = json.loads(room_object[2])
        room = Room(room_dict)
        rooms.append(room)
