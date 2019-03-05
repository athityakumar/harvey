import collections
import matplotlib.pyplot as plt
from models.case import Case
from models.legal_knowledge_graph import LegalKnowledgeGraph
from globals import *

# TODO: complete this for tuple input (taken from out_degree_distibution()
def plot_distribution(distribution, title="Default value", filename=None):
    degree = [d for (d, c) in distribution]
    count = [c for (d, c) in distribution]

    fig, ax = plt.subplots()
    plt.bar(degree, count, width=0.80, color='b')

    plt.title("{} Histogram".format(title))
    plt.ylabel("Count")
    plt.xlabel(title)
    ax.set_xticks([d for d in degree])
    plt.xticks(rotation=90, fontSize=5)
    ax.set_xticklabels(degree)

    if filename:
        plt.savefig(filename, bbox_inches='tight', dpi=(200))
    else:
        plt.show()

def init_graph(filename):
    MAX_LIMIT = 1000
    i = 1
    G = LegalKnowledgeGraph()

    with open(filename) as f:
        for line in f.readlines():
            # if i > MAX_LIMIT:
            #     break

            cited_by, cited_to = line.rstrip().split("-->")
            case1 = Case(txt_string=cited_by)
            case2 = Case(txt_string=cited_to)

            print(i, case1.uuid, case2.uuid)

            CASE_ID_TO_NAME_MAPPING[case1.uuid] = case1.title
            CASE_ID_TO_NAME_MAPPING[case2.uuid] = case2.title
            CASE_NAME_TO_ID_MAPPING[case1.title] = case1.uuid
            CASE_NAME_TO_ID_MAPPING[case2.title] = case2.uuid
            G.add_citation(case1, case2)
            i += 1

    return(G)

def compute_landmark_cases(centrality_function, G, centrality_type, n=30):
    centrality_results = centrality_function(G)

    if type(centrality_results) is dict:
        centrality_results = sorted(list(centrality_results.items()), key= lambda k: k[1], reverse=True)[:n]
        centrality_results = dict(centrality_results)
    else:
        centrality_results = list(centrality_results)
        for i in range(len(centrality_results)):
            centrality_results[i] = sorted(list(centrality_results[i].items()), key= lambda k: k[1], reverse=True)[:n]
    return(centrality_results)

def print_landmark_cases(centrality_function, G, centrality_type, n=30):
    print("Top cases according to {}:".format(centrality_type))
    centrality_results = compute_landmark_cases(centrality_function, G, centrality_type, n)

    if type(centrality_results) is dict:
        for i, case_id in enumerate(centrality_results):
            value = centrality_results[case_id]
            print(i+1, "\t", case_id, "\t", CASE_ID_TO_NAME_MAPPING[case_id], "\t", value)
    else:
        for i, centrality_result in enumerate(list(centrality_results)):
            print("Type {}".format(i+1))
            for j, (case_id, value) in enumerate(centrality_result):
                print(j+1, "\t", case_id, "\t", CASE_ID_TO_NAME_MAPPING[case_id], "\t", value)
