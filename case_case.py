import networkx as nx

from models.case import Case
from models.legal_knowledge_graph import LegalKnowledgeGraph
from helpers import *
from custom import *

G = init_graph("{}/case-case-citation.txt".format(DATADIR)).fetch_subgraph(
        query_type='case')

print(len(G.nodes()))
print(len(G.edges()))
print(G.in_degree_distribution())
print(G.out_degree_distribution())
print("Average clustering coeff", nx.average_clustering(G))
print("Average in_degree", G.average_in_degree())
print("Average out_degree", G.average_out_degree())

print_landmark_cases(nx.in_degree_centrality, G, "In-Degree centrality")
print_landmark_cases(nx.eigenvector_centrality, G, "Eigen-vector centrality")
print_landmark_cases(nx.katz_centrality, G, "Katz centrality")
print_landmark_cases(nx.closeness_centrality, G, "Closeness centrality")
print_landmark_cases(nx.pagerank, G, "Pagerank")
print_landmark_cases(custom_centrality, G, "Custom centrality")

# plot_distribution(G.in_degree_distribution(), "In-Degree")
# plot_distribution(G.out_degree_distribution(), "Out-Degree")
