import networkx as nx
from models.case import Case
from models.legal_knowledge_graph import LegalKnowledgeGraph
from helpers import *

G = init_graph('case-case-citation.txt')

print(len(G.nodes()))
print(len(G.edges()))
print(G.in_degree_distribution())
print(G.out_degree_distribution())

print("Average clustering coeff", nx.average_clustering(G.fetch_subgraph(query_type='case')))

import collections
import matplotlib.pyplot as plt
import networkx as nx

print("Average in_degree", G.average_in_degree())
print("Average out_degree", G.average_out_degree())

plot_distribution(G.in_degree_distribution(), "In-Degree")
plot_distribution(G.out_degree_distribution(), "Out-Degree")
