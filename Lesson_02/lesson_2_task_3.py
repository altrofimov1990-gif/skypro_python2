import math

def square(side):
    area = side * side
    if isinstance(side, int):
        return int(area)
    else:
        return math.ceil(area)