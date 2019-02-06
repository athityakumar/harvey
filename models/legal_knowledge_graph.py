import networkx as nx


class LegalKnowledgeGraph(nx.DiGraph):
    def add_case(self, case):
        # TODO: Abstract case and add more metadata support w/ categories
        self.add_node(case.uuid, type='case')

    def fetch_subgraph(self, query_type='', query_nodes=set()):
        if (not query_type and not query_nodes):
            return(self)

        if not query_type:
            return(self.subgraph(query_nodes))

        subgraph_nodes = set(
                [node for (node, data) in self.nodes(data=True)
                    if data['type'] == query_type])

        if query_nodes:
            subgraph_nodes = subgraph_nodes.intersection(set(query_nodes))

        return(self.subgraph(list(subgraph_nodes)))

    def add_citation(self, from_case, to_case):
        self.add_case(from_case)
        self.add_case(to_case)
        self.add_edge(from_case.uuid, to_case.uuid)

    def in_degree_distribution(self, query_type='', query_nodes=set()):
        subgraph = self.fetch_subgraph(
            query_type=query_type, query_nodes=query_nodes)
        in_degree_tuples = self.in_degree()
        return(self.degree_distribution(in_degree_tuples))

    def out_degree_distribution(self, query_type='', query_nodes=set()):
        subgraph = self.fetch_subgraph(
            query_type=query_type, query_nodes=query_nodes)
        out_degree_tuples = self.out_degree()
        return(self.degree_distribution(out_degree_tuples))

    def degree_distribution(self, node_degree_tuple):
        distribution = dict()
        for (node, degree) in node_degree_tuple:
            if degree in distribution:
                distribution[degree] += 1
            else:
                distribution[degree] = 1
        return(sorted(distribution.items(), key=lambda k: k[0], reverse=True))

    def average_in_degree(self, query_type='', query_nodes=set()):
        subgraph = self.fetch_subgraph(
            query_type=query_type, query_nodes=query_nodes)
        in_degree_distribution = self.in_degree_distribution()
        return(self.average_degree(in_degree_distribution))

    def average_out_degree(self, query_type='', query_nodes=set()):
        subgraph = self.fetch_subgraph(
            query_type=query_type, query_nodes=query_nodes)
        out_degree_distribution = self.out_degree_distribution()
        return(self.average_degree(out_degree_distribution))

    def average_degree(self, distribution):
        return(
            sum([degree*count for (degree, count) in distribution])
            / self.number_of_cases())

    def number_of_cases(self):
        return(len(self.fetch_subgraph(query_type='case').nodes()))

    def number_of_citations(self):
        return(len(self.fetch_subgraph(query_type='case').edges()))
