from pathlib import Path
from reathon.exceptions import InvalidNodeMethod

class Node:
    def __init__(self, *nodes_to_add, **kwargs):
        if 'node_name' in kwargs:
            self.name = kwargs.get('node_name')
        else:
            self.name = 'UNTITLED'
        if 'meta_props' in kwargs:
            self.meta_props = kwargs.get('meta_props')
        else:
            self.meta_props = None
        self.valid_children = [Node, Track, Item, Source, FXChain, AU, VST]
        self.nodes = []
        self.props = []
        self.parents = []
        self.string = ''
        self.add(*nodes_to_add)
        for prop, value in kwargs.items():
            if prop == 'file':
                value = self.wrap_file(value)
            if prop != 'node_name' and prop != 'meta_props':
                self.props.append([prop.upper(), str(value)])

    def __repr__(self):
        return "Node()"

    def __str__(self):
        self.traverse(self)
        return self.string

    def add(self, *nodes_to_add):
        for node in nodes_to_add:
            if any(isinstance(node, x) for x in self.valid_children):
                self.nodes.append(node)
                node.parents.append(self) # add the self to the parents of the node
            else:
                print(f'You cannot add a {node.name} to a {self.name}')
        return self

    def get_children(self, type_query = 'Node'):
        children = []
        for node in self.nodes:
            if type(node) == type_query:
                children.append(node)
        
        return children

    def traverse(self, origin, this_level = 0):
        indent = ''
        for _ in range(this_level):
            indent += '  '
        
        if origin.meta_props != None:
            self.string += f'{indent}<{origin.name} {origin.meta_props}\n'
        else:
            self.string += f'{indent}<{origin.name}\n'

        for state in origin.props:
            self.string += f'{indent}  {state[0]} {state[1]}\n'
    
        for node in origin.nodes:
            self.traverse(node, this_level = this_level + 1)
        self.string += indent + '>\n'

    @staticmethod
    def wrap_file(path_to_wrap: str) -> str:
        return f"'{path_to_wrap}'"

class Project(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        super().__init__(*nodes_to_add, **kwargs)
        self.name = 'REAPER_PROJECT'
        self.valid_children = [Node, Track]
        self.accepted_chunks = {
            # when reading if the chunk is not in this name/class pair, a generic node will be created with name='CHUNK'.
            'PROJECT' : Project,
            'TRACK' : Track,
            'ITEM' : Item,
            'SOURCE' : Source
        } 
        if 'file' in kwargs:
            self.read(kwargs.get('file'))

    def write(self, path):
        self.traverse(self)
        with open(path, "w") as f:
            f.write(self.string)

    def get_tracks(self):
        # Get track in project either by index or track name:
        return super().get_children(type_query = Track)

    def read(self, path):
        # Read an rpp file
        self.nodes = [] # Reinit nodes.
        self.props = [] # Reinit props.

        # The first element will always be a project, and it is already created:
        current_parent = self 
        current_hierarchy = [self]
        with open(path, 'r') as f:
            # The first line is the project, so just add it's meta_props if there are any:
            first_line = f.readline()
            line_array = self.line_pre_parse(first_line)
            project_meta_props = self.get_metaprops(line_array)
            self.meta_props = project_meta_props
            
            # Now read through the rest of the file:
            for line in f:
                # Read through the lines in the rpp file:
                line_array = self.line_pre_parse(line)
                if (line_array[0][:1] == '>'):
                    # Closing a chunk:
                    if len(current_hierarchy) != 1: # Skip the last line (the project) as it was never opened!
                        current_hierarchy.pop()
                        current_parent = current_hierarchy[-1]
                else:
                    if(line_array[0][:1] == '<'):
                        # New chunk start
                        this_chunk = line_array[0][1:].replace('\n', '')

                        if(this_chunk in self.accepted_chunks):
                            accepted_chunk = self.accepted_chunks[this_chunk](meta_props = self.get_metaprops(line_array))
                        else:
                            accepted_chunk = Node(node_name = this_chunk, meta_props = self.get_metaprops(line_array))

                        current_parent.add(accepted_chunk)
                        current_parent = accepted_chunk
                        current_hierarchy.append(current_parent)
                    else:
                        # Add a property to the current parent:
                        current_parent.props.append(self.parse_prop(line_array))
                        if isinstance(current_parent, Source) and self.parse_prop(line_array)[0] == 'FILE':
                            current_parent.set_file(self.parse_prop(line_array)[1])  

    def get_metaprops(self, full_line):
        # Parse meta props. 
        # I tried combining this with parse_prop(), however the many sublte differences made it a nightmare.
        if len(full_line) == 1:
            return None
        else:
            prop_string = ''
            for i in range(len(full_line)):
                if i != 0:
                    prop_string += full_line[i].replace('\n', '')
                    if i != len(full_line) -1:
                        prop_string += ' '
            return prop_string

    def parse_prop(self, full_line):
        return_array = []
        prop_string = ''
        for i in range(len(full_line)):
            if i == 0:
                return_array.append(full_line[i])
            else:
                prop_string = prop_string + full_line[i].replace('\n', '')
                if i != len(full_line) -1:
                    prop_string = prop_string + ' '

        return_array.append(prop_string)
        return return_array

    def line_pre_parse(self, full_line):
        # Transform a line from an rpp file into an array without preceeding spaces.
        # For example: ['<REAPER_PROJECT', '0.1', '"6.51/OSX64"', '1646650836\n']
        initial_line_list = full_line.split(' ')
        removed_initial_spaces = []
        final_array = []
        can_push = False

        # Remove preceeding empty entries:
        for element in initial_line_list:
            if(can_push == False and element != ''):
                can_push = True
            if(can_push):
                removed_initial_spaces.append(element)

        # Stick strings back together:
        adding_string = False
        current_string = ''
        for element in removed_initial_spaces:
            if('"' in element): 
                last_char = element.replace('\n', '')[-1]
                if(element[0] == '"' and last_char == '"'):
                    final_array.append(element)
                elif(element[0] == '"'):
                    adding_string = True
                    current_string = element
                elif(adding_string == True and last_char == '"'):
                    current_string = current_string + ' ' + element
                    final_array.append(current_string)
                    adding_string = False
            elif(adding_string == True):
                current_string = current_string + ' ' + element
            else:
                final_array.append(element)

        return final_array

class FXChain(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        super().__init__(*nodes_to_add, **kwargs)
        self.name = 'FXCHAIN'

class VST(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        super().__init__(*nodes_to_add, **kwargs)
        self.name = 'VST'

class AU(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        super().__init__(*nodes_to_add, **kwargs)
        self.name = 'AU'
        

class Track(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        super().__init__(*nodes_to_add, **kwargs)
        self.name = 'TRACK'
        self.valid_children = [Node, FXChain, Item]
        

    def get_items(self, query):
        # Get track in project either by index or track name:
        super().get_children(type_query = Item)
        
class Item(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        super().__init__(*nodes_to_add, **kwargs)
        self.name = 'ITEM'
        self.valid_children = [Node, Source]

class Source(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        super().__init__(*nodes_to_add, **kwargs)
        self.valid_children = [Node, Source]
        self.name = 'SOURCE'
        self.extension_lookup = {
            '.wav' : 'WAVE',
            '.wave' : 'WAVE',
            '.aiff' : 'WAVE',
            '.aif' : 'WAVE',
            '.mp3' : 'MP3',
            '.ogg' : 'VORBIS'
        }
        # Only do the source parsing if it is given:
        if 'file' in kwargs:
            self.file = kwargs.get('file')      
            self.process_extension()

    def set_file(self, path):
        # Allow for setting of the file from elsewhere.
        self.file = path
        self.process_extension()

    def process_extension(self):
        ext = Path(self.file.replace('"', '')).suffix
        try:
            self.meta_props = self.extension_lookup[ext]
        except KeyError:
            self.meta_props = 'SECTION'