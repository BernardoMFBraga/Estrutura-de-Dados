import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if node is None:
            return Node(key)
        if key < node.key:
            node.left = self._insert_recursive(node.left, key)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key)
        return node

    def rotate_right(self, node):
        if node is None or node.left is None:
            return node

        # Realiza a primeira rotação simples à direita entre B e C
        node.left = self._rotate_right(node.left)

        # Realiza a segunda rotação simples à direita entre A e B
        return self._rotate_left(node)

    def _rotate_left(self, node):
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        return new_root

    def _rotate_right(self, node):
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        return new_root

    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.key)
            self._inorder_recursive(node.right, result)

    def print_tree(self):
        self._print_tree_recursive(self.root, 0)

    def _print_tree_recursive(self, node, depth):
        if node is not None:
            self._print_tree_recursive(node.right, depth + 1)
            print("   " * depth + "->", node.key)
            self._print_tree_recursive(node.left, depth + 1)

    def draw_tree(self, ax, title="Tree"):
        G = nx.DiGraph()
        self._add_edges(self.root, G)
        pos = self._get_positions(self.root)
        labels = {node: node for node in G.nodes()}

        nx.draw(G, pos, labels=labels, with_labels=True, node_size=2000, node_color="skyblue", font_size=16, font_weight="bold", arrows=True, ax=ax)
        ax.set_title(title)

    def _add_edges(self, node, graph):
        if node:
            if node.left:
                graph.add_edge(node.key, node.left.key)
                self._add_edges(node.left, graph)
            if node.right:
                graph.add_edge(node.key, node.right.key)
                self._add_edges(node.right, graph)

    def _get_positions(self, node, pos=None, x=0, y=0, layer=1):
        if pos is None:
            pos = {}
        if node:
            pos[node.key] = (x, y)
            if node.left:
                l = x - 1 / layer
                pos = self._get_positions(node.left, pos, l, y - 1, layer + 1)
            if node.right:
                r = x + 1 / layer
                pos = self._get_positions(node.right, pos, r, y - 1, layer + 1)
        return pos

# Exemplo de uso:
if __name__ == "__main__":
    bst = BinarySearchTree()
    keys = [30, 20, 40, 10, 25, 35, 50, 5, 15]

    for key in keys:
        bst.insert(key)

    print("Árvore original:")
    bst.print_tree()

    # Cria uma figura com dois subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Desenha a árvore original
    bst.draw_tree(ax1, "Árvore Original")

    # Realiza a rotação dupla à direita no nó com chave 30
    bst.root = bst.rotate_right(bst.root)

    print("\nÁrvore após a rotação dupla à direita:")
    bst.print_tree()

    # Desenha a árvore após a rotação
    bst.draw_tree(ax2, "Árvore Após Rotação Dupla à Direita")

    plt.show()

    print("\nInorder traversal da árvore após a rotação:")
    print(bst.inorder_traversal())
