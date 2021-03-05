from reathon.nodes import *
from reathon.helper import marker

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
    marker(2, 0.5, 'second')
])

proj.write('markers.rpp')

