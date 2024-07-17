import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Passo 1: Criar o grafo
G = nx.DiGraph()
edges = [('A', 'B', 1), ('A', 'C', 4), ('B', 'C', 2), ('C', 'D', 1), ('D', 'A', 5)]
G.add_weighted_edges_from(edges)

# Função para desenhar o grafo
def draw_graph(G, pos, title):
    plt.figure(figsize=(8, 6))
    plt.title(title)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=15, font_weight='bold', arrowsize=20)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=15)
    plt.show()

# Desenhar o grafo original
pos = nx.spring_layout(G)
draw_graph(G, pos, "Grafo Original")

# Passo 2: Implementar Floyd-Warshall
def floyd_warshall(graph):
    nodes = list(graph.nodes)
    n = len(nodes)
    dist = {node: {node2: float('inf') for node2 in nodes} for node in nodes}

    for node in nodes:
        dist[node][node] = 0

    for u, v, data in graph.edges(data=True):
        dist[u][v] = data['weight']

    for k in nodes:
        for i in nodes:
            for j in nodes:
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist

distances = floyd_warshall(G)

# Passo 3: Mostrar a matriz de distâncias finais
print("Matriz de Distâncias Finais:")
nodes = list(G.nodes)
dist_matrix = np.zeros((len(nodes), len(nodes)))

for i, u in enumerate(nodes):
    for j, v in enumerate(nodes):
        dist_matrix[i][j] = distances[u][v]

print(dist_matrix)

# Passo 4: Desenhar o grafo com as menores distâncias
G_shortest = nx.DiGraph()

for i, u in enumerate(nodes):
    for j, v in enumerate(nodes):
        if i != j and dist_matrix[i][j] < float('inf'):
            G_shortest.add_edge(u, v, weight=dist_matrix[i][j])

draw_graph(G_shortest, pos, "Grafo com Menores Distâncias (Floyd-Warshall)")
