import json
import random
from random import randrange


def generate_ifr_flows(quantity, info_flow_data):
    id_count = 1
    ifr_flows_data = []

    for info_flow_data in info_flow_data:
        info_number = info_flow_data['id'].split('-')[2]

        for i in range(quantity):
            flow_id = f"ifr-flow-{id_count:04d}"
            flow_data = {
                "id": flow_id,
                "type": "Graph",
                "category": "Infrastructure Flow",
                "label": f"Infrastructure flow for {info_flow_data['id']}",
                "metadata": {
                    "deploymentRoom": info_flow_data['metadata']['deploymentRoom'],
                    "application": info_flow_data['metadata']['application'],
                    "informationFlow": info_flow_data['id'],
                    "precisionModel": random.uniform(0.6262, 1)
                },
                "nodes": {},
                "edges": []
            }

            nodes = {}

            room_number = info_flow_data['metadata']['deploymentRoom'].split('-')[1]
            app_number = info_flow_data['id'].split('-')[2]
            if 'A' or 'D' in info_flow_data['metadata']['application']:
                r_tr = 300
                deploymentCost = 790.96
                operationalCost = 18.16
            elif 'B' in info_flow_data['metadata']['application']:
                r_tr = 600
                deploymentCost = 735
                operationalCost = 5.51
            elif 'C' in info_flow_data['metadata']['application']:
                r_tr = 15
                deploymentCost = 1399
                operationalCost = 12.02
            elif 'E' in info_flow_data['metadata']['application']:
                r_tr = 10
                deploymentCost = 360
                operationalCost = 8.38

            nodes_id_count = 1

            for ii, info_node in enumerate(info_flow_data['nodes']):
                if ii == len(info_flow_data['nodes']) - 1:
                    break
                node_id = f"ifr{room_number}-{app_number}-{info_number}-{nodes_id_count:04d}"
                nodes[node_id] = {
                    "metadata": {
                        "weight": info_flow_data['nodes'][info_node]['metadata']['weight'],
                        "role": "sensor",
                        "r_tr": r_tr,
                        "r_sen": r_tr,
                        'deploymentCost': deploymentCost,
                        "operationalCost": operationalCost
                    }
                }

                nodes_id_count = nodes_id_count + 1

            for j in range(i + 1):
                node_id = f"ifr{room_number}-{app_number}-{info_number}-{nodes_id_count:04d}"
                protocol_type = randrange(2)
                if protocol_type == 0:
                    weight = 1562500
                    edge_weight = 100000000
                    r_tr = 50
                    deploymentCost = 272.11
                    operationalCost = 9.25
                else:
                    weight = 781.25
                    edge_weight = 50000
                    r_tr = 1000
                    deploymentCost = 728.7
                    operationalCost = 23.11
                nodes[node_id] = {
                    "metadata": {
                        "weight": weight,
                        'edge_weight': edge_weight,
                        "role": "network",
                        "r_tr": r_tr,
                        "r_sen": r_tr,
                        'deploymentCost': deploymentCost,
                        "operationalCost": operationalCost
                    }
                }

                nodes_id_count = nodes_id_count + 1

            node_id = f"ifr{room_number}-{app_number}-{info_number}-{nodes_id_count:04d}"
            nodes[node_id] = {
                "metadata": {
                    "weight": 6800000000,
                    "role": "compute",
                    "r_tr": 50,
                    'deploymentCost': 433.53,
                    "operationalCost": 77.28
                }
            }

            flow_data['nodes'] = nodes

            edges = []

            for j in range(nodes_id_count - 1):
                source_node_id = f"ifr{room_number}-{app_number}-{info_number}-{j + 1:04d}"
                target_node_id = f"ifr{room_number}-{app_number}-{info_number}-{j + 2:04d}"
                role = nodes[source_node_id]['metadata']['role']
                if role == 'sensor':
                    weight = info_flow_data['edges'][0]['metadata']['weight']
                elif role == 'network':
                    weight = nodes[source_node_id]['metadata']['edge_weight']
                    del nodes[source_node_id]['metadata']['edge_weight']
                edges.append(
                    {
                        "source": source_node_id,
                        "target": target_node_id,
                        "metadata": {
                            "weight": weight
                        }
                    },
                )

            flow_data['edges'] = edges

            flow_filename = f"evaluation/{flow_id}.json"
            with open(flow_filename, 'w') as flow_file:
                json.dump(flow_data, flow_file, indent=2)

            id_count = id_count + 1
            ifr_flows_data.append((info_flow_data, flow_data))

    return flow_data
