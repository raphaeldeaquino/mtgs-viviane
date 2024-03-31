from collections import defaultdict


class Graph(object):
    """ Graph data structure,directed. """

    def __init__(self):
        self._node_metadata = defaultdict(set)
        self._edge_metadata = defaultdict(set)
        self._connections = defaultdict(set)

    def add_nodes(self, nodes):
        for node in nodes:
            self._node_metadata[node] = nodes[node]["metadata"]

    def get_nodes(self):
        return self._node_metadata

    def add_edges(self, edges):
        for edge in edges:
            source = edge["source"]
            target = edge["target"]
            self.add_connection(source, target)
            self._edge_metadata[(source, target)] = edge["metadata"]

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """

        for node1, node2 in connections:
            self.add_connection(node1, node2)

    def add_connection(self, node1, node2):
        """ Add connection between node1 and node2 """

        self._connections[node1].add(node2)

    def remove(self, node):
        """ Remove all references to node """

        for n, cxns in self._connections.items():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._connections[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        """ Is node1 directly connected to node2 """

        return node1 in self._connections and node2 in self._connections[node1]

    def find_path(self, node1, node2, path=[]):
        """ Find any path between node1 and node2 (may not be shortest) """

        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self._connections:
            return None
        for node in self._connections[node1]:
            if node not in path:
                new_path = self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._connections))