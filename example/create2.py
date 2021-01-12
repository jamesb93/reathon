from reathon.nodes import *
tracks = [Track() for x in range(100)]
session = Project(*tracks)
session.write("foobar.rpp")