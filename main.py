import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as mpa
import numpy as np
# 75 looks nice
np.random.seed(7)
"""Create networkX graph to visualise"""
# animation is based off of the concept from:
# https://stackoverflow.com/questions/43646550/how-to-use-an-update-function-to-animate-a-networkx-graph-in-matplotlib-2-0-0?rq=1

# number of nodes
n = 20
# generate positions of nodes
p = {i: (np.random.normal(0, 0.12), np.random.normal(0, 0.12)) for i in range(n)}
G = nx.random_geometric_graph(n, 0.172, pos=p)
# get positions of each node
position = nx.get_node_attributes(G, 'pos')
edges = G.edges
nodes = G.nodes
# labels for edge weights
edge_weights_labels = []
# create adjacency list
adj_list = {}

# fill adjacency list
for node in nodes:
    adj_list[node] = []
for edge in edges:
    node = edge[0]
    connected_node = edge[1]
    # generate weights by calculating distance between the two nodes
    x1, y1 = position[node][0], position[node][1]
    x2, y2 = position[connected_node][0], position[connected_node][1]
    # the weight is the distance between the two connected nodes multiplied by 100 and rounded to 1 decimal place
    weight = round((((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5) * 100, 1)
    adj_list[node].append([connected_node, weight])
    adj_list[connected_node].append([node, weight])
    # fill edge_weight_labels
    if edge not in edge_weights_labels:
        edge_weights_labels.append([edge[0], edge[1], weight])

print("edge weights:", edge_weights_labels)
print("adj list:", adj_list)


def bfs(graph, start):
    """
    Runs bfs on a graph with the purpose of visualising it

    Parameters
    ----------
    graph : dict
        Dictionary with nodes as keys and values as the adjacent nodes and weights as values
    start : int
        Starting node

    Returns
    -------
    order_visited : list
        list containing order of nodes visited
    """
    queue = []
    bfs_visited = [0 for i in range(len(adj_list.keys()))]
    queue.append(start)
    # mark as visited
    bfs_visited[start] = 1
    # store order of visited nodes
    order_visited = []
    # while there is something in the queue
    while queue:
        current_node = queue[0]
        # for each adjacent node to the current node
        for neighbour in graph[current_node]:
            adjacent_node = neighbour[0]
            # if the vertex has not been visited yet
            if bfs_visited[adjacent_node] == 0:
                order_visited.append((current_node, adjacent_node))
                # add adjacent (neighbour) node to queue
                queue.append(adjacent_node)
                # mark as visited
                bfs_visited[adjacent_node] = 1
        queue.pop(0)
    return order_visited


def kruskals(G, N):
    root = list(range(N))
    steps = []
    added = []
    edges = edge_weights_labels
    edges.sort(key=lambda x: x[2])

    def find(x):
        if root[x] == x:
            return x

        root[x] = find(root[x])
        return root[x]

    def join(a, b):
        root[find(a)] = root[find(b)]

    order_vis = []

    for i in range(len(edges)):
        added = False
        a = edges[i][0]
        b = edges[i][1]
        wt = edges[i][2]

        if find(a) != find(b):
            join(a, b)
            added = True

        order_vis.append([edges[i], added])
    return order_vis


"""
Animation created using matplotlib animation function
"""


def update_bfs(itr):
    """
    For BFS
    Parameters
    ----------
    itr : int
        An iterable
    """
    plt.clf()
    # bfs
    node_col = 'blue'

    targeted_nodes = []

    order = bfs(adj_list, 0)

    targeted_index = itr % len(order)
    targeted_edges = [order[targeted_index]]
    targeted_nodes.append(order[targeted_index][1])
    already_visited_nodes = [0]
    already_visited_nodes.extend(item[1] for item in order[:targeted_index])

    already_visited_edges = order[:targeted_index]

    nx.draw_networkx_edges(G, position, width=2, alpha=0.5)
    nx.draw_networkx_edges(G, position, edgelist=targeted_edges, width=4, edge_color='red', alpha=1)
    nx.draw_networkx_edges(G, position, edgelist=already_visited_edges, width=4, edge_color='orange', alpha=1)

    nx.draw_networkx_nodes(G, position, node_size=250, node_color=node_col)
    nx.draw_networkx_nodes(G, position, nodelist=already_visited_nodes, node_size=250, node_color='orange')
    nx.draw_networkx_nodes(G, position, nodelist=targeted_nodes, node_size=250, node_color='red')
    plt.tight_layout()


def update_mst(itr):
    """
    Meant to visualise kruskals
    Parameters
    ----------
    itr : int
        iterable

    """
    plt.clf()

    order = kruskals(edge_weights_labels, n)

    targeted_index = itr % len(order)
    current_edge = [(order[targeted_index][0][0], order[targeted_index][0][1])]
    show = order[targeted_index][1]
    current_node = []
    already_visited_nodes = []
    already_visited_edges = [tuple(edge[0][:2]) for edge in order[:targeted_index] if edge[1]]
    print(already_visited_edges)

    # draw
    nx.draw_networkx_edges(G, position, width=2, alpha=0.5)
    nx.draw_networkx_edges(G, position, edgelist=already_visited_edges, width=4, edge_color='red', alpha=1)
    nx.draw_networkx_edges(G, position, edgelist=current_edge, width=4, edge_color='orange', alpha=1)

    nx.draw_networkx_nodes(G, position, node_size=250, node_color='blue')
    nx.draw_networkx_nodes(G, position, nodelist=already_visited_nodes, node_size=250, node_color='orange')
    nx.draw_networkx_labels(G, position)
    plt.tight_layout()


fig, ax = plt.subplots(figsize=(14, 7))
# ani_bfs = mpa.FuncAnimation(fig, update_bfs, interval=300, repeat=True)
ani_mst = mpa.FuncAnimation(fig, update_mst, interval=300, repeat=True)

plt.show()
