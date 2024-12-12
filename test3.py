from dataclasses import dataclass


@dataclass
class Circle:
    r: int

@dataclass
class Rectangle:
    h: int
    w: int

def test(obj):
    a = pmatch obj:
        Circle(r): 2 * r
        Rectangle(h, w): h + w
        _: -1
    endpmatch

    return a

c = Circle(r=10)
test(c)
