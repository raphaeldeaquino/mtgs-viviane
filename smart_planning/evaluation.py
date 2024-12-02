import json
import os
import random
from shapely.geometry import Polygon, Point, LineString, box
from shapely.ops import split
import networkx as nx
from pyproj import Transformer
import numpy as np


# Área mínima para cada subpolígono
min_area = 50
max_attempts = 100  # Tentativas máximas para gerar divisões válidas


# Função para gerar uma linha de corte aleatória
def random_cut(polygon):
    minx, miny, maxx, maxy = polygon.bounds
    start_point = (random.uniform(minx, maxx), random.uniform(miny, maxy))
    end_point = (random.uniform(minx, maxx), random.uniform(miny, maxy))
    return LineString([start_point, end_point])


def generate_rooms(num_salas, total_area, industry_polygon):
    if not os.path.exists('evaluation'):
        os.makedirs('evaluation')

    # Dividir o polígono em subpolígonos
    sub_polygons = [industry_polygon]
    attempts = 0

    while len(sub_polygons) < num_salas and attempts < max_attempts:
        # Escolhe um polígono aleatório para dividir
        poly_to_split = []
        for poly in sub_polygons:
            transformer = Transformer.from_crs("EPSG:4326", "EPSG:32722", always_xy=True)
            projected_coords = [transformer.transform(x, y) for x, y in poly.exterior.coords]
            projected_polygon = Polygon(projected_coords)
            total_area = projected_polygon.area
            if total_area > min_area * 2:
                poly_to_split.append(poly)

        # Gera uma linha de corte aleatória
        cut_line = random_cut(poly_to_split[0])

        # Divide o polígono
        try:
            split_result = split(poly_to_split[0], cut_line)
            new_sub_polygons = []

            for poly in sub_polygons:
                if poly == poly_to_split[0]:
                    new_sub_polygons.extend(split_result.geoms)
                else:
                    new_sub_polygons.append(poly)

            # Valida se as áreas dos novos subpolígonos respeitam a área mínima
            transformer = Transformer.from_crs("EPSG:4326", "EPSG:32722", always_xy=True)
            projected_coords = [transformer.transform(x, y) for x, y in poly.exterior.coords]
            projected_polygon = Polygon(projected_coords)
            total_area = projected_polygon.area
            if all(total_area >= min_area for poly in new_sub_polygons):
                sub_polygons = new_sub_polygons
        except Exception as e:
            # Ignorar divisões inválidas
            pass

        attempts += 1

    # Certifique-se de ter exatamente o número desejado de subpolígonos
    if len(sub_polygons) > num_salas:
        sub_polygons = sub_polygons[:num_salas]

    # Resultados
    for i, sub_poly in enumerate(sub_polygons, 1):
        transformer = Transformer.from_crs("EPSG:4326", "EPSG:32722", always_xy=True)
        projected_coords = [transformer.transform(x, y) for x, y in sub_poly.exterior.coords]
        projected_polygon = Polygon(projected_coords)
        total_area = projected_polygon.area

    # Visualização (opcional)
    try:
        import matplotlib.pyplot as plt
        for poly in sub_polygons:
            x, y = poly.exterior.xy
            plt.plot(x, y)
        plt.title("Divisão do Polígono em Salas")
        plt.show()
    except ImportError:
        print("Matplotlib não está instalado para visualização.")

    # If not enough rooms could be placed
    if len(sub_polygons) < num_rooms:
        raise ValueError(f"Could only place {len(sub_polygons)} rooms out of {num_rooms} requested")

    areas = generate_area_layout(total_area)

    for room_id in range(1, len(sub_polygons) + 1):
        area_type = random.choice(list(areas.keys()))
        area_size = areas[area_type]

        floor_size = random.uniform(0.5 * area_size, area_size)
        if floor_size < 50:
            floor_size = 50  # Garantir um tamanho mínimo de 50m² para cada sala

        people_capacity = int(floor_size // 2)
        if people_capacity > 200:
            people_capacity = 200

        transformer = Transformer.from_crs("EPSG:4326", "EPSG:32722", always_xy=True)
        projected_coords = [transformer.transform(x, y) for x, y in sub_polygons[room_id - 1].exterior.coords]
        projected_polygon = Polygon(projected_coords)
        total_area = projected_polygon.area

        room_data = {
            "id": f"room-{room_id:02}",
            "type": "Room",
            "description": f"Main room in Volga industry {room_id}",
            "containedInBuilding": "volga",
            "floorLevel": 1,
            "floorSize": floor_size,
            "peopleCapacity": people_capacity,
            "peopleOccupancy": people_capacity // 2,  # Ocupação inicial como metade da capacidade
            "areaType": area_type,
            "location": {
                "type": "Polygon",
                "coordinates": generate_random_coordinates(sub_polygons[room_id -1])
            },
            "metadata": {
                "room_area": total_area,  # Área da sala
                "minimum_size": 50,
                "max_people_capacity": people_capacity,
                "current_occupancy": people_capacity // 2
            }
        }

        room_filename = f"evaluation/room-{room_id:02}.json"
        with open(room_filename, 'w') as room_file:
            json.dump(room_data, room_file, indent=2)

    return sub_polygons





# Função para gerar coordenadas aleatórias dentro de um polígono da indústria
def generate_random_point_within_polygon(polygon):
    min_x, min_y, max_x, max_y = polygon.bounds
    while True:
        random_point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        if polygon.contains(random_point):
            return random_point


# Função para gerar coordenadas do polígono para a sala
def generate_random_coordinates(industry_polygon):
    coordinates = []
    for _ in range(5):
        point = generate_random_point_within_polygon(industry_polygon)
        coordinates.append((point.x, point.y))
    return coordinates


# Função para gerar as salas com informações complementares
def generate_rooms0(num_rooms, total_area, industry_polygn):
    if not os.path.exists('evaluation'):
        os.makedirs('evaluation')

    areas = generate_area_layout(total_area)
    room_data_list = []

    for room_id in range(1, num_rooms + 1):
        area_type = random.choice(list(areas.keys()))
        area_size = areas[area_type]

        floor_size = random.uniform(0.5 * area_size, area_size)
        if floor_size < 50:
            floor_size = 50  # Garantir um tamanho mínimo de 50m² para cada sala

        people_capacity = int(floor_size // 2)
        if people_capacity > 200:
            people_capacity = 200

        room_data = {
            "id": f"room-{room_id:02}",
            "type": "Room",
            "description": f"Main room in Volga industry {room_id}",
            "containedInBuilding": "volga",
            "floorLevel": 1,
            "floorSize": floor_size,
            "peopleCapacity": people_capacity,
            "peopleOccupancy": people_capacity // 2,  # Ocupação inicial como metade da capacidade
            "areaType": area_type,
            "location": {
                "type": "Polygon",
                "coordinates": generate_random_coordinates(industry_polygn)
            },
            "metadata": {
                "room_area": area_size,  # Área da sala
                "minimum_size": 50,
                "max_people_capacity": people_capacity,
                "current_occupancy": people_capacity // 2
            }
        }

        room_filename = f"evaluation/room-{room_id:02}.json"
        with open(room_filename, 'w') as room_file:
            json.dump(room_data, room_file, indent=2)

        room_data_list.append(room_data)

    return room_data_list


def create_graph_infrastructure(num_sensors, num_devices, num_switches):
    G = nx.DiGraph()

    # Adicionar nós (sensores, dispositivos, switches)
    for i in range(num_sensors):
        G.add_node(f"Sensor {i + 1}", tipo="sensor")
    for i in range(num_devices):
        G.add_node(f"Device {i + 1}", tipo="computing")
    for i in range(num_switches):
        G.add_node(f"Switch {i + 1}", tipo="switch")

    # Conectar sensores aos dispositivos, dispositivos aos switches
    for sensor in range(num_sensors):
        for device in range(num_devices):
            G.add_edge(f"Sensor {sensor + 1}", f"Device {device + 1}")
    for device in range(num_devices):
        for switch in range(num_switches):
            G.add_edge(f"Device {device + 1}", f"Switch {switch + 1}")

    return G


# Função para criar gráfico de fluxo de informação (dados e middleware)
def create_graph_information(num_raw_data, num_middleware):
    G = nx.DiGraph()

    # Adicionar nós (dados brutos e middleware)
    for i in range(num_raw_data):
        G.add_node(f"Raw Data {i + 1}", tipo="data")
    G.add_node("Middleware", tipo="middleware")

    # Conectar dados ao middleware
    for i in range(num_raw_data):
        G.add_edge(f"Raw Data {i + 1}", "Middleware")

    return G


# Função para gerar as aplicações para cada sala
def generate_applications(num_rooms, num_applications_per_room):
    for room_id in range(1, num_rooms + 1):
        for app_id in range(1, num_applications_per_room + 1):
            category = random.choice(["Infrastructure Flow", "Information Flow"])
            app_id_str = f"{category.lower().replace(' ', '-')}-{room_id:02}-{app_id:02}"
            application_data = {
                "id": app_id_str,
                "type": "Graph",
                "category": category,
                "label": f"{category} for application {app_id_str}",
                "metadata": {
                    "deploymentRoom": f"room-{room_id:02}",
                    "application": f"application-{room_id:02}-{app_id:02}",
                    "category_description": "Infrastructure and Data Flow Management"
                }
            }

            # Gerar gráfico de infraestrutura ou fluxo de informação
            if category == "Infrastructure Flow":
                num_sensors = random.randint(1, 3)
                num_devices = random.randint(1, 2)
                num_switches = random.randint(1, 2)
                graph = create_graph_infrastructure(num_sensors, num_devices, num_switches)
                application_data["nodes"] = {node: {"metadata": dict(graph.nodes[node])} for node in graph.nodes}
                application_data["edges"] = [
                    {"source": edge[0], "target": edge[1], "metadata": {"weight": random.randint(10000, 50000)}} for
                    edge in graph.edges]
            else:
                num_raw_data = random.randint(1, 3)
                num_middleware = 1
                graph = create_graph_information(num_raw_data, num_middleware)
                application_data["nodes"] = {node: {"metadata": dict(graph.nodes[node])} for node in graph.nodes}
                application_data["edges"] = [
                    {"source": edge[0], "target": edge[1], "metadata": {"weight": random.randint(10000, 50000)}} for
                    edge in graph.edges]

            app_filename = f"evaluation/{app_id_str}.json"
            with open(app_filename, 'w') as app_file:
                json.dump(application_data, app_file, indent=2)





# Gerar salas e aplicações
num_rooms = 10
num_applications_per_room = 2
coordinates = [(-16.826091, -49.218526),
               (-16.827192, -49.218437),
               (-16.827243, -49.218947),
               (-16.827767, -49.218942),
               (-16.827798, -49.219392),
               (-16.826129, -49.219440),
               (-16.826091, -49.218526)]
industry_polygon = Polygon(coordinates)
# Reprojetar o polígono para um sistema métrico (ex.: UTM Zone 22S - EPSG:32722)
transformer = Transformer.from_crs("EPSG:4326", "EPSG:32722", always_xy=True)
projected_coords = [transformer.transform(x, y) for x, y in coordinates]
projected_polygon = Polygon(projected_coords)
total_area = projected_polygon.area
rooms = generate_rooms(num_rooms, total_area, industry_polygon)
#candidate_locations = generate_candidate_locations(rooms)
#generate_applications(num_rooms, num_applications_per_room)

print("Arquivos JSON de salas e aplicações gerados com sucesso!")
