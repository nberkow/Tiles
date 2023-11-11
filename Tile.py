

class Vertex:
    def __init__(self, tile, x, y):
        self.tile = tile
        self.x = x
        self.y = y

    def __gt__(self, other_vertex):
        
        if self.x - self.tile.center.x >= 0 and other_vertex.x - self.tile.center.x < 0:
            return True
        if self.x - self.tile.center.x < 0 and other_vertex.x - self.tile.center.x >= 0:
            return False
        if self.x - self.tile.center.x == 0 and other_vertex.x - self.tile.center.x == 0:
            if self.y - self.tile.center.y >= 0 or other_vertex.y - self.tile.center.y >= 0:
                return self.y > other_vertex.y
            return other_vertex.y > self.y

        # compute the cross product of vectors (center -> a) x (center -> b)
        det = (self.x - self.tile.center.x) * (other_vertex.y - self.tile.center.y) - (other_vertex.x - self.tile.center.x) * (self.y - self.tile.center.y)
        if det < 0:
            return True
        if det > 0:
            return False

        # points a and b are on the same line from the center
        # check which point is closer to the center
        d1 = (self.x - self.tile.center.x) * (self.x - self.tile.center.x) + \
             (self.y - self.tile.center.y) * (self.y - self.tile.center.y)
        d2 = (other_vertex.x - self.tile.center.x) * (other_vertex.x - self.tile.center.x) + \
             (other_vertex.y - self.tile.center.y) * (other_vertex.y - self.tile.center.y)
        return d1 > d2
    
    def __str__(self):
        return f"{self.x},{self.y}"


class Tile:
    def __init__(self, vertices):
        self.vertices = []
        cx, cy = 0, 0
        for v in vertices:
            self.vertices.append(Vertex(self, v[0], v[1]))
            cx += v[0]/len(vertices)
            cy += v[1]/len(vertices)
        self.center = Vertex(self, cx, cy)

    def to_svg(self):
        path =  '<path d="{} Z" fill="transparent" stroke="black"/>'
        moves = f"M {self.vertices[0].x} {self.vertices[0].y}"
        for vertex in self.vertices[1:]:
            moves += f" L {vertex.x} {vertex.y}"
        return(path.format(moves))
    
    def sort_vertices(self):
        self.vertices.sort()


if __name__ == "__main__":

    t = Tile([(20,10),(10,10),(20,20),(10,20)])
    t.sort_vertices()

    for v in t.vertices:
        print(v)


    with open('header.txt') as header, open('footer.txt') as footer, open("tiles.svg", 'w') as out_svg:
        print(header.read(), file=out_svg)
        print(t.to_svg(),    file=out_svg)
        print(footer.read(), file=out_svg)

    


