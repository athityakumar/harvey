import networkx as nx

class LegalKnowledgeGraph(nx.DiGraph):
    def add_case(case):
        # TODO: Abstract case and add more metadata support w/ categories
        self.add_node(case.uuid, type='case')

    def fetch_subgraph(self, query_type='', query_nodes=set()):
        return(self) if (not query_type and not query_nodes)
        return(self.subgraph(query_nodes)) if not query_type

        subgraph_nodes = set([node for (node, data) in self.nodes(data=True) if data['type'] == query_type])

        if query_nodes:
            subgraph_nodes = subgraph_nodes.intersection(set(query_nodes))

        return(self.subgraph(list(subgraph_nodes)))

    def add_citation(self, from_case, to_case):
        self.add_case(from_case)
        self.add_case(to_case)
        self.add_edge(from_case.uuid, to_case.uuid)
