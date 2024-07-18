import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Passo 1: Criar o grafo
G = nx.DiGraph()
edges = [('A', 'B', 1), ('A', 'C', 4), ('B', 'C', 2), ('C', 'D', 1), ('D', 'A', 5)]
G.add_weighted_edges_from(edges)

# Função para desenhar o grafo com curvas nas arestas
def draw_graph(G, pos, title, ax):
    ax.set_title(title)
    edge_colors = 'black'  # Todas as arestas serão pretas
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=15, font_weight='bold', arrowsize=20, edge_color=edge_colors, ax=ax)

    labels = nx.get_edge_attributes(G, 'weight')
    
    for u, v, data in G.edges(data=True):
        # Converter as posições para arrays numpy para realizar operações matemáticas
        pos_u = np.array(pos[u])
        pos_v = np.array(pos[v])
        
        # Calcular a curva da aresta
        edge_width = np.sqrt(data['weight']) * 0.1
        
        # Determinar o estilo da seta e a posição do texto da distância
        if G.has_edge(v, u):  # Verificar se há uma aresta no sentido contrário
            arrowprops = dict(arrowstyle="<->", color='black', linestyle='--', linewidth=edge_width, shrinkA=15, shrinkB=15)
            pos_text = 0.5 * (pos_u + pos_v) + np.array([0.1, -0.1])
        else:
            arrowprops = dict(arrowstyle="->", color='black', linewidth=edge_width, shrinkA=15, shrinkB=15)
            pos_text = pos_v + 0.25 * (pos_u - pos_v)  # Posicionar texto mais perto de v

        # Determinar o ângulo da seta
        angle = np.arctan2(pos_v[1] - pos_u[1], pos_v[0] - pos_u[0])
        angle = np.degrees(angle)

        # Ajustar a posição da etiqueta para evitar sobreposição
        pos_text_final = pos_v + 0.1 * (pos_u - pos_v)
        
        ax.annotate("",
                    xy=pos_u, 
                    xytext=pos_v,
                    arrowprops=arrowprops,
                    )

        ax.text(pos_text_final[0], pos_text_final[1], f'{data["weight"]}', fontsize=12, ha='center', va='center', rotation=angle, rotation_mode='anchor', bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.3'))

# Layout fixo para os nós (novas posições)
fixed_pos = {'A': (0, 0), 'B': (2, 1), 'C': (1, 2), 'D': (1, 0)}

# Implementar Floyd-Warshall para encontrar as menores distâncias
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

# Mostrar a matriz de distâncias finais
print("Matriz de Distâncias Finais:")
nodes = list(G.nodes)
distances = floyd_warshall(G)
dist_matrix = np.zeros((len(nodes), len(nodes)))

for i, u in enumerate(nodes):
    for j, v in enumerate(nodes):
        dist_matrix[i][j] = distances[u][v]

print(dist_matrix)

# Desenhar o grafo com as menores distâncias
G_shortest = nx.DiGraph()

for i, u in enumerate(nodes):
    for j, v in enumerate(nodes):
        if i != j and dist_matrix[i][j] < float('inf'):
            G_shortest.add_edge(u, v, weight=dist_matrix[i][j])

# Criar subplots para os grafos e a matriz de distâncias
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

draw_graph(G, fixed_pos, "Grafo Original", ax1)
draw_graph(G_shortest, fixed_pos, "Grafo com Menores Distâncias (Floyd-Warshall)", ax2)

# Ajustar o layout dos grafos
fig1.tight_layout(pad=5.0)

# Criar uma nova figura para a matriz de distâncias
fig2, ax3 = plt.subplots(figsize=(6, 6))

# Exibir a matriz de distâncias
ax3.matshow(dist_matrix, cmap=plt.cm.Blues)

for i in range(len(nodes)):
    for j in range(len(nodes)):
        c = dist_matrix[j, i]
        ax3.text(i, j, f'{c:.1f}', va='center', ha='center')

ax3.set_title("Matriz de Distâncias Finais")
ax3.set_xticks(range(len(nodes)))
ax3.set_xticklabels(nodes)
ax3.set_yticks(range(len(nodes)))
ax3.set_yticklabels(nodes)

# Ajustar o layout da matriz
fig2.tight_layout(pad=5.0)

# Exibir ambas as figuras
plt.show()
