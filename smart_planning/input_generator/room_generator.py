import os
import json
from shapely.geometry import Polygon
from pyproj import Transformer


def generate_room(room_id, industry_id, coordinates):
    if not os.path.exists('evaluation'):
        os.makedirs('evaluation')

    polygon = Polygon(coordinates)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:32722", always_xy=True)
    projected_coords = [transformer.transform(x, y) for x, y in polygon.exterior.coords]
    projected_polygon = Polygon(projected_coords)
    total_area = projected_polygon.area

    room_data = {
        "id": room_id,
        "type": "Room",
        "description": f"Room in industry id {industry_id}",
        "containedInBuilding": industry_id,
        "floorLevel": 1,
        "floorSize": total_area,
        "peopleCapacity": int(total_area // 2),
        "peopleOccupancy": int(total_area // 4),
        "location": {
            "type": "Polygon",
            "coordinates": coordinates
        }
    }

    room_filename = f"evaluation/{room_id}.json"
    with open(room_filename, 'w') as room_file:
        json.dump(room_data, room_file, indent=2)
