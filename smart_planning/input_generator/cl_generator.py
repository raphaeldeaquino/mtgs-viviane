from shapely.geometry import Polygon
from pyproj import Transformer


def generate_candidate_locations(rooms_list):
    candidate_locations_list = set()

    for room in rooms_list:
        coordinates = room.exterior.coords
        transformer = Transformer.from_crs("EPSG:4326", "EPSG:32722", always_xy=True)
        projected_coords = [transformer.transform(x, y) for x, y in coordinates]
        projected_polygon = Polygon(projected_coords)
        total_area = projected_polygon.area
        polygon = room
        # Garantir que é uma LineString para usar a borda
        boundary = polygon.exterior

        # Parâmetros
        if total_area <= 6:
            num_points = 1  # Número de pontos desejados
        else:
            num_points = round(total_area / 10)

        # Calcular o comprimento total da borda
        perimeter = boundary.length

        # Distância entre os pontos
        distance_between_points = perimeter / num_points

        # Gerar os pontos
        points = [boundary.interpolate(distance_between_points * i) for i in range(num_points)]

        # Exibir os pontos
        for i, point in enumerate(points, 1):
            candidate_locations_list.add((point.x, point.y))

    return list(candidate_locations_list)
