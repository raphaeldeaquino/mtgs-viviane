def is_valid_polygon(coordinates):
    # Um polígono GeoJSON deve ser uma lista de anéis, onde cada anel é uma lista de coordenadas.
    if not isinstance(coordinates, list) or len(coordinates) < 4:
        return False

    # O primeiro e o último ponto devem ser iguais (um polígono fechado).
    if coordinates[0] != coordinates[-1]:
        return False

    # Verificando se cada coordenada é uma lista de pontos [x, y].
    for point in coordinates:
        if not isinstance(point, list) or len(point) != 2:
            return False

    return True


class GeoJSONPolygon:

    def __init__(self, coordinates):
        self.type = "Polygon"
        if is_valid_polygon(coordinates):
            self.coordinates = coordinates
        else:
            raise ValueError("Coordenadas do polígono inválidas.")

    def to_geojson(self):
        return {
            "type": self.type,
            "coordinates": self.coordinates
        }

    def __str__(self):
        coordinates_str = ", ".join([str(coord) for coord in self.coordinates])
        return f"GeoJSONPolygon(type={self.type}, coordinates=[{coordinates_str}])"
