import os  # Função para interagir com o S.O. (criar, identificar, buscar e remover um diretório, etc.)

from django.http import JsonResponse
# django usa objetos de solicitação de resposta para passar o estado pelo sistema JsonResponse cria respostas JSON Em
# um HttpRequestobjeto, os atributos GETe POSTsão instâncias de django.http.QueryDict, uma classe semelhante a um
# dicionário personalizada para lidar com vários valores para a mesma chave. Isso é necessário porque alguns
# elementos de formulário HTML, principalmente, passam vários valores para a mesma chave.<select multiple>
from django.views.decorators.csrf import csrf_exempt
from jsonschema import \
    validate  # Um esquema de amostra, como o que obteríamos de json.load() >>> schema = { ... " type" : "object",
# ... " properties" : { ... " preço" : {"tipo" : "número"}, ... "
import sys, traceback
from .controller.DatabaseController import *

@csrf_exempt
def get_schema(json_data):
    """This function loads the given schema available"""
    entity_type = json_data["type"]
    current_path = os.path.dirname(__file__)
    schema_file = current_path + '/dataModel/' + entity_type + '/schema.json'
    with open(schema_file, 'r') as file:
        schema = json.load(file)
    return schema


def validate_json(json_data):
    """REF: https://json-schema.org/ """
    # Describe what kind of json you expect.
    execute_api_schema = get_schema(json_data)

    try:
        validate(instance=json_data, schema=execute_api_schema)
    except Exception as err:
        logger.error(err)
        err = "Given JSON data is Invalid"
        return False, err
    message = "Given JSON data is Valid"
    return True, message


def entities(request):
    if request.method == "POST":
        entity: object = json.loads(request.body)
        result = validate_json(entity)
        if result[0]:
            entity_id = entity['id']
            try:
                database_controller = DatabaseController()
                return_value = database_controller.save_entity(entity)
                message = f"Entity {entity_id} saved" if return_value else f"Entity {entity_id} already saved"
            except Exception as e:
                logger.error(e)
                return_value = False
                message = f"{e}"
            finally:
                database_controller.close_connection()
        else:
            logger.error('Invalid entity json input')
            return_value = False
            message = result[1]

    return JsonResponse({"success": return_value, "message": message})


def get_entity(request, id):
    return None
