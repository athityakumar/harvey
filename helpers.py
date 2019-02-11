import collections
import matplotlib.pyplot as plt
from models.case import Case
from models.legal_knowledge_graph import LegalKnowledgeGraph


# TODO: complete this for tuple input (taken from out_degree_distibution()
def plot_distribution(distribution, title):
    degree = [d for (d, c) in distribution]
    count = [c for (d, c) in distribution]

    fig, ax = plt.subplots()
    plt.bar(degree, count, width=0.80, color='b')

    plt.title("{} Histogram".format(title))
    plt.ylabel("Count")
    plt.xlabel(title)
    ax.set_xticks([d for d in degree])
    ax.set_xticklabels(degree)
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

            G.add_citation(case1, case2)
            i += 1

    return(G)

def print_landmark_cases(centrality_function, G, centrality_type, n=10):
    print("Top cases according to {}:".format(centrality_type))
    centrality_results = centrality_function(G)

    if type(centrality_results) is dict:
        centrality_results = sorted(list(centrality_results.items()), key= lambda k: k[1], reverse=True)[:n]
    else:
        centrality_results = list(centrality_results)
        for i in range(len(centrality_results)):
            centrality_results[i] = sorted(list(centrality_results[i].items()), key= lambda k: k[1], reverse=True)[:n]
    if type(centrality_results) is dict:
        for case_id, value in centrality_results:
            print(case_id, value)
    else:
        for centrality_result in list(centrality_results):
            for case_id, value in centrality_result:
                print(case_id, value)
