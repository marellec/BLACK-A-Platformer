
from vectormath import Vector2 # type: ignore


def str_Vector2(vector: Vector2):
    x = str(vector.x)
    y = str(vector.y)
    x = x if (len(x) >= 2 and x[-2:] != ".0") else x[:-2]
    y = y if (len(y) >= 2 and y[-2:] != ".0") else y[:-2]
    return f"< {x}, {y} >"