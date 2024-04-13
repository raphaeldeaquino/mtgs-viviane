from .Graph import *


class InfrastructureFlow:

    def __init__(self, flow_dict):
        try:
            if flow_dict["type"] != "Graph":
                raise ValueError("Invalid ifr flow dictionary: 'type' must be 'Graph'")

            if flow_dict["category"] != "Infrastructure Flow":
                raise ValueError("Invalid ifr flow dictionary: 'category' must be 'Infrastructure Flow'")

            self.id = flow_dict["id"]
            self.type = "Graph"
            self.category = "Infrastructure Flow"
            self.description = flow_dict["description"] if "description" in flow_dict else None
            self.label = flow_dict["label"] if "label" in flow_dict else None
            metadata = flow_dict["metadata"]
            self.deployment_room = metadata["deploymentRoom"]
            self.application = ["application"]
            self.information_flow = metadata["informationFlow"]
            self.precision_model = metadata["precisionModel"]
            self.flow_representation = Graph()
            self.flow_representation.add_nodes(flow_dict["nodes"])
            self.flow_representation.add_edges(flow_dict["edges"])
        except KeyError:
            raise ValueError("Invalid information flow dictionary")

    def get_sensors(self):
        nodes = self.flow_representation.get_nodes()
        sensors = []

        for node in nodes:
            if nodes[node]["role"] == "sensor":
                sensors.append({node: nodes[node]})

        return sensors

    def get_nodes(self):
        return self.flow_representation.get_nodes()

    def get_edges(self):
        return self.flow_representation.get_edges()
