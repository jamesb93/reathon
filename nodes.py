from pathlib import Path
from exceptions import InvalidNodeMethod

# https://github.com/ReaTeam/Doc/blob/master/State%20Chunk%20Definitions

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


class Session(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        self.name = 'REAPER_PROJECT'
        self.valid_children = Track
        super().__init__(*nodes_to_add, **kwargs)

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
        
    def file(self, path):
        self.props['FILE'] = path
        self.name = f'SOURCE {self.extension_lookup[Path(path).suffix]}'
        return self


