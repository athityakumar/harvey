import networkx as nx

from models.case import Case
from models.legal_knowledge_graph import LegalKnowledgeGraph
from helpers import *

G = init_graph('datafiles/case-case-citation.txt').fetch_subgraph(
        query_type='case')

print(len(G.nodes()))
print(len(G.edges()))
print(G.in_degree_distribution())
print(G.out_degree_distribution())
print("Average clustering coeff", nx.average_clustering(G))
print("Average in_degree", G.average_in_degree())
print("Average out_degree", G.average_out_degree())
degree_centrality = list(nx.degree_centrality(G))[:10]

for d in degree_centrality:
    print(d)
    print(G.in_degree(d), G.out_degree(d))

plot_distribution(G.in_degree_distribution(), "In-Degree")
plot_distribution(G.out_degree_distribution(), "Out-Degree")
