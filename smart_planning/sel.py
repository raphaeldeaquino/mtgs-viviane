import json
from shapely.geometry import Polygon, Point
from shapely.ops import transform
from functools import partial
import pyproj

from .controller.DatabaseController import *
from .model.Room import *
from .model.SoftwareApplication import *
from .model.InformationFlow import *
from .model.InfrastructureFlow import *
from .model.Building import *


def check_sensor_coverage(polygon, sensor_location, sensor_range):
    # Converte as coordenadas do polígono em uma forma geométrica Shapely
    polygon_shape = Polygon(polygon.coordinates[0])

    # Converte as coordenadas do sensor para um objeto Point Shapely
    sensor_point = Point(sensor_location)

    # Verifica se o ponto do sensor está dentro do polígono
    if not polygon_shape.contains(sensor_point):
        return False

    # Cria um buffer circular ao redor do ponto do sensor com o alcance especificado
    project = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:4326'),  # transforma de latitude/longitude para um sistema de coordenadas projetadas
        pyproj.Proj('+proj=aea +lat_1=-10 +lat_2=-40 +lat_0=-25 +lon_0=-50 +x_0=0 +y_0=0 +ellps=aust_SA +units=m +no_defs'))
    sensor_buffer = transform(project, sensor_point.buffer(sensor_range))

    # Interseção entre o buffer do sensor e o polígono
    intersection = polygon_shape.intersection(sensor_buffer)

    # Verifica se a interseção é vazia ou se é igual ao buffer do sensor (ou seja, parte da sala está coberta)
    return not intersection.is_empty and intersection.equals(sensor_buffer)


def sel_heuristic(industry_id, rooms_list, apps_list, info_flows_list, ifr_flows_list):
    database_controller = DatabaseController()
    geo_mapping = {}

    industry_object = database_controller.get_entity(industry_id, "Building")
    industry_dict = json.loads(industry_object[2])
    industry = Building(industry_dict)

    rooms = []
    for r in rooms_list:
        room_object = database_controller.get_entity(r, 'Room')
        room_dict = json.loads(room_object[2])
        room = Room(room_dict)
        rooms.append(room)

    apps = []
    for r in apps_list:
        app_object = database_controller.get_entity(r, 'SoftwareApplication')
        app_dict = json.loads(app_object[2])
        app = SoftwareApplication(app_dict)
        apps.append(app)

    info_flows = []
    for r in info_flows_list:
        info_flow_object = database_controller.get_entity(r, 'Graph')
        info_flow_dict = json.loads(info_flow_object[2])
        info_flow = InformationFlow(info_flow_dict)
        info_flows.append(info_flow)

    ifr_flows = []
    for r in ifr_flows_list:
        ifr_flow_object = database_controller.get_entity(r, 'Graph')
        ifr_flow_dict = json.loads(ifr_flow_object[2])
        ifr_flow = InfrastructureFlow(ifr_flow_dict)
        ifr_flows.append(ifr_flow)

    for ifr_flow in ifr_flows:
        sensors = ifr_flow.get_sensors()
        candidate_locations = industry.candidateLocations

        for room in rooms:
            location = room.location
            for sensor in sensors:
                for candidate_location in candidate_locations:
                    if check_sensor_coverage(location, candidate_location, sensor["r_sen"]):

