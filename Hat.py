

class Hat:

    def __init__(self, side_len, orientation, parity, triangle_type, abs_grid_coords):

        self.side_len = side_len
        self.orientation = orientation % 3
        self.parity = parity
        self.halfturn = triangle_type
        self.abs_grid_coords = abs_grid_coords

        # internal coords

        if (triangle_type > 0):
            self.vertices = [
            
                [0,0,0],
                self.midpoint(( [0,0,0], [1,0,0] )),
                self.midpoint(( [0,0,0], [1,0,0], [0,0,-1] )),
                self.midpoint(( [self.halfturn,0,0], [0,0,-1] )),
                [0,0,-1],
                self.midpoint(( [0,1,0], [0,0,-1] )),
                self.midpoint(( [0,1,0], [0,0,-1], [0,1,-1] )),
                self.midpoint(( [0,1,0], [0,1,-1] )),
                [0,1,0],
                self.midpoint(( [0,1,0], [0,0,0] )),
                self.midpoint(( [-1,0,0], [0,1,0], [0,0,0] )),
                self.midpoint(( [-1,0,0], [0,0,0], [0,0,1] )),
                self.midpoint(( [0,0,0], [0,0,1] ))
            ]

        else:
            self.vertices = [           
                [0,0,0],
                self.midpoint(([0,0,0],[0,-1,0])),
                self.midpoint(([0,0,0],[0,-1,0], [1,0,0])),
                self.midpoint(([0,-1,0], [1,0,0])),
                [1,0,0],
                self.midpoint(( [1,0,0], [0,0,-1])),
                self.midpoint(( [1,0,0], [0,0,-1], [1,0,-1])),
                self.midpoint(( [0,0,-1], [1,0,-1])),
                [0,0,-1],
                self.midpoint(([0,0,0], [0,0,-1])),
                self.midpoint(([0,0,0], [0,0,-1], [0,1,0])),
                self.midpoint(([0,0,0], [-1,0,0], [0,1,0])),
                self.midpoint(([0,0,0], [-1,0,0])),
            ]


    def midpoint(self, points):

        midpoint = [0, 0, 0]
        
        for p in points:
            midpoint[0] += p[0]/len(points)
            midpoint[1] += p[1]/len(points)
            midpoint[2] += p[2]/len(points)

        return(midpoint)
    
    def to_svg_block(self, stroke, fill):

        abs_x, abs_y = self.triangular_to_cartesian(self.abs_grid_coords, 0)
        path =  '<path d="{} Z" fill="{}" stroke="{}"/>'
        moves = f"M {abs_x} {abs_y}"
        for vertex in self.vertices[1:]:
            rel_x, rel_y = self.triangular_to_cartesian(vertex, self.orientation)
            moves += f"L {rel_x * self.parity + abs_x} {rel_y + abs_y}"
        return(path.format(moves, fill, stroke))

    def triangular_to_cartesian(self, coord, local_orientation):

        a, b, c = coord

        xy_cooef = [
            [self.side_len * (3**0.5)/2, -self.side_len/2],
            [0, self.side_len],
            [-self.side_len * (3**0.5)/2, -self.side_len/2],
        ]

        coords = [
            a * xy_cooef[local_orientation][0] + b * xy_cooef[(local_orientation + 1) % 3][0] + c * xy_cooef[(local_orientation + 2) % 3][0],
            a * xy_cooef[local_orientation][1] + b * xy_cooef[(local_orientation + 1) % 3][1] + c * xy_cooef[(local_orientation + 2) % 3][1],
        ]
        return(coords)
    

if __name__ == "__main__":

    tile = Hat(100,0,-1,(10,10,-10))
    tile2 = Hat(100,1,1,(10,10,-10))
    tile3 = Hat(100,2,1,(10,10,-10))

    with open('header.txt') as header, open('footer.txt') as footer, open("tiles.svg", 'w') as out_svg:
        print(header.read(), file=out_svg)
        print(tile.to_svg_block("green", 'transparent'), file=out_svg)
        print(tile2.to_svg_block("cyan", 'transparent'), file=out_svg)
        print(tile3.to_svg_block("blue", 'transparent'), file=out_svg)
        print(footer.read(), file=out_svg)
        


