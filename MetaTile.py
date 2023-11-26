
from Hat import Hat

class Metatile:
    def __init__(self, graph, orientation):

        # pos zero is top-right edge when orientation == 0
        self.edge_connections = [[],[],[],[],[],[]]
        self.orientation = 0
        pass

    def to_cluster(self):
        pass

    def to_tiles(self, tri_coord):
        pass

class TriangleMetatile(Metatile):
    def __init__(self, graph, orientation):

        self.edge_connections = [[],[],[],[],[],[]]
        self.orientation = orientation
        self.cluster_nodes = []
        self.cluster_connections = []
        self.graph = graph
        self.type = 'T'

    def to_cluster(self):
        pass

    def to_tiles(self, tri_coord):
        a, b, c = tri_coord

        # tiles from top right
        
        tiles = [
            Hat(self.graph.side_len, (self.orientation + 2) % 3, 1, -1, (a, b, c))
        ]
        
        return tiles
    
class TrigonalHexMetatile(Metatile):
    def __init__(self, graph, orientation):

        self.edge_connections = [[],[],[],[],[],[]]
        self.orientation = orientation
        self.graph = graph
        self.type = 'H'
        pass

    def to_cluster(self):
        t0 = TriangleMetatile(1)
        
        h0 = TrigonalHexMetatile(2)
        h1 = TrigonalHexMetatile(0)
        h2 = TrigonalHexMetatile(0)

        t0.edge_connections = [[h0], [], [h1], [], [h2], []]

        r0 = RhombusMetatile(1)
        r1 = RhombusMetatile(0)
        r2 = RhombusMetatile(5)

        a0 = ArrowMetatile(4)
        a1 = ArrowMetatile(2)
        a2 = ArrowMetatile(0)
        a3 = ArrowMetatile(4)
        a4 = ArrowMetatile(2)
        a5 = ArrowMetatile(0)

        h0.edge_connections = [[a2],[r1],[h1, t0],[h2],[r0],[a1]]
        h1.edge_connections = [[h2,t0],[h0],[r1],[a3],[a4],[r2]]
        h2.edge_connections = [[a0],[r0],[h0,t0],[h1],[r2],[a5]]

        r0.edge_connections = [[a1], [], [h0], [h2,a0], [], []]
        r1.edge_connections = [[h0,a2], [], [], [a3], [], [h1]]
        r2.edge_connections = [[h1,a4],[], [], [a5], [], [h0]]

        a0.edge_connections = [[a5],[],[],[r0],[],[h2]]
        a1.edge_connections = [[],[a2],[h0,r0],[],[],[]]
        a2.edge_connections = [[a1],[],[],[r1],[],[h0]]
        a3.edge_connections = [[],[a4],[h1,r1],[],[],[]]
        a4.edge_connections = [[a3],[],[],[r2],[],[h1]]
        a5.edge_connections = [[],[a0],[h2,r2],[],[],[]]

        self.cluster_nodes = [t0, h0, h1, h2, r0, r1, r2, a0, a1, a2, a3, a4, a5]
        self.cluster_edge_tiles = [[a0, r0, a1], [a1], [a2, r1, a3], [a2], [a4, r2, a5], [a5]]

    def to_tiles(self, tri_coord):

        ori_shift_1 = [0,0,1]
        ori_shift_2 = [-1,0,1]
        ori_shift_3 = [-1,0,0]

        a, b, c = tri_coord

        # tiles from top right
 
        tiles = [
            Hat(self.graph.side_len, (self.orientation + 2) % 3, 1, -1, (a, b, c)),
            Hat(self.graph.side_len, (self.orientation) % 3, 1, -1, (
                a + ori_shift_1[self.orientation], 
                b + ori_shift_1[(self.orientation + 2) % 3], 
                c + ori_shift_1[(self.orientation + 1) % 3])),
            Hat(self.graph.side_len, (self.orientation + 2) % 3, 1, -1, (
                a + ori_shift_2[self.orientation], 
                b + ori_shift_2[(self.orientation + 2) % 3], 
                c + ori_shift_2[(self.orientation + 1) % 3])),
            Hat(self.graph.side_len, (3 - self.orientation + 1) % 3, -1, 1, (
                a + ori_shift_3[(self.orientation) % 3], 
                b + ori_shift_3[(self.orientation + 2) % 3], 
                c + ori_shift_3[(self.orientation + 1) % 3])),
        ]
        
        return tiles

class RhombusMetatile(Metatile):
    def __init__(self, graph, orientation):

        self.edge_connections = [[],[],[],[],[],[]]
        self.orientation = orientation
        self.type = 'R'
        self.graph = graph

    def to_cluster(self):
        pass

    def to_tiles(self, tri_coord):
        a, b, c = tri_coord

        ori_shift = [0,1,0]

        # tiles from top right
        
        tiles = [
            Hat(self.graph.side_len, (self.orientation + 2) % 3, 1, -1, (a, b, c)), # focal tile = metatile focal tile
            Hat(self.graph.side_len, (self.orientation + 1) % 3, 1, 1, (
                    a + ori_shift[self.orientation],
                    b + ori_shift[(self.orientation + 2) % 3],
                    c + ori_shift[(self.orientation + 1) % 3] ))
        ]
        
        return tiles

class ArrowMetatile(Metatile):
    def __init__(self, graph, orientation):

        self.graph = graph
        self.edge_connections = [[],[],[],[],[],[]]
        self.orientation = orientation
        self.type = 'A'

    def to_cluster(self):
        pass

    def to_tiles(self, tri_coord):

        a, b, c = tri_coord

        ori_shift = [0,1,0]

        # tiles from top right
        
        tiles = [
            Hat(self.graph.side_len, self.orientation, 1, -1, (a, b, c)), # focal tile = metatile focal tile
            Hat(self.graph.side_len, self.orientation, 1, 1, (
                    a + ori_shift[self.orientation],
                    b + ori_shift[(self.orientation + 2) % 3],
                    c + ori_shift[(self.orientation + 1) % 3] ))
        ]

        return tiles

class MetatileGraph:

    def __init__(self, side_len):
        self.side_len = side_len
        self.tiles = []

if __name__ == "__main__":

    g = MetatileGraph(10)

    col = ["cyan", "blue", "pink", "red", "green", "blue",]

    with open('header.txt') as header, open('footer.txt') as footer, open("tiles.svg", 'w') as out_svg:
        print(header.read(), file=out_svg)

        metatiles = []
        
        

        print(footer.read(), file=out_svg)


