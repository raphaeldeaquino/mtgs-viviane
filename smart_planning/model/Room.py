from shapely.geometry import Polygon, Point
from .GeoJSONPolygon import *


class Room:

    def __init__(self, room_dict):
        try:
            if room_dict["type"] != "Room":
                raise ValueError("Invalid room dictionary: 'type' must be 'Room'")

            if room_dict["location"]["type"] != "Polygon":
                raise ValueError("Invalid room dictionary: 'type' of 'location' must be 'Polygon'")

            self.id = room_dict["id"]
            self.type = "Room"
            self.description = room_dict["description"] if "description" in room_dict else None
            self.location = GeoJSONPolygon(room_dict["location"]["coordinates"][0])
            self.floorLevel = room_dict["floorLevel"] if "floorLevel" in room_dict else None
            self.floorSize = room_dict["floorSize"] if "floorSize" in room_dict else None
            self.peopleCapacity = room_dict["peopleCapacity"] if "peopleCapacity" in room_dict else None
            self.peopleOccupancy = room_dict["peopleOccupancy"] if "peopleOccupancy" in room_dict else None
        except KeyError:
            raise ValueError("Invalid room dictionary")

    def __str__(self):
        # Construindo a representação em string do objeto Room
        room_str = f"Room ID: {self.id}\n"
        room_str += f"Description: {self.description}\n"
        room_str += f"Floor Level: {self.floorLevel}\n"
        room_str += f"Floor Size: {self.floorSize}\n"
        room_str += f"People Capacity: {self.peopleCapacity}\n"
        room_str += f"People Occupancy: {self.peopleOccupancy}\n"
        room_str += "Location Coordinates:\n"
        room_str += str(self.location) + "\n"  # chamando __str__ de GeoJSONPolygon

        return room_str
