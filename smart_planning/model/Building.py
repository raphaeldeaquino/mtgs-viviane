from shapely.geometry import Polygon, Point
from .GeoJSONPolygon import *


class Building:

    def __init__(self, building_dict):
        try:
            if building_dict["type"] != "Building":
                raise ValueError("Invalid building dictionary: 'type' must be 'Building'")

            if building_dict["location"]["type"] != "Polygon":
                raise ValueError("Invalid building dictionary: 'type' of 'location' must be 'Polygon'")

            self.id = building_dict["id"]
            self.type = "Building"
            self.description = building_dict["description"] if "description" in building_dict else None
            self.location = GeoJSONPolygon(building_dict["location"]["coordinates"][0])
            if not self.is_valid_candidate_locations(building_dict["candidateLocations"]):
                raise ValueError("One or more points in 'candidateLocations' is outside 'location'")
            else:
                self.candidateLocations = building_dict["candidateLocations"]
            self.floorsAboveGround = building_dict["floorsAboveGround"] if "floorsAboveGround" in building_dict else None
            self.floorsBelowGround = building_dict["floorsBelowGround"] if "floorsBelowGround" in building_dict else None
            self.openingHours = building_dict["openingHours"] if "openingHours" in building_dict else None
            self.peopleCapacity = building_dict["peopleCapacity"] if "peopleCapacity" in building_dict else None
            self.peopleOccupancy = building_dict["peopleOccupancy"] if "peopleOccupancy" in building_dict else None
        except KeyError as e:
            raise ValueError(f"Invalid room dictionary: {e} not found")

    def is_valid_candidate_locations(self, points):
        # Convertendo as coordenadas do polígono GeoJSON para o formato suportado pelo Shapely.
        polygon_shapely = Polygon(self.location.coordinates)

        # Verificando se cada par de números está dentro do polígono.
        for par in points:
            point = Point(par['location'])
            if not polygon_shapely.contains(point):
                print(polygon_shapely)
                print(point)
                return False

        return True