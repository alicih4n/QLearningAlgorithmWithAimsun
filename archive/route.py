import random

class Route:
    def __init__(self, nodes):
        self.nodes = nodes
        self.current_node = None
        self.passed_nodes = []
        self.visited_nodes = set()

    def select_route(self, selection_method="random"):
        if selection_method == "random":
            self.current_node = random.choice(self.nodes)
        elif selection_method == "sequential":
            if self.current_node is None:
                self.current_node = random.choice(self.nodes)
            else:
                current_index = self.nodes.index(self.current_node)
                next_index = (current_index + 1) % len(self.nodes)
                self.current_node = self.nodes[next_index]
        else:
            pass

        self.passed_nodes.append(self.current_node)
        self.visited_nodes.add(self.current_node)

    def get_current_node(self):
        return self.current_node

    def get_next_node(self):
        if self.current_node is None:
            return None

        current_index = self.nodes.index(self.current_node)
        next_index = (current_index + 1) % len(self.nodes)
        next_node = self.nodes[next_index]
        return next_node

    def update_current_node(self, new_node):
        self.current_node = new_node
        self.passed_nodes.append(new_node)
        self.visited_nodes.add(new_node)

    def has_visited_all_nodes(self):
        return len(self.visited_nodes) == len(self.nodes)
