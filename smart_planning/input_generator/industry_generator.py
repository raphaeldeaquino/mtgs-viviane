import os
import json


def generate_industry(coordinates, candidate_locations_list):
    if not os.path.exists('evaluation'):
        os.makedirs('evaluation')

    industry = {
        "id": "industry-01",
        "type": "Building",
        "category": [
            "industrial"
        ],
        "description": "Volga building",
        "floorsAboveGround": 1,
        "floorsBelowGround": 0,
        "openingHours": [
            "Mo-Fr 8:00-18:00",
            "Sa 8:00-12:00"
        ],
        "location": {
            "type": "Polygon",
            "coordinates": coordinates
        },
        "address": {
            "addressLocality": "Aparecida de Goiânia, Goiás, Brasil",
            "postalCode": "74993-535",
            "streetAddress": "Avenida Elmar Arantes Cabral, Quadra 01, Lote 05, s/n - Parque Industrial Vice-Presidente José de Alencar"
        },
        "candidateLocations": candidate_locations_list
    }

    industry_filename = f"evaluation/industry.json"

    with open(industry_filename, 'w') as industry_file:
        json.dump(industry, industry_file, indent=2)

    industry_file.close()
