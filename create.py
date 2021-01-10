from nodes import Session, Track, Item, Source

tiger = Source(file='/Users/james/Downloads/Bengal_Tiger_aggresive_grunt_medium.wav')
session = Session()

session.add(
    Track(
        Item(tiger, length=10, position=1)
    )
)

class Writer:
    def __init__(self):
        self.string = ''

    def traverse(self, origin):
        self.string += f'<{origin.name}\n'
        for k, v in origin.props.items():
                self.string += f'{k} {v}\n'
        for node in origin.nodes:
            self.traverse(node)
        self.string += '>\n'

    def write(self, path):
        with open(path, "w") as f:
            f.write(self.string)


writer = Writer()

writer.traverse(session)
writer.write("hello.rpp")


# session.add(
#     Track().add(
#         Item().add(
#             Source()
#         )
#     )
# )

