import collections
import matplotlib.pyplot as plt
from models.case import Case
from models.legal_knowledge_graph import LegalKnowledgeGraph
from globals import *
import numpy as np
from scipy import stats
from bs4 import BeautifulSoup

# TODO: complete this for tuple input (taken from out_degree_distibution()
def plot_distribution(distribution, title="Default value", filename=None, fontSize=5, dpi=200):
    degree = [d for (d, c) in distribution]
    count = [c for (d, c) in distribution]

    fig, ax = plt.subplots()
    plt.bar(degree, count, width=0.80, color='b')

    plt.title("{} Histogram".format(title))
    plt.ylabel("Count")
    plt.xlabel(title)
    ax.set_xticks([d for d in degree])
    plt.xticks(rotation=90, fontSize=fontSize)
    ax.set_xticklabels(degree)

    if filename:
        plt.savefig(filename, bbox_inches='tight', dpi=(dpi))
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

    with open("datafiles/all_indexes.txt") as f:
        for line in f.readlines():
            # if i > MAX_LIMIT:
            #     break
            case_path, case_name = line.rstrip().split("-->")

            if case_name in CASE_NAME_TO_ID_MAPPING:
	            case_id = CASE_NAME_TO_ID_MAPPING[case_name]
	            case_path = "datafiles/"+case_path

	            CASE_ID_TO_FILE_MAPPING[case_id] = case_path

    return(G)

def compute_landmark_cases(centrality_function, G, centrality_type, n=50):
    centrality_results = centrality_function(G)

    if type(centrality_results) is dict:
        centrality_results = sorted(list(centrality_results.items()), key= lambda k: k[1], reverse=True)
        centrality_results = dict(centrality_results)
    else:
        centrality_results = list(centrality_results)
        for i in range(len(centrality_results)):
            centrality_results[i] = sorted(list(centrality_results[i].items()), key= lambda k: k[1], reverse=True)
    return(centrality_results)

def print_landmark_cases(centrality_function, G, centrality_type, n=50):
    print("Top cases according to {}:".format(centrality_type))
    centrality_results = compute_landmark_cases(centrality_function, G, centrality_type, n)

    if type(centrality_results) is dict:
        for i, case_id in enumerate(centrality_results):
            value = centrality_results[case_id]
            print(i+1, "\t", case_id, "\t", CASE_ID_TO_NAME_MAPPING[case_id], "\t", value)
            if case_id not in case_commonality_count:
                case_commonality_count[case_id] = 1
                case_rank_cumulative_sum[case_id] = [] #rank
                case_rank_cumulative_sum[case_id].append(i+1)
            else:
                case_commonality_count[case_id] += 1
                case_rank_cumulative_sum[case_id].append(i+1)
    else:
        for i, centrality_result in enumerate(list(centrality_results)):
            print("Type {}".format(i+1))
            for j, (case_id, value) in enumerate(centrality_result):
                print(j+1, "\t", case_id, "\t", CASE_ID_TO_NAME_MAPPING[case_id], "\t", value)
                if case_id not in case_commonality_count:
                    case_commonality_count[case_id] = 1
                    case_rank_cumulative_sum[case_id] = [] #rank
                    case_rank_cumulative_sum[case_id].append(j+1)

                else:
                    case_commonality_count[case_id] += 1
                    case_rank_cumulative_sum[case_id].append(j+1)

def print_common_cases():
    
    case_commonality = sorted(case_commonality_count.items(), key=lambda kv: kv[1], reverse=True)
    print(case_commonality)
    for case_id, count in case_commonality:
        print(count, "\t", case_id, "\t", CASE_ID_TO_NAME_MAPPING[case_id])
        
    print("-" * 80)

    case_rank_cumulative = sorted(case_rank_cumulative_sum.items(), key=lambda kv: kv[1])
    print("Rank", ";\t", "case_id", ";\t", "Title", ";\t", "Harmonic mean", ";\t", "Geometric mean", ";\t", "Mean", ";\t", "Average")
    for case_id, rank in case_rank_cumulative:
        print(rank, ";\t", case_id, ";\t", CASE_ID_TO_NAME_MAPPING[case_id], ";\t", stats.hmean(rank), ";\t", stats.gmean(rank), ";\t", np.mean(rank), ";\t", np.average(rank))


def find_subjects_for_case(file):
	with open(file) as html_file:
		soup = BeautifulSoup(html_file, 'lxml')
	
	for elem in soup(text = "Subject:"):
		par = elem.parent.parent
		subject_list = par.get_text().replace("Subject:", '').split(';')
	return subject_list