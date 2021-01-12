# from reapy.nodes import Session, Track, Item, Source
from reathon.nodes import *

tiger = Source(file='/Users/james/Downloads/Bengal_Tiger_aggresive_grunt_medium.wav')
session = Project()
session.add(
    Track(
        Item(
            tiger, length=15, position=4
        )
    )
)

session.write("foobar.rpp")