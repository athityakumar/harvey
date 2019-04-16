import os
import networkx as nx
from bs4 import BeautifulSoup

from models.case import Case
from models.legal_knowledge_graph import LegalKnowledgeGraph
from helpers import *
from custom import *

# G = init_graph("{}/all_citations.txt".format(DATADIR)).fetch_subgraph(
#         query_type='case')

directory = "CaseAnalysis"
os.chdir(DATADIR + '/' + directory)

folders = [name for name in os.listdir() if not name.startswith(".")]
unique_acts = dict()
i = 0
for folder in folders:
    year = folder
    os.chdir(folder)
    files = list(os.listdir())
    for file in files:
        with open(file) as html_file:
            soup = BeautifulSoup(html_file, 'lxml')
        if i%1000 == 0:
            print(i)
        i += 1
        # print(file)
        for elem in soup.find_all(id="legiscited"):
            act_names = [act_div.get_text() for act_div in elem.parent.find_all("p")]
            # print(act_names)
            for act in act_names:
                act = act.strip()
                if act in unique_acts:
                    unique_acts[act][year] += 1
                else:
                    unique_acts[act] = dict()
                    for y in range(1953, 2019):
                        y = str(y)
                        unique_acts[act][y] = 0
                    unique_acts[act][year] = 1

    os.chdir('..')

ACTS = [act for act in unique_acts]
print(len(ACTS))

acts_frequency = dict()
for act in unique_acts:
    year_dist = unique_acts[act]
    acts_frequency[act] = 0
    for year in year_dist:
        val = year_dist[year]
        acts_frequency[act] += val

def dict_sort(centrality_results, n=5):
    centrality_results = sorted(list(centrality_results.items()), key= lambda k: k[1], reverse=True)[:n]
    centrality_results = dict(centrality_results)
    return(centrality_results)

top_acts_frequency = dict_sort(acts_frequency)
print(top_acts_frequency)

i = 0
for top_act in top_acts_frequency:
    i += 1
    act_dist = unique_acts[top_act]
    act_dist_tuple = [(year, act_dist[year]) for year in act_dist]
    plot_distribution(act_dist_tuple, "Citations of act: '{}' over 1953-2018".format(top_act), filename="{}_Citations_of_{}.png".format(i, top_act))
