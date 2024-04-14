import itertools

from haversine import haversine, Unit

from .controller.DatabaseController import *
from .model.Room import *
from .model.SoftwareApplication import *
from .model.InformationFlow import *
from .model.InfrastructureFlow import *
from .model.Building import *


def points_in_range(sensor_lat, sensor_lon, range, points_of_interest):
    """
    Verifica quantos pontos de interesse estão dentro do alcance do sensor.

    :param sensor_lat: Latitude do sensor em graus decimais.
    :param sensor_lon: Longitude do sensor em graus decimais.
    :param range: Alcance do sensor em metros.
    :param points_of_interest: Lista de tuplas contendo (latitude, longitude) dos pontos de interesse.
    :return: Número de pontos de interesse dentro do alcance do sensor.
    """
    points_in_range = set()

    for point in points_of_interest:
        # Calcula a distância entre o sensor e o ponto de interesse em metros
        distance = haversine((sensor_lat, sensor_lon), point['location'], unit=Unit.METERS)

        # Verifica se o ponto está dentro do alcance do sensor
        if distance <= range:
            points_in_range.add((sensor_lat, sensor_lon))

    return points_in_range


def rm_heuristic(industry_id, rooms_list, apps_list, info_flows_list, ifr_flows_list, mifs, eff_weight, cov_weight):
    database_controller = DatabaseController()

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

    candidate_deployments = []
    values_to_combine = []

    for room in mifs:
        for app in mifs[room]:
            for mif in mifs[room][app]:
                mif['application'] = app
                values_to_combine.append(mif)

    for room in mifs:
        number_of_apps = len(mifs[room].keys())
        combinations = list(itertools.combinations(values_to_combine, number_of_apps))
        deployment_options = {}

        for combination in combinations:
            # Checa se são da mesma aplicação
            same_app = False
            for i in range(1, len(combination)):
                if combination[0]['application'] == combination[i]['application']:
                    same_app = True
                    break
            if len(combination) > 0 and not same_app:
                if combination[0]['application'] not in deployment_options:
                    deployment_options[combination[0]['application']] = []
                utility = 0.0
                cost = 0.0
                coverage = 0.0
                option = {'mifs': []}
                for value in combination:
                    option['mifs'].append(value)
                    for node in value['mif']:
                        cost += value['mif'][node]['deployCost']
                        cost += value['mif'][node]['operationalCost']
                    utility += value['utility']
                    coverage += value['coverage']
                option['cost'] = cost
                option['utility'] = utility
                option['coverage'] = coverage
                option['investmentEfficiency'] = utility / cost

                covered_locations = set()
                for value in combination:
                    for n in value['mif']:
                        location = value['mif'][n]['location']
                        r_tr = value['mif'][n]['r_tr']
                        points = points_in_range(location[0], location[1], r_tr, industry.candidateLocations)
                        covered_locations.update(points)
                option['coverageLocations'] = len(covered_locations)
                option['reusabilityIndex'] = eff_weight * option['investmentEfficiency'] + \
                                             cov_weight * option['coverageLocations']

                candidate_deployments.append(option)
    candidate_deployments = sorted(candidate_deployments, key=lambda x: x["reusabilityIndex"], reverse=True)
    print(candidate_deployments[0])
