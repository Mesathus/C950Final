import networkx as nx
import networkx.drawing
import matplotlib.pyplot as plt
import csv


g = nx.Graph()

with open('nodes.txt', 'r') as node_file:
    for line in node_file:
        g.add_node(line.strip())

with open('edges.csv', 'r') as edge_file:
    reader = csv.reader(edge_file)
    for line in reader:
        g.add_edge(line[0], line[2], dist=line[1])

nx.draw(g, with_labels=True, pos=nx.circular_layout(g, 15))
plt.savefig("graph.png")
#plt.show()

print("Done.")
