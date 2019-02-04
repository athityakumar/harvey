import networkx as nx
G = nx.DiGraph()

i = 1

with open('case-case-citation.txt') as f:
    for line in f.readlines():
        # if i>10:
        #     break

        cited_by, cited_to = line.rstrip().split("-->")
        cited_by_uuid = cited_by.split("(")[-1].split(")")[0]
        cited_to_uuid = cited_to.split("(")[-1].split(")")[0]

        print(i, cited_by_uuid, cited_to_uuid)

        G.add_edge(cited_by_uuid, cited_to_uuid)
        i += 1

print(len(G.nodes()))
print(len(G.edges()))
