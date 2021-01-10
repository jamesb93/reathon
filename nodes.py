from pathlib import Path
from exceptions import InvalidNodeMethod

class Node:
    def __init__(self, *nodes_to_add, **kwargs):
        self.nodes = []
        self.props = {}
        self.parents = []
        self.add(*nodes_to_add)
        for x, y in kwargs.items():
            if hasattr(self, x):
                method = getattr(self, x)
                method(y)
            else:
                raise InvalidNodeMethod(self, x)

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
    #item has to have length and position but not sure if anything else
    # can have volume set in absolute and it converts to DB
    # VOLPAN 0.5 0 1 -1
    def __init__(self, *nodes_to_add, **kwargs):
        self.name = 'ITEM'
        self.valid_children = Source
        super().__init__(*nodes_to_add, **kwargs)
    
    def length(self, length):
        self.props['LENGTH'] = length
        return self

    def position(self, pos):
        self.props['POSITION'] = pos
        return self

class Source(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        self.name = 'SOURCE'
        self.valid_children = ''
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


