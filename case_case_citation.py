import networkx as nx
G = nx.DiGraph()
MAX_LIMIT = 1000
i = 1

def get_dist_from_deg(degree):
    dist = dict()
    for (node, deg) in degree:
        if deg in dist:
            dist[deg] += 1
        else:
            dist[deg] = 1
    return(sorted(dist.items(), key=lambda k: k[1], reverse=True))

with open('case-case-citation.txt') as f:
    for line in f.readlines():
        # if i>MAX_LIMIT:
        #     break

        cited_by, cited_to = line.rstrip().split("-->")
        cited_by_uuid = cited_by.split("(")[-1].split(")")[0]
        cited_to_uuid = cited_to.split("(")[-1].split(")")[0]

        print(i, cited_by_uuid, cited_to_uuid)

        G.add_edge(cited_by_uuid, cited_to_uuid)
        i += 1

print(len(G.nodes()))
print(len(G.edges()))
print(get_dist_from_deg(G.in_degree()))
print(get_dist_from_deg(G.out_degree()))

print(nx.average_clustering(G))

import collections
import matplotlib.pyplot as plt
import networkx as nx

sum_in_degree = 0
for (deg, count) in get_dist_from_deg(G.in_degree()):
    sum_in_degree += deg*count
print(sum_in_degree/len(G.nodes()))

sum_out_degree = 0
for (deg, count) in get_dist_from_deg(G.out_degree()):
    sum_out_degree += deg*count
print(sum_out_degree/len(G.nodes()))


degree_sequence = sorted([d for n, d in G.in_degree()], reverse=True)  # degree sequence
# print "Degree sequence", degree_sequence
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())

fig, ax = plt.subplots()
plt.bar(deg, cnt, width=0.80, color='b')

plt.title("In-Degree Histogram")
plt.ylabel("Count")
plt.xlabel("In-Degree")
ax.set_xticks([d + 1 for d in deg])
ax.set_xticklabels(deg)
plt.show()

degree_sequence = sorted([d for n, d in G.out_degree()], reverse=True)  # degree sequence
# print "Degree sequence", degree_sequence
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())

fig, ax = plt.subplots()
plt.bar(deg, cnt, width=0.80, color='b')

plt.title("Out-Degree Histogram")
plt.ylabel("Count")
plt.xlabel("Out-Degree")
ax.set_xticks([d + 1 for d in deg])
ax.set_xticklabels(deg)
plt.show()

