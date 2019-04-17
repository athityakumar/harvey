import networkx as nx

from models.case import Case
from models.legal_knowledge_graph import LegalKnowledgeGraph
from helpers import *
from custom import *

G = init_graph("{}/all_citations.txt".format(DATADIR)).fetch_subgraph(
        query_type='case')

print(len(G.nodes()))
print(len(G.edges()))
print(G.in_degree_distribution())
print(G.out_degree_distribution())
print('Average clustering coeff', nx.average_clustering(G))
print('Average in_degree', G.average_in_degree())
print('Average out_degree', G.average_out_degree())

# print_landmark_cases(nx.in_degree_centrality, G, 'In-Degree centrality')
# print_landmark_cases(nx.eigenvector_centrality, G, 'Eigen-vector centrality')
# print_landmark_cases(nx.katz_centrality, G, 'Katz centrality')
# print_landmark_cases(nx.closeness_centrality, G, 'Closeness centrality')
# print_landmark_cases(nx.pagerank, G, 'Pagerank')
# print_landmark_cases(custom_centrality, G, 'Custom centrality')
# print_common_cases()

# plot_distribution(fetch_log_scale(G.in_degree_distribution()), 'In-Degree', 'graph_plots/power_law_distribution/in_degree.png', fontSize=2, dpi=500, plot_type="scatter")
# plot_distribution(fetch_log_scale(G.out_degree_distribution()), 'Out-Degree', 'graph_plots/power_law_distribution/out_degree.png', fontSize=2, dpi=500, plot_type="scatter")

# unfrozen_graph = nx.Graph(G)
# unfrozen_graph.remove_edges_from(unfrozen_graph.selfloop_edges())

# core_number = nx.core_number(unfrozen_graph)
# core_number_sorted = sorted(core_number.items(), key=lambda kv: kv[1], reverse=True)[:50]
# for case_id, value in core_number_sorted:
#     print(case_id, "\t", CASE_ID_TO_NAME_MAPPING[case_id], "\t", value)
# print("k_core")
# k_core = nx.k_core(unfrozen_graph)
# # k_core_sorted = sorted(k_core.items(), key=lambda kv: kv[1], reverse=True)[:50]
# for _ in k_core.nodes():
#     print(_, "\t", CASE_ID_TO_NAME_MAPPING[_])
# print("k_shell")
# k_shell = nx.k_shell(unfrozen_graph)
# for _ in k_shell.nodes():
#     print(_, "\t", CASE_ID_TO_NAME_MAPPING[_])
# print("k_crust")
# k_crust = nx.k_crust(unfrozen_graph)
# for _ in k_crust.nodes():
#     print(_, "\t", CASE_ID_TO_NAME_MAPPING[_])
# print("k_corona")
# k_corona = nx.k_corona(unfrozen_graph, k=10)
# for _ in k_corona.nodes():
#     print(_, "\t", CASE_ID_TO_NAME_MAPPING[_])

# rich_club_coefficient = nx.rich_club_coefficient(unfrozen_graph, normalized=False)
# rich_club_sorted = sorted(rich_club_coefficient.items(), key=lambda kv: kv[1], reverse=True)
# min_degree = 116
# rich_club = list()

# for case_id in unfrozen_graph:
# 	if len(unfrozen_graph[case_id]) > min_degree:
# 		rich_club.append(case_id)
# print([CASE_ID_TO_NAME_MAPPING[case_id] for case_id in rich_club])

# k_clique_communities = list(nx.algorithms.community.k_clique_communities(unfrozen_graph, k=8))
# # print(k_clique_communities)

# for k_clique in k_clique_communities:
# 	print("\n")
# 	for case_id in k_clique:
# 		if case_id in CASE_ID_TO_FILE_MAPPING:
# 			path = CASE_ID_TO_FILE_MAPPING[case_id]
# 			subjects = find_subjects_for_case(path)
# 			print(case_id,"\t", CASE_ID_TO_NAME_MAPPING[case_id],"\t", ", ".join(subjects))
