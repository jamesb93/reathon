from pathlib import Path
from reathon.exceptions import InvalidNodeMethod

class Node:
    def __init__(self, *nodes_to_add, **kwargs):
        self.nodes = []
        self.props = []
        self.parents = []
        self.string = ''
        self.add(*nodes_to_add)
        for prop, value in kwargs.items():
            if prop == 'file':
                value = self.wrap_file(value)
            self.props.append([prop.upper(), str(value)])

    def __repr__(self):
        return "Node()"

    def __str__(self):
        self.traverse(self)
        return self.string


    def add(self, *nodes_to_add):
        for node in nodes_to_add:
            if isinstance(node, self.valid_children):
                self.nodes.append(node)
                node.parents.append(self) # add the self to the parents of the node
            else:
                print(f'You cannot add a {node.name} to a {self.name}')
        return self

    def get_child(self, query):
        # Get child by index or propriety 'NAME':
        try:
            query = int(query)
            if query < len(self.nodes):
                return self.nodes[query]
            else:
                return None
        except ValueError:
            to_return = None
            for i in range(len(self.nodes)):
                for j in range(len(self.nodes[i].props)):
                    if self.nodes[i].props[j][0].upper() == 'NAME' and self.nodes[i].props[j][1] == query:
                        to_return = self.nodes[i]
            return to_return

    def traverse(self, origin):
        self.string += f'<{origin.name}\n'

        for state in origin.props:
            self.string += f'{state[0]} {state[1]}\n'
    
        for node in origin.nodes:
            self.traverse(node)
        self.string += '>\n'

    @staticmethod
    def wrap_file(path_to_wrap: str) -> str:
        return f"'{path_to_wrap}'"


class Project(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        self.name = 'REAPER_PROJECT'
        self.valid_children = Track
        super().__init__(*nodes_to_add, **kwargs)
        self.accepted_chunks = {
            # Used for reading, these are the only chunks that will be included.
            # Each included chunk must have a corresponding class that it will be created as.
            'PROJECT' : Project,
            'TRACK' : Track,
            'ITEM' : Item,
            'SOURCE' : Source
        } 
        if 'file' in kwargs:
            self.read(kwargs.get('file')) # If an rpp file is given, read it.

    def write(self, path):
        self.traverse(self)
        with open(path, "w") as f:
            f.write(self.string)

    def get_track(self, query):
        # Get track in project either by index or track name:
        return super().get_child(query)

    def read(self, path):
        # Read an rpp file
        self.nodes = [] # Reinit nodes.
        self.props = [] # Reinit props.

        current_parent = self 
        current_hierarchy = [self]
        with open(path, 'r') as f:
            for line in f:
                # Read through the lines in the rpp file:
                line_array = self.line_pre_parse(line)
                if (line_array[0][:1] == '>'):
                    # Finalise object
                    current_hierarchy.pop()
                    current_parent = current_hierarchy[-1]
                else:
                    if(line_array[0][:1] == '<'):
                        # New Object start
                        this_chunk = line_array[0][1:].replace('\n', '')
                        
                        if(this_chunk in self.accepted_chunks):
                            accepted_chunk = self.accepted_chunks[this_chunk]()
                            current_parent.add(accepted_chunk)
                            current_parent = accepted_chunk
                            current_hierarchy.append(current_parent)
                        else:
                            current_hierarchy.append(current_parent)
                    else:
                        # Add property to current obj:
                        for allowed in self.accepted_chunks:
                            if isinstance(current_parent, self.accepted_chunks[allowed]):
                                current_parent.props.append(self.parse_prop(line_array))
                            if isinstance(current_parent, Source) and self.parse_prop(line_array)[0] == 'FILE':
                                current_parent.set_file(self.parse_prop(line_array)[1])     
            
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
        for i in range(len(initial_line_list)):
            if(can_push == False and initial_line_list[i] != ''):
                can_push = True
            if(can_push):
                removed_initial_spaces.append(initial_line_list[i])

        # Stick strings back together:
        adding_string = False
        current_string = ''
        for i in range(len(removed_initial_spaces)):
            if('"' in removed_initial_spaces[i]): 
                last_char = removed_initial_spaces[i].replace('\n', '')[-1]
                if(removed_initial_spaces[i][0] == '"' and last_char == '"'):
                    final_array.append(removed_initial_spaces[i])
                elif(removed_initial_spaces[i][0] == '"'):
                    adding_string = True
                    current_string = removed_initial_spaces[i]
                elif(adding_string == True and last_char == '"'):
                    current_string = current_string + ' ' + removed_initial_spaces[i]
                    final_array.append(current_string)
                    adding_string = False
            elif(adding_string == True):
                current_string = current_string + ' ' + removed_initial_spaces[i]
            else:
                final_array.append(removed_initial_spaces[i])

        return final_array

class Track(Node):
    def __init__(self, *nodes_to_add, **kwargs):
        self.name = 'TRACK'
        self.valid_children = Item
        super().__init__(*nodes_to_add, **kwargs)

    def get_item(self, query):
        # Get track in project either by index or track name:
        return super().get_child(query)
        
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
        # Only do the source parsing if it is given:
        if 'file' in kwargs:
            self.file = kwargs.get('file')
            self.process_extension()
        else:
            self.name = 'SOURCE'
        super().__init__(*nodes_to_add, **kwargs)

    def set_file(self, path):
        # Allow for setting of the file from elsewhere.
        self.file = path
        self.process_extension()

    def process_extension(self):
        ext = Path(self.file.replace('"', '')).suffix
        try:
            self.name = f'SOURCE {self.extension_lookup[ext]}'
        except KeyError:
            self.name = 'SOURCE SECTION'