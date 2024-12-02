import json


def generate_info_flows(quantity, application_data):
    id_count = 1
    info_flows_data = []

    for app_data in application_data:
        for i in range(quantity):
            flow_id = f"info-flow-{id_count:04d}"
            flow_data = {
                "id": flow_id,
                "type": "Graph",
                "category": "Information Flow",
                "label": f"Information flow for {app_data['id']}",
                "metadata": {
                    "deploymentRoom": app_data['deploymentRoom'],
                    "application": app_data['id']
                },
                "nodes": {},
                "edges": []
            }

            nodes = {}

            room_number = app_data['deploymentRoom'].split('-')[1]
            app_number = app_data['id'].split('-')[1]

            for j in range(i + 1):
                node_id = f"info{room_number}-{app_number}-{j + 1:04d}"
                nodes[node_id] = {
                    'metadata': {
                        'weight': app_data['processorRequirements'],
                        "role": "application_data"
                    }
                }

            node_id = f"info{room_number}-{app_number}-{i + 2:04d}"
            nodes[node_id] = {
                'metadata': {
                    'weight': 6800000000,
                    "role": "application_data"
                }
            }

            flow_data['nodes'] = nodes

            edges = []

            for j in range(i + 1):
                source_node_id = f"info{room_number}-{app_number}-{j + 1:04d}"
                target_node_id = f"info{room_number}-{app_number}-{i + 1:04d}"
                edges.append(
                    {
                        "source": source_node_id,
                        "target": target_node_id,
                        "metadata": {
                            "weight": app_data['networkRequirements']
                        }
                    },
                )

            flow_data['edges'] = edges

            flow_filename = f"evaluation/{flow_id}.json"
            with open(flow_filename, 'w') as flow_file:
                json.dump(flow_data, flow_file, indent=2)

            id_count = id_count + 1
            info_flows_data.append(flow_data)

    return info_flows_data
