import networkx as nx
from itertools import groupby

from models.case import Case
from models.legal_knowledge_graph import LegalKnowledgeGraph
from helpers import *
from custom import *

def compute_case_name_to_year_mapping(filename):
    with open(filename) as f:
    for line in f.readlines():
        path, case_name = line.rstrip().split("-->")
        year = path.split('/')[-2]
        CASE_NAME_TO_YEAR_MAPPING[case_name] = year

G = init_graph("{}/all_citations.txt".format(DATADIR)).fetch_subgraph(
        query_type='case')
compute_case_name_to_year_mapping('datafiles/all_indexes.txt')

TOP_CASES = []
yearwise_distribution = dict()

for top_case in TOP_CASES:
    yearwise_distribution[top_case] = dict()
    for year in range(1953, 2019):
        yearwise_distribution[top_case][year] = 0

for top_case in TOP_CASES:
    citing_case_ids = [edge[0] for edge in G.in_edges(top_case)]
    citing_case_names = [CASE_ID_TO_NAME_MAPPING[case_id] for case_id in citing_case_ids]
    year_of_citing_cases = [CASE_NAME_TO_YEAR_MAPPING[case_name] for case_name in citing_case_names]
    for year in year_of_citing_cases:
        yearwise_distribution[top_case][year] += 1

# Cumulative distribution
for top_case in TOP_CASES:
    for year in range(1954, 2019):
        prev_year = str(int(year)-1)
        yearwise_distribution[top_case][year] += yearwise_distribution[top_case][prev_year]
