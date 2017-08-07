#!/usr/bin/python3
# pystronghold.py
"Simple script to triangulate a stronghold in minecraft."
import math


class WorldPoint:
    "A point in the world, with an angle relative to the grid pointing to the \
    closest stronghold"
    def __init__(self, pos, angle):
        self.pos = pos
        self.angle = angle

    def swap(self, other):
        "Swaps pos and angle with another WorldPoint"
        temp = WorldPoint(self.pos, self.angle)
        self.pos = other.pos
        self.angle = other.angle
        other.pos = temp.pos
        other.angle = temp.angle

    def absang(self):
        "Returns the absoulte angle (0°-360° instead of -180°-180°)"
        return self.angle if self.angle >= 0 else self.angle + 360

    def __repr__(self):
        return 'x: {}, z: {}  {}°'.format(*self.pos, self.angle)


def sortpoints(pointa, pointb):
    "If point a has a higher z value than point z, they're swapped"
    if pointa.pos[1] > pointb.pos[1]:
        pointa.swap(pointb)


def pythagoras(posa, posb):
    "Takes two tuples. Calculates the distance between two points (any number \
    of dimensions)."
    return math.sqrt(sum([math.pow(a - b, 2) for a, b in zip(posa, posb)]))


def findstronghold(pointa, pointb):
    "Find the stronghold, using math!"
    sortpoints(pointa, pointb)
    linec = pythagoras(pointa.pos, pointb.pos)
    alpha = abs(math.degrees(math.asin((pointb.pos[0]-pointa.pos[0]) / linec)))
    beta = 90 - alpha
    if pointa.pos[0] < pointb.pos[0]:
        anglea = (alpha + pointa.absang()) % 360
        angleb = abs(beta + 90 - pointb.absang())
    else:
        anglea = abs(alpha - pointa.absang())
        angleb = abs(180 + alpha - pointb.absang())
    anglea = 360 - anglea if anglea > 180 else anglea
    angleb = 360 - angleb if angleb > 180 else angleb
    anglec = 180 - anglea - angleb
    linea = (linec /
             math.sin(math.radians(anglec))) * math.sin(math.radians(anglea))
    tria = math.sin(math.radians(pointb.absang() % 90)) * linea
    trib = math.cos(math.radians(pointb.absang() % 90)) * linea
    if pointb.absang() // 90 == 0:
        return (pointb.pos[0] - tria, pointb.pos[1] + trib)
    elif pointb.absang() // 90 == 1:
        return (pointb.pos[0] - trib, pointb.pos[1] - tria)
    elif pointb.absang() // 90 == 2:
        return (pointb.pos[0] + tria, pointb.pos[1] - trib)
    elif pointb.absang() // 90 == 3:
        return (pointb.pos[0] + trib, pointb.pos[1] + tria)


def main():
    "Main function. Run if this is being executed as a script."
    pointa = WorldPoint((float(input("Point a, x: ")),
                         float(input("Point a, z: "))),
                        float(input("Point a, angle: ")))
    pointb = WorldPoint((float(input("Point b, x: ")),
                         float(input("Point b, z: "))),
                        float(input("Point b, angle: ")))
    print("x: {:.0f}, z: {:.0f}".format(*findstronghold(pointa, pointb)))


if __name__ == "__main__":
    main()
