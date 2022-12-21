import json     #Função de importação do JSON, o Python usa diretamente as funções JSON para escrever diretamente no arquivo Json
import os       #Função para interagir com o S.O. (criar, identificar, buscar e remover um diretório, etc.)

import jsonschema  #Implementação da especificação JSON Schema para Python
from jsonschema import validate #Um esquema de amostra, como o que obteríamos de json.load() >>> schema = { ... " type" : "object", ... " properties" : { ... " preço" : {"tipo" : "número"}, ... "

from django.http import JsonResponse
#django usa objetos de solicitação de resposta para passar o estado pelo sistema
#JsonResponse cria respostas JSON
#Em um HttpRequestobjeto, os atributos GETe POSTsão instâncias de django.http.QueryDict,
# uma classe semelhante a um dicionário personalizada para lidar com vários valores para a mesma chave.
# Isso é necessário porque alguns elementos de formulário HTML, principalmente, passam vários valores para a mesma chave.<select multiple>
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

def get_schema(json_data):
    """This function loads the given schema available"""
    type = json_data["type"]
    current_path = os.path.dirname(__file__)
    parent_path = os.path.abspath(os.path.join(current_path, os.pardir))
    schema_file = parent_path + '/models/'+type+'/schema.json'
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
        print(err)
        err = "Given JSON data is InValid"
        return False, 
    # err
    message = "Given JSON data is Valid"
    return True, message


def entities(request):
    if request.method == "POST":
        entity: object = json.loads(request.body)
        entity_type = entity['type']
        result = validate_json(entity)
    return JsonResponse({"result": result})


def get_entity(request, id):
    return None