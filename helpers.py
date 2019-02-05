import collections
import matplotlib.pyplot as plt
from models.case import Case
from models.legal_knowledge_graph import LegalKnowledgeGraph

# TODO: complete this for tuple input (taken from out_degree_distibution()
def plot_distribution(distribution, title):
    degree = [d for (d,c) in distribution]
    count = [c for (d,c) in distribution]

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
            if i > MAX_LIMIT:
                break

            cited_by, cited_to = line.rstrip().split("-->")
            case1 = Case(txt_string=cited_by)
            case2 = Case(txt_string=cited_to)

            print(i, case1.uuid, case2.uuid)

            G.add_citation(case1, case2)
            i += 1

    return(G)
