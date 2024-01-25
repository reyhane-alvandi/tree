from Hash import sha256
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
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
    def are_parent_and_child(self, name1, name2):   #balanced O(log N) , else O(N)
        hash_name1 = name1
        hash_name2 = name2

        node1 = self.find_node(hash_name1)
        node2 = self.find_node(hash_name2)

        if node1 and node2:
            return node2 in node1.children or node1 in node2.children
        return False

    def check_siblings(self, name1, name2):       #balanced O(log N) , else O(N)
        hash_name1 = name1
        hash_name2 = name2

        node1 = self.find_node(hash_name1)
        node2 = self.find_node(hash_name2)

        if node1 and node2:
            return any(child in node2.parents[0].children for child in node1.parents[0].children)
        return False

    def are_family_related(self, name1, name2):     #balanced O(log N) , else O(N)
        hash_name1 = name1
        hash_name2 = name2

        node1 = self.find_node(hash_name1)
        node2 = self.find_node(hash_name2)

        if node1 and node2:
            if node2 in node1.children or node1 in node2.children:
                return False

            if node2.parents and node1 in node2.parents[0].children:
                return False
            elif node1.parents and node2 in node1.parents[0].children:
                return False

            return True
        else:
            return False

    def find_child_count(self, node_name):     #O(1)
        node = self.find_node(node_name)

        if node is None:
            return 0

        return len(node.children)

    def find_farthest_relationship(self, people):  #O(n^2)

        max_distance = 0
        farthest_pair = (None, None)
        for person1 in people:
            for person2 in people:
                if person1 != person2:
                    distance = self.calculate_distance(person1, person2, people)
                    if distance == "no relationship":
                        continue
                    if distance > max_distance:
                        max_distance = distance
                        farthest_pair = (person1, person2)
        return farthest_pair

    def calculate_distance(self, name1, name2, people):  #O(n)

        ancestor = self.lca(name1, name2)
        if ancestor is None:
            return "no relationship"
        distance1 = 0
        distance2 = 0
        current1 = name1
        current2 = name2
        while current1 and current1 != ancestor:
            current1 = people.get(current1, None)
            if current1:
             current1 = current1.father
             distance1 += 1

        while current2 and current2 != ancestor:
         current2 = people.get(current2, None)
         if current2:
          current2 = current2.father
          distance2 += 1

        return distance2 + distance1

class TreeVisualizer:
    def __init__(self, family_tree):
        self.family_tree = family_tree
        self.graph = nx.DiGraph()

    def build_graph(self, node, parent=None):
        self.graph.add_node(node.name)
        if parent:
            self.graph.add_edge(parent.name, node.name)
        for child in node.children:
            self.build_graph(child, parent=node)

    def visualize_tree(self):
        self.build_graph(self.family_tree.root)
        pos = self._layout_tree(self.family_tree.root)
        nx.draw(self.graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_color='black')
        plt.show()

    def _layout_tree(self, current_node, pos=None, x=0, level=1, width=2.0, vert_gap=0.4, xcenter=0.5):
        if pos is None:
            pos = {current_node.name: (x, -level * vert_gap)}
        else:
            pos[current_node.name] = (x, -level * vert_gap)
        neighbors = list(self.graph.neighbors(current_node.name))
        if len(neighbors) != 0:
            dx = width / 2
            nextx = x - width / 2 - dx / 2
            for neighbor_name in neighbors:
                neighbor_node = self.family_tree._find_node(neighbor_name, current_node)  # Pass the current_node
                if isinstance(neighbor_node, TreeNode):  # Check if it's a TreeNode
                    nextx += dx
                    pos = self._layout_tree(neighbor_node, pos=pos, x=nextx, level=level-1, width=dx, vert_gap=vert_gap, xcenter=xcenter)
        return pos

# Define people dictionary
class Person:
    def __init__(self, father):
        self.father = father

people = {
    'Grandpa': Person(None),
    'Grandma': Person(None),
    'Dad': Person('Grandpa'),
    'Mom': Person(None),
    'Son': Person('Dad'),
    'Daughter': Person('Dad'),
    'Uncle': Person('Grandpa'),
    'Aunt': Person('Grandma'),
    'Cousin': Person('Uncle'),
    'Nephew': Person('Son'),
    'Niece': Person('Daughter')
}

grandpa = TreeNode("Grandpa")
grandma = TreeNode("Grandma")
dad = TreeNode("Dad", parents=[grandpa, grandma])
mom = TreeNode("Mom")
son = TreeNode("Son", parents=[dad, mom])
daughter = TreeNode("Daughter", parents=[dad, mom])
uncle = TreeNode("Uncle", parents=[grandpa, grandma])
aunt = TreeNode("Aunt", parents=[grandpa, grandma])
cousin = TreeNode("Cousin", parents=[uncle, aunt])
nephew = TreeNode("Nephew", parents=[son])
niece = TreeNode("Niece", parents=[daughter])

grandpa.add_child(dad)
grandma.add_child(dad)
dad.add_child(son)
dad.add_child(daughter)
grandpa.add_child(uncle)
grandma.add_child(uncle)
grandpa.add_child(aunt)
grandma.add_child(aunt)
uncle.add_child(cousin)
son.add_child(nephew)
daughter.add_child(niece)

print("Family Tree:")
family_tree = Tree(root=grandpa)
family_tree.display_tree()

# Check are_parent_and_child?
parent_result = family_tree.are_parent_and_child('Daughter', 'Son')
print(f"Are parent and child? {parent_result}")

# Check are siblings or not?
siblings_result = family_tree.check_siblings('Son', 'Daughter')
print(f"Are siblings? {siblings_result}")

# Check family relationship distance
family_related = family_tree.are_family_related('Son', 'Daughter')
print(f"Are they family? {family_related}")

# Find Least Common Ancestor
common_result = family_tree.lca('Cousin', 'Son')
print(f"The common Ancestor is {common_result}")

# Get descendant count
descendant_count = family_tree.find_child_count('Grandpa')
print(f"The descendant count is {descendant_count}")

# Find furthest nodes in the relationship
furthest_node1, furthest_node2 = family_tree.find_farthest_relationship(people)
print(f"The furthest nodes are: {furthest_node1}, {furthest_node2}")


# Assuming family_tree is already created
visualizer = TreeVisualizer(family_tree)
visualizer.visualize_tree()
