from pathlib import Path
from reathon.exceptions import InvalidNodeMethod
from reathon.helper import region, marker


class Node:
    def __init__(self, *nodes_to_add, **kwargs):
        self.nodes = []
        self.props = []
        self.parents = []
        self.add(*nodes_to_add)
        for prop, value in kwargs.items():
            if isinstance(value, str) or isinstance(value, Path):
                value = f'"{value}"'
            self.props.append([prop.upper(), value])

    def add(self, *nodes_to_add):
        for node in nodes_to_add:
            if isinstance(node, self.valid_children):
                self.nodes.append(node)
                node.parents.append(self)  # add the self to the parents of the node
            else:
                print(f"You cannot add a {node.name} to a {self.name}")
        return self


class Project(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        self.name = "REAPER_PROJECT"
        self.valid_children = Track
        self.string = ""
        super().__init__(*nodes_to_add, **kwargs)

    def traverse(self, origin):
        self.string += f"<{origin.name}\n"

        for state in origin.props:
            self.string += f"{state[0]} {state[1]}\n"

        for node in origin.nodes:
            self.traverse(node)
        self.string += ">\n"

    def write(self, path):
        self.traverse(self)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.string)

    def add_marker(self, index: int, time: float, name: str, color: int = 0):
        new_marker = marker(index, time, name, color)
        self.props.append(new_marker)

    def add_region(
        self, index: int, start: float, end: float, name: str, color: int = 0
    ):
        new_region = region(index, start, end, name, color)
        self.props.extend(new_region)


class Track(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        self.name = "TRACK"
        self.valid_children = Item
        super().__init__(*nodes_to_add, **kwargs)


class Item(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        self.name = "ITEM"
        self.valid_children = Source
        super().__init__(*nodes_to_add, **kwargs)


class Source(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        self.valid_children = Source
        self.extension_lookup = {
            ".wav": "WAVE",
            ".wave": "WAVE",
            ".aiff": "WAVE",
            ".aif": "WAVE",
            ".mp3": "MP3",
            ".ogg": "VORBIS",
            ".flac": "FLAC",
        }
        self.file = kwargs.get("file")
        self.process_extension()
        super().__init__(*nodes_to_add, **kwargs)

    def process_extension(self):
        if not isinstance(self.file, Path):
            self.file = Path(self.file)
        ext = self.file.suffix
        try:
            self.name = f"SOURCE {self.extension_lookup[ext]}"
        except KeyError:
            self.name = "SOURCE SECTION"
