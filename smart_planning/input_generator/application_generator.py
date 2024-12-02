import json


def generate_application(app_id, application_category, room_ids, memory_requirement, processor_requirement,
                         network_requirement):
    application_data = []
    for room_id in room_ids:
        application_id = f"application-{app_id}0{room_id}"

        app_data = {
            "id": application_id,
            "type": "SoftwareApplication",
            "deploymentRoom": f"room-0{room_id}",
            "applicationCategory": application_category,
            "memoryRequirements": memory_requirement,
            "processorRequirements": processor_requirement,
            "networkRequirements": network_requirement
        }

        app_filename = f"evaluation/{app_data['id']}.json"
        with open(app_filename, 'w') as app_file:
            json.dump(app_data, app_file, indent=2)

        application_data.append(app_data)

    return application_data


def generate_applications():
    application_data = []
    application_data.extend(generate_application('A', 'Failure detection by acoustic sensing', [1, 5],
                                                 16000, 6000, 128000))
    application_data.extend(generate_application('B', 'Emission detection by smoke sensing', [1, 5],
                                                 80, 20, 640))
    application_data.extend(generate_application('C', 'Ventilation efficiency by air quality sensing',
                                                 [1, 2, 4, 5], 1250000000, 1250000, 10000000))
    application_data.extend(generate_application('D', 'Detection of overheating by temperature sensing'
                                                 , [1, 5], 80, 20, 640))
    application_data.extend(generate_application('E', 'Lighting and refrigeration control by presence '
                                                      'sensing', [1, 2, 3, 4, 5], 240, 60, 1920))

    return application_data
