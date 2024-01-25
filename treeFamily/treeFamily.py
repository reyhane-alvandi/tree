
from hash import sha256
import matplotlib.pyplot as plt
import networkx as nx

class TreeNode:
    def __init__(self, name, parents=None):
        self.name = name  # Hashing the name
        self.parents = parents if parents else []
        self.children = []

    def add_child(self, child):
        self.children.append(child)

class Tree:
    def __init__(self, root):
        self.root = root
        self.size = 1

    def add(self, parent_name, child_name):      #balanced O(log N) , else O(N)
        parent_node = self.find_node(parent_name)
        if parent_node:
            new_child = TreeNode(child_name, parents=[parent_node])
            parent_node.add_child(new_child)
            self.size += 1
        else:
            pass
    def delete(self, name):       #balanced O(log N) , else O(N)
        node_to_delete = self.find_node(name)
        if node_to_delete:
            parent = node_to_delete.parents[0] if node_to_delete.parents else None
            if parent:
                parent.children.remove(node_to_delete)
                return True
        return False
    def find_node(self, name):      #O(log N) , worst case O(N)
        return self._find_node(name, self.root)

    def _find_node(self, name_hash, current_node):
        if current_node.name == name_hash:
            return current_node
        for child in current_node.children:
            result = self._find_node(name_hash, child)
            if result:
                return result
        return None
    def _find_all_nodes(self, current_node):  #O(N)
        nodes = [current_node]
        for child in current_node.children:
            nodes.extend(self._find_all_nodes(child))
        return nodes
    def lca(self, node1_name, node2_name):  # O(N)
      node1 = self.find_node(node1_name)
      node2 = self.find_node(node2_name)

      if node1 and node2:
        lca_node = self._lca(self.root, node1, node2)
        return lca_node.name if lca_node else None
            
      else:
        return None

    def _lca(self, current_node, node1, node2):
     if current_node is None:
        return None

     if current_node == node1 or current_node == node2:
        return current_node

     if current_node.children:
        if len(current_node.children) >= 1:
            lca_left = self._lca(current_node.children[0], node1, node2)
        else:
            lca_left = None

        if len(current_node.children) >= 2:
            lca_right = self._lca(current_node.children[1], node1, node2)
        else:
            lca_right = None

        if lca_left and lca_right:
            return current_node
        elif lca_left:
            return lca_left
        else:
            return lca_right

     return None
 
    def display_tree(self):     #O(N)
        self._display_tree(self.root)

    def _display_tree(self, node, level=0):
        indent = "  " * level
        print(f"{indent}{node.name}")
        for child in node.children:
            self._display_tree(child, level + 1)