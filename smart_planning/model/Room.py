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
            if not self.is_valid_candidate_locations(room_dict["candidateLocations"]):
                raise ValueError("One or more points in 'candidateLocations' is outside 'location'")
            else:
                self.candidateLocations = room_dict["candidateLocations"]
            self.floorLevel = room_dict["floorLevel"] if "floorLevel" in room_dict else None
            self.floorSize = room_dict["floorSize"] if "floorSize" in room_dict else None
            self.peopleCapacity = room_dict["peopleCapacity"] if "peopleCapacity" in room_dict else None
            self.peopleOccupancy = room_dict["peopleOccupancy"] if "peopleOccupancy" in room_dict else None
        except KeyError:
            raise ValueError("Invalid room dictionary")

    def is_valid_candidate_locations(self, points):
        # Convertendo as coordenadas do polígono GeoJSON para o formato suportado pelo Shapely.
        polygon_shapely = Polygon(self.location.coordinates)

        # Verificando se cada par de números está dentro do polígono.
        for par in points:
            point = Point(par)
            if not polygon_shapely.contains(point):
                return False

        return True

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
        room_str += "Candidate Locations:\n"
        for index, point in enumerate(self.candidateLocations):
            room_str += f"Point {index + 1}: {point}\n"

        return room_str
