from pathlib import Path
from reathon.exceptions import InvalidNodeMethod

class Node:
    def __init__(self, *nodes_to_add, **kwargs):
        self.nodes = []
        self.props = {}
        self.parents = []
        self.add(*nodes_to_add)
        for x, y in kwargs.items():
            self.props[x.upper()] = y

    def add(self, *nodes_to_add):
        for node in nodes_to_add:
            if isinstance(node, self.valid_children):
                self.nodes.append(node)
                node.parents.append(self) # add the self to the parents of the node
            else:
                print(f'You cannot add a {node.name} to a {self.name}')
        return self


class Project(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        self.name = 'REAPER_PROJECT'
        self.valid_children = Track
        self.string = ''
        super().__init__(*nodes_to_add, **kwargs)

    def traverse(self, origin):
        self.string += f'<{origin.name}\n'
        for k, v in origin.props.items():
                self.string += f'{k} {v}\n'
        for node in origin.nodes:
            self.traverse(node)
        self.string += '>\n'

    def write(self, path):
        self.traverse(self)
        with open(path, "w") as f:
            f.write(self.string)

class Track(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        self.name = 'TRACK'
        self.valid_children = Item
        super().__init__(*nodes_to_add, **kwargs)
        
class Item(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        self.name = 'ITEM'
        self.valid_children = Source
        super().__init__(*nodes_to_add, **kwargs)

class Source(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        self.valid_children = Source
        self.extension_lookup = {
            '.wav' : 'WAVE',
            '.wave' : 'WAVE',
            '.aiff' : 'WAVE',
            '.aif' : 'WAVE',
            '.mp3' : 'MP3',
            '.ogg' : 'VORBIS'
        }
        super().__init__(*nodes_to_add, **kwargs)
        self.process_extension()
        self.clean_path()

    def process_extension(self):
        try: 
            ext = Path(self.props['FILE']).suffix
            self.name = f'SOURCE {self.extension_lookup[ext]}'
        except KeyError:
            self.name = 'SOURCE SECTION'
    
    def clean_path(self):
        if 'FILE' in self.props:
            self.props['FILE'] = f"'{self.props['FILE']}'"



