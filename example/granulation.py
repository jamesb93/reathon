from pyper.nodes import Project, Track, Item, Source # note new nodes Item() and Source()
from pathlib import Path
import random

sources = []

# create a source object for each of the .wav files in a directory (can you tell I love comprehensions)
sources = [
    Source(file=f'{str(x)}')
    for x in Path('/Users/james/Cloud/Projects/ElectroMagnetic/outputs/segments/2_ExplodeAudio').rglob("*.wav")
]

track = Track() # create a blank Track()

pos = 0.0 # set our initial position to 0
for x in range(1000): # 1000 grains
    grain = random.choice(sources) # random file from our sources
    
    length = random.uniform(0.001, 0.03) # random length of the item
    track.add(
        Item(
            grain, # Item()'s have a child Source() node, which is randomly selected above
            position = pos, # and we set the position
            length = length # and we set the length
        )
    )
    pos += length # increment the position by the length to create contiguous blocks

project = Project(track) # create the project with our composed track
project.write("granular.rpp") # write it out