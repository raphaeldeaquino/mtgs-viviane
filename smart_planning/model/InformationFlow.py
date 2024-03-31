from .Graph import *


class InformationFlow:

    def __init__(self, flow_dict):
        try:
            if flow_dict["type"] != "Graph":
                raise ValueError("Invalid info flow dictionary: 'type' must be 'Graph'")

            if flow_dict["category"] != "Information Flow":
                raise ValueError("Invalid info flow dictionary: 'category' must be 'Information Flow'")

            self.id = flow_dict["id"]
            self.type = "Graph"
            self.category = "Information Flow"
            self.description = flow_dict["description"] if "description" in flow_dict else None
            self.label = flow_dict["label"] if "label" in flow_dict else None

            self.flow_representation = Graph()
            self.flow_representation.add_nodes(flow_dict["nodes"])
            self.flow_representation.add_edges(flow_dict["edges"])
        except KeyError:
            raise ValueError("Invalid information flow dictionary")
