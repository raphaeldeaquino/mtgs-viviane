import json
import os

import jsonschema
from jsonschema import validate

from django.http import JsonResponse


def get_schema():
    """This function loads the given schema available"""
    current_path = os.path.dirname(__file__)
    parent_path = os.path.abspath(os.path.join(current_path, os.pardir))
    schema_file = parent_path + '/dataModel/Building/schema.json'
    with open(schema_file, 'r') as file:
        schema = json.load(file)
    return schema


def validate_json(json_data):
    """REF: https://json-schema.org/ """
    # Describe what kind of json you expect.
    execute_api_schema = get_schema()

    try:
        validate(instance=json_data, schema=execute_api_schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        err = "Given JSON data is InValid"
        return False, err

    message = "Given JSON data is Valid"
    return True, message


def entities(request):
    if request.method == "POST":
        entity = json.loads(request.body)
        entity_type = entity['type']
        result = validate_json(entity)
    return JsonResponse({"result": result})


def get_entity(request, id):
    return None