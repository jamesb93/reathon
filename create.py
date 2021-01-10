from nodes import Session, Track, Item, Source

tiger = Source(file='/Users/james/Downloads/Bengal_Tiger_aggresive_grunt_medium.wav')
section = Source()
session = Session()
item = Item()
session.add(
    Track(
        Item(
            tiger, length=15, position=4
        )
    )
)

session.write("foobar.rpp")