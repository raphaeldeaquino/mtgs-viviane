import warnings
import itertools
import math
from shapely.ops import transform
from functools import partial
from geopy.distance import geodesic
import pyproj

from .controller.DatabaseController import *
from .model.Room import *
from .model.SoftwareApplication import *
from .model.InformationFlow import *
from .model.InfrastructureFlow import *
from .model.Building import *

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)


def check_sensor_coverage(polygon, sensor_location, sensor_range):
    # Converte as coordenadas do polígono em uma forma geométrica Shapely
    polygon_shape = Polygon(polygon.coordinates)

    # Converte as coordenadas do sensor para um objeto Point Shapely
    sensor_point = Point(sensor_location)

    # Verifica se o ponto do sensor está dentro do polígono
    if polygon_shape.contains(sensor_point):
        return True

    # Cria um buffer circular ao redor do ponto do sensor com o alcance especificado
    project = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:4326'),  # transforma de latitude/longitude para um sistema de coordenadas projetadas
        pyproj.Proj(
            '+proj=aea +lat_1=-10 +lat_2=-40 +lat_0=-25 +lon_0=-50 +x_0=0 +y_0=0 +ellps=aust_SA +units=m +no_defs'))
    sensor_buffer = transform(project, sensor_point.buffer(sensor_range))

    try:
        # Interseção entre o buffer do sensor e o polígono
        intersection = polygon_shape.intersection(sensor_buffer)

        # Verifica se a interseção é válida e não vazia
        return intersection.is_valid and not intersection.is_empty
    except Exception as e:
        logger.error("Error during  intersection:", e)
        return False


def check_inner(polygon, location):
    # Converte as coordenadas do polígono em uma forma geométrica Shapely
    polygon_shape = Polygon(polygon.coordinates)

    # Converte as coordenadas para um objeto Point Shapely
    point = Point(location)

    # Verifica se o ponto está dentro do polígono
    return polygon_shape.contains(point)


def coverage_area(infra):
    area_in_meters = math.pi * math.pow(infra['range'], 2)

    return area_in_meters


# Função para calcular a área de sobreposição entre duas áreas de cobertura
def overlapping_area(infra1, infra2):
    circle1 = Point((infra1['lat'], infra1['lon'])).buffer(infra1['range'])
    circle2 = Point((infra2['lat'], infra2['lon'])).buffer(infra2['range'])

    return circle1.intersection(circle2).area


def check_communication_coverage(infra_tr, mifs):
    adapted_mifs = []
    for mif in mifs:
        total_area = 0

        brokers = [{k: mif['mif'][k]} for k in mif['mif']]

        for i, infra1 in enumerate(brokers):
            infra_location = list(infra1.values())[0]['location']

            broker1 = {'lat': infra_location[0],
                       'lon': infra_location[1],
                       'range': infra_tr[list(infra1.keys())[0]]}
            total_area += coverage_area(broker1)

            for infra2 in brokers[i + 1:]:
                infra_location = list(infra2.values())[0]['location']

                broker2 = {'lat': infra_location[0],
                           'lon': infra_location[1],
                           'range': infra_tr[list(infra2.keys())[0]]}
                total_area += coverage_area(broker2)
                total_area -= overlapping_area(broker1, broker2)

        adapted_mifs.append({'mif': mif['mif'], 'utility': mif['utility'], 'coverage': total_area})

    return adapted_mifs


def sel_heuristic(industry_id, rooms_list, apps_list, info_flows_list, ifr_flows_list, service_utility_pruning,
                  communication_coverage_pruning):
    database_controller = DatabaseController()
    geo_mapping = {}
    mifs = {}
    nodes_role = {}
    nodes_r_tr = {}
    nodes_r_sen = {}
    nodes_op_cost = {}
    deployed_nodes = []

    industry_object = database_controller.get_entity(industry_id, "Building")
    industry_dict = json.loads(industry_object[2])
    industry = Building(industry_dict)

    rooms = []
    room_by_id = {}
    for r in rooms_list:
        room_object = database_controller.get_entity(r, 'Room')
        room_dict = json.loads(room_object[2])
        room = Room(room_dict)
        room_by_id[r] = room
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
    ifr_flow_by_id = {}
    for r in ifr_flows_list:
        ifr_flow_object = database_controller.get_entity(r, 'Graph')
        ifr_flow_dict = json.loads(ifr_flow_object[2])
        ifr_flow = InfrastructureFlow(ifr_flow_dict)
        ifr_flow_by_id[r] = ifr_flow
        ifr_flows.append(ifr_flow)

    candidate_locations = industry.candidateLocations

    # Verifica todas as localizações válidas para cada infraestrutura inicial
    for room in rooms:
        geo_mapping[room.id] = {}
        location = room.location

        for ifr_flow in ifr_flows:
            if ifr_flow.deployment_room == room.id:
                geo_mapping[room.id][ifr_flow.id] = {}
                nodes = ifr_flow.get_nodes()

                for node in nodes:
                    for candidate_location in candidate_locations:
                        if check_inner(location, candidate_location['location']) or \
                                (nodes[node]['role'] == 'sensor' and
                                 check_sensor_coverage(location,
                                                       candidate_location['location'],
                                                       nodes[node]['r_sen'])):
                            if node not in geo_mapping[room.id][ifr_flow.id]:
                                geo_mapping[room.id][ifr_flow.id][node] = []
                            geo_mapping[room.id][ifr_flow.id][node].append(candidate_location)

    # Gera os FIMs
    for room in rooms:
        mifs[room.id] = {}
        location = room.location
        polygon_shape = Polygon(location.coordinates)
        x, y = polygon_shape.centroid.xy
        centroid_location = [x[0], y[0]]

        for ifr_flow in ifr_flows:
            if ifr_flow.deployment_room == room.id:
                ifr_flow_nodes = ifr_flow.get_nodes()
                ifr_flow_sensors = ifr_flow.get_sensors()
                ifr_flow_edges = ifr_flow.get_edges()

                for node in ifr_flow_nodes:
                    nodes_role[node] = ifr_flow_nodes[node]['role']
                    nodes_op_cost[node] = ifr_flow_nodes[node]['operationalCost']
                    nodes_r_tr[node] = ifr_flow_nodes[node]['r_tr']
                    nodes_r_sen[node] = ifr_flow_nodes[node]['r_sen'] if 'r_sen' in ifr_flow_nodes[node] else None
                    if 'location' in ifr_flow_nodes[node]:
                        deployed_nodes.append(node)

                keys = list(geo_mapping[room.id][ifr_flow.id].keys())
                values_lists = list(geo_mapping[room.id][ifr_flow.id].values())
                combinations = list(itertools.product(*values_lists))
                result = []
                for combo in combinations:
                    result_dict = {keys[i]: combo[i] for i in range(len(keys))}
                    result_dict2 = {}
                    for node in result_dict:
                        if node in deployed_nodes:
                            deploy_cost = 0.0
                        else:
                            deploy_cost = result_dict[node]['deployCost'][nodes_role[node]]
                        result_dict2[node] = {'deployCost': deploy_cost,
                                              'operationalCost': nodes_op_cost[node],
                                              'r_tr': nodes_r_tr[node],
                                              'r_sen': nodes_r_sen[node],
                                              'location': result_dict[node]['location']}
                    result.append(result_dict2)

                mifs[room.id][ifr_flow.application] = []
                for mif in result:
                    connected = True
                    for edge in ifr_flow_edges:
                        source = edge['source']
                        target = edge['target']
                        source_location = mif[source]['location']
                        target_location = mif[target]['location']
                        source_r_tr = ifr_flow_nodes[source]['r_tr']
                        target_r_tr = ifr_flow_nodes[target]['r_tr']
                        distance = geodesic(source_location, target_location).meters
                        if distance > min(source_r_tr, target_r_tr):
                            connected = False
                            break
                    if not connected:
                        mifs[room.id][ifr_flow.application].append({'mif': mif, 'utility': 0})
                    else:
                        covered = True
                        for sensor in ifr_flow_sensors:
                            sensor_location = mif[list(sensor.keys())[0]]['location']
                            r_sen = list(sensor.values())[0]['r_sen']
                            distance = geodesic(centroid_location, sensor_location).meters
                            if distance > r_sen:
                                covered = False
                                break
                        if not covered:
                            mifs[room.id][ifr_flow.application].append({'mif': mif, 'utility': 0})
                        else:
                            detection_prob = 0.0
                            for sensor in ifr_flow_sensors:
                                sensor_location = mif[list(sensor.keys())[0]]['location']
                                distance = geodesic(centroid_location, sensor_location).meters
                                detection_prob = detection_prob + math.pow(math.e, -1 * distance)
                            detection_prob = detection_prob / len(ifr_flow_sensors)
                            utility = ifr_flow.precision_model * detection_prob
                            mifs[room.id][ifr_flow.application].append({'mif': mif, 'utility': utility})

    pruned_mifs = {}
    for room in mifs:
        pruned_mifs[room] = {}
        for app in mifs[room]:
            # Ordena para pegar somente os melhores
            flow_mifs = sorted(mifs[room][app], key=lambda x: x['utility'], reverse=True)

            # Remove os mifs com utility 0
            flow_mifs = [item for item in flow_mifs if item['utility'] > 0]

            # Faz a poda para pegar os M melhores. Checa o mínimo porque pode ter restado menos que M
            flow_mifs = flow_mifs[:min(service_utility_pruning, len(flow_mifs))]

            # Para cada mif determina a área de cobertura
            flow_mifs = check_communication_coverage(nodes_r_tr, flow_mifs)

            # Ordena para pegar somente os melhores
            flow_mifs = sorted(flow_mifs, key=lambda x: x['coverage'], reverse=True)

            # Faz a poda para pegar os M melhores. Checa o mínimo porque pode ter restado menos que N
            flow_mifs = flow_mifs[:min(communication_coverage_pruning, len(flow_mifs))]

            pruned_mifs[room][app] = flow_mifs

    return pruned_mifs
