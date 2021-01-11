from reapy.nodes import Session, Track, Item, Source
from pathlib import Path
import random

sources = []

for x in Path('/Users/james/Downloads/speakers-phones').rglob("*.wav"):
    sources.append(
        Source(
            file=f'{str(x)}'
        )
    )

track = Track()
session = Session().add(track)

pos = 0.0
for x in range(1000): #1000 grains
    grain = random.choice(sources) #random file
    
    length = random.uniform(0.1, 0.5)
    track.add(
        Item(
            grain,
            position = pos,
            length = length
        )
    )
    pos += length

session.write("gran.rpp")


