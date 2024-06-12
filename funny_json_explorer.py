from abc import ABC, abstractmethod

# Component
class Node(ABC):
    @abstractmethod
    def draw(self, level=0):
        pass

# Leaf
class Leaf(Node):
    def __init__(self, name, icon=None):
        self.name = name
        self.icon = icon

    def draw(self, level=0, style="tree"):
        icon_display = f" {self.icon}" if self.icon else ""
        prefix = f"{'|   ' * level}|-- " if style == "tree" else f"{'--' * (level + 1)}"
        return f"{prefix}{self.name}{icon_display}\n"

# Composite
class Container(Node):
    def __init__(self, name, icon=None):
        self.name = name
        self.icon = icon
        self.children = []

    def add(self, node):
        self.children.append(node)

    def draw(self, level=0, style="tree"):
        icon_display = f" {self.icon}" if self.icon else ""
        prefix = f"{'|   ' * level}|-- " if style == "tree" else f"{'--' * (level + 1)}"
        result = f"{prefix}{self.name}{icon_display}\n"
        for child in self.children:
            result += child.draw(level + 1, style)
        return result

# Abstract Factory
class NodeFactory(ABC):
    @abstractmethod
    def create_leaf(self, name, icon=None):
        pass

    @abstractmethod
    def create_container(self, name, icon=None):
        pass

# Concrete Factory
class DefaultNodeFactory(NodeFactory):
    def create_leaf(self, name, icon=None):
        return Leaf(name, icon)

    def create_container(self, name, icon=None):
        return Container(name, icon)

# Builder
class JSONBuilder:
    def __init__(self, factory):
        self.factory = factory
        self.root = None

    def build(self, json_data):
        self.root = self._build_node(json_data)

    def _build_node(self, data, name="root"):
        if isinstance(data, dict):
            node = self.factory.create_container(name)
            for key, value in data.items():
                node.add(self._build_node(value, key))
        elif isinstance(data, list):
            node = self.factory.create_container(name)
            for index, item in enumerate(data):
                node.add(self._build_node(item, str(index)))
        else:
            node = self.factory.create_leaf(name, str(data))
        return node

    def get_result(self):
        return self.root

# Client code
import json

def main(json_str, style="tree", icon_family=None):
    json_data = json.loads(json_str)
    factory = DefaultNodeFactory()
    builder = JSONBuilder(factory)
    builder.build(json_data)

    result = builder.get_result()
    print(result.draw(style=style))

if __name__ == "__main__":
    json_str = '''
    {
        "oranges": {
            "mandarin": null,
            "clementine": null,
            "tangerine": "cheap & juicy!"
        },
        "apples": {
            "gala": null,
            "pink lady": null
        }
    }
    '''

    # Style: tree, Icon family: None
    print("Style: tree, Icon family: None")
    main(json_str, style="tree", icon_family=None)
    print("\n")

    # Style: tree, Icon family: example
    print("Style: tree, Icon family: example")
    main(json_str, style="tree", icon_family="example")
    print("\n")

    # Style: rectangle, Icon family: None
    print("Style: rectangle, Icon family: None")
    main(json_str, style="rectangle", icon_family=None)
    print("\n")

    # Style: rectangle, Icon family: example
    print("Style: rectangle, Icon family: example")
    main(json_str, style="rectangle", icon_family="example")
    print("\n")
