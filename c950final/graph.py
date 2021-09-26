import networkx as nx
import matplotlib.pyplot as plt
import csv


LOC_FILE = 'c950final/data/locations.csv'
EDGE_FILE = 'c950final/data/edges.csv'
GRAPH_PIC = 'c950final/data/graph.png'


def print_full_graph():
    g = nx.Graph()

    with open(LOC_FILE, 'r', newline='') as loc_file:
        reader = csv.reader(loc_file)
        for location in reader:
            g.add_node(location[0])

    with open(EDGE_FILE, 'r') as edge_file:
        reader = csv.reader(edge_file)
        for line in reader:
            g.add_edge(line[0], line[2], dist=line[1])

    nx.draw(g, with_labels=True, pos=nx.circular_layout(g, 15))
    plt.savefig(GRAPH_PIC)
    #plt.show()
    print("Done printing graph.")


def print_path(path):
    # TODO
    print("Done printing path.")


if __name__ == "__main__":
    print_graph()