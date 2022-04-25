from reathon.nodes import *
from reathon.helper import make_color
from reathon.helper import marker
from reathon.helper import region

proj = Project(
    Track(isbus='1 1', trackheight='67'),
    Track(isbus='1 1', trackheight='67'),
    Track(isbus='2 -1', trackheight='30'),
    Track(isbus='1 1', trackheight='67'),
    Track(isbus='1 1', trackheight='67'),
    Track(isbus='2 -1', trackheight='30'),
)

proj.props.extend([
    marker(1, 0, 'first'),
    marker(2, 0.5, 'second', make_color(0, 255, 0))  # with custom color
])

# or

proj.add_marker(3, 1.0, 'third')

proj.write('markers.rpp')
