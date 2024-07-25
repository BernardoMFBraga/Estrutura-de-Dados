import networkx as nx
import matplotlib.pyplot as plt

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.count = 1  # Contador de nós repetidos

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)
        else:
            node.count += 1  # Incrementa o contador se o valor for repetido

    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        if node is None:
            return node

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            if node.count > 1:
                node.count -= 1  # Decrementa o contador se houver nós repetidos
                return node

            # Caso contrário, prossegue com a exclusão do nó
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            min_larger_node = self._get_min(node.right)
            node.value = min_larger_node.value
            node.count = min_larger_node.count
            node.right = self._delete_recursive(node.right, min_larger_node.value)

        return node

    def _get_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder_traversal(self):
        return self._inorder_recursive(self.root, [])

    def _inorder_recursive(self, node, traversal):
        if node:
            self._inorder_recursive(node.left, traversal)
            traversal.append((node.value, node.count))
            self._inorder_recursive(node.right, traversal)
        return traversal

    def draw_tree(self, title="Tree"):
        graph = nx.DiGraph()
        pos = self._add_edges(graph, self.root)
        labels = {node: node for node in graph.nodes()}
        plt.figure(figsize=(8, 6))
        plt.title(title)
        nx.draw(graph, pos, labels=labels, with_labels=True, node_size=2000, node_color="skyblue", font_size=16, font_weight="bold", arrows=False)
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        plt.show()

    def _add_edges(self, graph, node, pos=None, x=0, y=0, layer=1):
        if pos is None:
            pos = {}
        if node:
            pos[node.value] = (x, y)
            if node.left:
                graph.add_edge(node.value, node.left.value)
                l = x - 1 / layer
                pos = self._add_edges(graph, node.left, x=l, y=y-1, pos=pos, layer=layer+1)
            if node.right:
                graph.add_edge(node.value, node.right.value)
                r = x + 1 / layer
                pos = self._add_edges(graph, node.right, x=r, y=y-1, pos=pos, layer=layer+1)
        return pos

# Exemplo de uso
bt = BinaryTree()

# Inserções
bt.insert(5)
bt.insert(3)
bt.insert(7)
bt.insert(2)
bt.insert(4)
bt.insert(2)  # Inserção de um valor repetido
bt.insert(6)
bt.insert(8)
bt.insert(3)  # Inserção de um valor repetido

# Verifica a árvore após as inserções
print("Inorder traversal após inserções:", bt.inorder_traversal())
bt.draw_tree(title="Árvore Binária Após Inserções")

# Exclusões
bt.delete(2)
bt.delete(7)

# Verifica a árvore após as exclusões
print("Inorder traversal após exclusões:", bt.inorder_traversal())
bt.draw_tree(title="Árvore Binária Após Exclusões")
