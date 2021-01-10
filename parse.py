from rea import Session, Track, Node

session = Session()

with open("template.RPP") as f:
    current_node = session
    t = f.readlines()
    for x in t:
        x = x.replace("\n", "")
        x = x.lstrip()
        if "<" in x:
            x = x[1:]
            
        # if ">" in x:
            print(x, 'node end')