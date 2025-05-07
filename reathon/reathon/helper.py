# N.B. colors are passed as ints but should be created with this helper - pass 0 for the default colors


def make_color(r, g, b):
    return (1 << 24) + (r << 16) + (g << 8) + b


def marker(index: int, time: float, name: str, color: int = 0):
    return ["MARKER", f'{index} {time} "{name}" 0 {color} 1 B']


def region(index: int, start: float, end: float, name: str, color: int = 0):
    return [
        ["MARKER", f'{index} {start} "{name}" 1 {color} 1 B'],
        ["MARKER", f'{index} {end} ""  1 {color} 1 B'],
    ]
