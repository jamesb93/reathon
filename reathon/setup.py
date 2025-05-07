from setuptools import setup, find_packages

long_description = """
# reathon

`reathon` is a python package for constructing REAPER session with native python constructs. The majority of the interface is a reflection of the `.rpp` file structure which itself is very similar to `.xml` with tags and elements (except each element is called a 'chunk'). As such, you may need to know a bit about the underlying structure of REAPER's file format before using something like this. A good way to do this is to make a REAPER project and open the project in a text editor. You might also refer to [this document](https://github.com/ReaTeam/Doc/blob/master/State%20Chunk%20Definitions) which is fairly exhaustive.

## installation

You can `git clone` this repo, `cd` to it and then install via `pip install -e reathon`. You need to point `pip` to the folder containing setup.py, not the parent folder with examples and README.md etc.

You can also `pip install reathon`.

## usage

`reathon` exposes objects for each type of 'chunk' or as I've called it **node** in the graph of objects in a session. A very simple example of a REAPER project with a single track would go as follows.

```python
from reathon.nodes import * # import all of the reathon nodes

project = Project( # create an instance of a project
    Track() # and pass a Track() object to the constructor
)

project.write("basic.rpp") # write the project out to the path
```

We can construct such graphs in a variety of ways which lends `reathon` towards programmatic constructions of projects.

```python
# Using Loops
from reathon.nodes import *

project = Project() # create an instance of a project

for x in range(1024):
    project.add(Track()) # use the add method of the project to add a Track()

project.write("loops.rpp") # write the project out to the path
```

```python
# Comprehensions
from reathon.nodes import *
tracks = [Track() for x in range(100)]
project = Project(*tracks)
project.write("comprehensions.rpp") # write the project out to the path
```

A more complex example might be to arrange a series of sound files randomly along a single track, similar to a granular synthesiser. This example presents new `reathon` nodes you won't have seen before

```python
from reathon.nodes import Project, Track, Item, Source # note new nodes Item() and Source()
from pathlib import Path
import random

sources = []

# create a source object for each of the .wav files in a directory (can you tell I love comprehensions)
sources = [
    Source(file=f'{str(x)}')
    for x in Path('my-sounds').rglob("*.wav") # you would point it to an actual folder of sounds, not just 'my-sounds'
]

track = Track() # create a blank Track()

pos = 0.0 # set our initial position to 0
for x in range(1000): # 1000 grains
    grain = random.choice(sources) # random file from our sources
    
    length = random.uniform(0.1, 0.5) # random length of the item
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
```

### props
In the `.rpp` structure each 'chunk' can have various properties. For example, the `ITEM` chunk will have length and position properties that determine where in the timeline the item is positioned and the duration of the item. I don't want to implement functions for each of these so there are ways to insert arbitrary properties for each 'chunk', or what you are now familiar with as a `reathon` 'node'.

```python
# modifiying properties with function arguments
from reathon.nodes import *
item = Item(
    length = 10, 
    position = 0.5
) # create a blank item 10 seconds in length a 0.5 seconds in the timeline
# the convention is you match the word of the property as lower case.
# if the property in the file is LENGTH, then the function argument is 'length'
track = Track(item)
project = Project(track)
project.write("properties1.rpp") # write the project out to the path
```

```python
# modifiying properties by directly modifying the .props of the object
from reathon.nodes import *
item = Item() # create a blank item 10 seconds in length a 0.5 seconds in the timeline
item.props = [
    ["LENGTH", 10],
    ["POSITION", 0.5]
]
track = Track(item)
project = Project(track)
project.write("properties1.rpp") # write the project out to the path
```
"""
setup(
    name="reathon",
    version="0.0.8",
    author="James Bradbury",
    url="https://github.com/jamesb93/reathon",
    license="GLPv3+",
    author_email="jamesbradbury93@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Construct REAPER projects in Python.",
    packages=find_packages()
)
