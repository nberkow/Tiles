

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
        self.fill = "transparent"
        cx, cy = 0, 0
        for v in vertices:
            self.vertices.append(Vertex(self, v[0], v[1]))
            cx += v[0]/len(vertices)
            cy += v[1]/len(vertices)
        self.center = Vertex(self, cx, cy)
        self.sort_vertices()

    def to_svg(self, fill="transparent", stroke="black"):
        path =  '<path d="{} Z" fill="{}" stroke="{}"/>'
        moves = f"M {self.vertices[0].x} {self.vertices[0].y}"
        for vertex in self.vertices[1:]:
            moves += f" L {vertex.x} {vertex.y}"
        return(path.format(moves, fill, stroke))
    
    def sort_vertices(self):
        self.vertices.sort()


class KiteGrid:

    def __init__(self, rows, cols, triangle_side_len):

        self.triangle_side_len = triangle_side_len
        self.triangle_height = 3**0.5/2 * triangle_side_len
        parity = 1
        self.triangle_grid = []
        self.kite_grid = []
        
        for row in range(rows):
            row_triangles = []
            row_kitesets = []
            for col in range(cols):
                triangle_east = Tile([ (col * self.triangle_height * 2 + (1 - parity) * self.triangle_height, 
                                        row * triangle_side_len/2),
                                       (col * self.triangle_height * 2 + self.triangle_height + (1 - parity) * self.triangle_height, 
                                        row * triangle_side_len/2 + triangle_side_len/2),
                                       (col * self.triangle_height * 2 + (1 - parity) * self.triangle_height, 
                                        row * triangle_side_len/2 + triangle_side_len)])
                kites_east = self.triangle_to_kites(triangle_east, False)
                
                triangle_west = Tile([ (col * self.triangle_height * 2 + self.triangle_height + parity * self.triangle_height, 
                                        row * triangle_side_len/2),
                                       (col * self.triangle_height * 2 + parity * self.triangle_height, 
                                        row * triangle_side_len/2 + triangle_side_len/2),
                                       (col * self.triangle_height * 2 + self.triangle_height + parity * self.triangle_height, 
                                        row * triangle_side_len/2 + triangle_side_len)])
                kites_west = self.triangle_to_kites(triangle_west, True)
                
                if parity:
                    row_triangles += [triangle_east, triangle_west]
                    row_kitesets += [kites_east, kites_west]
                else:
                    row_triangles += [triangle_west, triangle_east]
                    row_kitesets += [kites_west, kites_east] 

            self.triangle_grid.append(row_triangles)                
            self.kite_grid.append(row_kitesets)
            parity = (parity + 1) % 2

    def write_kite_grid(self, out_svg):
        j = 0

        for r in self.kite_grid:
            for c in r:
                for kite in c:
                    print(kite.to_svg(fill=kite.fill), file=out_svg)
                    j = (j+1) % 3


    def write_triangle_grid(self, out_svg):

        for r in self.triangle_grid:
            for triangle in r:
                print(triangle.to_svg(), file=out_svg)
                

    def triangle_to_kites(self, triangle_tile, flip_rotation):

        kites = []
        k_num = [0,1,2]
        if flip_rotation:
            k_num.reverse()        

        for v in k_num:
            vertex = triangle_tile.vertices[v]
            midpoint_a = ((vertex.x + triangle_tile.vertices[(v + 1) % 3].x)/2,
                          (vertex.y + triangle_tile.vertices[(v + 1) % 3].y)/2)
            midpoint_b = ((vertex.x + triangle_tile.vertices[(v + 2) % 3].x)/2,
                          (vertex.y + triangle_tile.vertices[(v + 2) % 3].y)/2)
            kite = Tile([(vertex.x, vertex.y), midpoint_a, midpoint_b, (triangle_tile.center.x, triangle_tile.center.y)])
            kites.append(kite)
        return(kites)

    
    def place_tile(self, triangle_grid_coord, chirality, orientation, color):
        
        t_row = triangle_grid_coord[0]
        t_col = triangle_grid_coord[1]

        row_parity = t_row % 2
        col_parity = t_col % 2
        parity_shift = 1

        if (row_parity + col_parity) % 2 == 0:
            parity_shift = -1
        
        triangle_kites = self.kite_grid[t_row][t_col]
        for tk in triangle_kites:
            tk.fill = color

        top_triangle = self.kite_grid[t_row-1][t_col]
        bottom_triangle = self.kite_grid[t_row+1][t_col]
        side_triangle = self.kite_grid[t_row][t_col + parity_shift]

        adjacent_triangles = [top_triangle, bottom_triangle, side_triangle]
        tip_triangle_options = [
            self.kite_grid[t_row - 1][t_col + parity_shift],
            self.kite_grid[t_row - 1][t_col - parity_shift],
            self.kite_grid[t_row + 2][t_col]]
            
        if chirality == -1:
            adjacent_triangles.reverse()
            tip_triangle_options.reverse()
        
        tip_triangle = tip_triangle_options[orientation]

        tip_triangle[(orientation + 2) % 3].fill = color

        rot = [2,1,0]
        adjacent_triangles[orientation][rot[(orientation + 1 + chirality) % 3]].fill = 'red'
        adjacent_triangles[orientation][rot[(orientation + 2 + chirality) % 3]].fill = 'cyan'
        adjacent_triangles[((orientation+1) % 3)][rot[(orientation) % 3]].fill = 'blue'
        adjacent_triangles[((orientation+2) % 3)][rot[(orientation + 1) % 3]].fill = 'purple'


if __name__ == "__main__":

    grid = KiteGrid(20,20,100)
    orientation = 0
    chirality = -1
    grid.place_tile((3,2), chirality, orientation, 'green')
    grid.place_tile((3,5), chirality, orientation, 'green')
    grid.place_tile((10,2), chirality, orientation, 'green')
    grid.place_tile((10,5), chirality, orientation, 'green')

    with open('header.txt') as header, open('footer.txt') as footer, open("tiles.svg", 'w') as out_svg:
        print(header.read(), file=out_svg)
        grid.write_kite_grid(out_svg)
        print(footer.read(), file=out_svg)
        

            


            

    




