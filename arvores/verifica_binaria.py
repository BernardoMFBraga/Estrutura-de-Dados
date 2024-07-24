import networkx as nx
import matplotlib.pyplot as plt

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def is_binary_tree(node):
    # Se a árvore está vazia, é uma árvore binária por definição
    if node is None:
        return True
    
    # Verifica se o nó tem mais de dois filhos (não pode acontecer em uma árvore binária)
    if hasattr(node, 'middle'):
        return False

    return is_binary_tree(node.left) and is_binary_tree(node.right)

def add_edges(graph, node, pos=None, x=0, y=0, layer=1):
    if pos is None:
        pos = {}
    pos[node.value] = (x, y)
    if node.left:
        graph.add_edge(node.value, node.left.value)
        l = x - 1 / layer
        pos = add_edges(graph, node.left, x=l, y=y-1, pos=pos, layer=layer+1)
    if node.right:
        graph.add_edge(node.value, node.right.value)
        r = x + 1 / layer
        pos = add_edges(graph, node.right, x=r, y=y-1, pos=pos, layer=layer+1)
    if hasattr(node, 'middle'):
        graph.add_edge(node.value, node.middle.value)
        m = x
        pos = add_edges(graph, node.middle, x=m, y=y-1, pos=pos, layer=layer+1)
    return pos

def draw_tree(root, title="Tree"):
    graph = nx.DiGraph()
    pos = add_edges(graph, root)
    labels = {node: node for node in graph.nodes()}
    plt.figure(figsize=(8, 6))
    plt.title(title)
    nx.draw(graph, pos, labels=labels, with_labels=True, node_size=2000, node_color="skyblue", font_size=16, font_weight="bold", arrows=False)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    plt.show()

# Exemplo de uso
# Cria uma árvore binária simples
root_binary = TreeNode(1)
root_binary.left = TreeNode(2)
root_binary.right = TreeNode(3)
root_binary.left.left = TreeNode(4)
root_binary.left.right = TreeNode(5)

# Verifica se é uma árvore binária
print("Árvore binária válida:", is_binary_tree(root_binary))  # Deve retornar True
draw_tree(root_binary, title="Árvore Binária")

# Cria uma árvore não binária (com mais de dois filhos para um nó)
root_non_binary = TreeNode(1)
root_non_binary.left = TreeNode(2)
root_non_binary.right = TreeNode(3)
root_non_binary.left.left = TreeNode(4)
root_non_binary.left.right = TreeNode(5)
# Adiciona um terceiro filho ao nó root_non_binary.left (não permitido em árvores binárias)
root_non_binary.left.middle = TreeNode(6)  # Exemplo inválido, pois não existe 'middle' em uma árvore binária

# Verifica se é uma árvore binária
print("Árvore binária válida:", is_binary_tree(root_non_binary))  # Deve retornar False
draw_tree(root_non_binary, title="Árvore Não Binária")
