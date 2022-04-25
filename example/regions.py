from reathon.nodes import *
from reathon.helper import marker, region

proj = Project(Track())

proj.props.extend(region(0, 0.3, 9.8, "meregion"))

# OR

proj.add_region(1, 10, 20, "foofoo")

proj.write('regions.rpp')
