
# Face numbers are assigned as follows:
#   0
# 1 2 3 4
#   5

opposites = [5, 3, 4, 1, 2, 0]

# contains lists of data values for use in turning each side
turns = [
    [(4,0), (3,0), (2,0), (1,0)],
    [(4,1), (0,3), (2,3), (5,3)],
    [(5,0), (1,1), (0,2), (3,3)],
    [(4,3), (5,1), (2,1), (0,1)],
    [(1,3), (5,2), (3,1), (0,0)],
    [(1,2), (2,2), (3,2), (4,2)],
]

# contains lists of data values for use in rotating around each side
rotations = [
    [(0,1), (2,0), (3,0), (4,0), (1,0), (5,3)],
    [(4,2), (1,1), (0,0), (3,3), (5,2), (2,0)],
    [(1,1), (5,1), (2,1), (0,1), (4,3), (3,1)],
    [(2,0), (1,3), (5,0), (3,1), (0,2), (4,2)],
    [(3,3), (0,3), (2,3), (5,3), (4,1), (1,3)],
    [(0,3), (4,0), (1,0), (2,0), (3,0), (5,1)],
]

def rotate_face(face, rot):
    n = len(face)
    m = n - 1
    
    if rot == 0:
        return [[face[r][c] for c in range(n)] for r in range(n)]
    elif rot == 1:
        return [[face[m - c][r] for c in range(n)] for r in range(n)]
    elif rot == 2:
        return [[face[m - r][m - c] for c in range(n)] for r in range(n)]
    else:
        return [[face[c][m - r] for c in range(n)] for r in range(n)]

def get_rotated_edge(face, rot):
    n = len(face)
    m = n - 1
    
    if rot == 0:
        return [face[0][c] for c in range(n)]
    elif rot == 1:
        return [face[c][m] for c in range(n)]
    elif rot == 2:
        return [face[m][m - c] for c in range(n)]
    else:
        return [face[m - c][0] for c in range(n)]

def set_rotated_edge(face, rot, vals):
    n = len(face)
    m = n - 1
    
    if rot == 0:
        for c in range(n):
            face[0][c] = vals[c]
    elif rot == 1:
        for c in range(n):
            face[c][m] = vals[c]
    elif rot == 2:
        for c in range(n):
            face[m][m - c] = vals[c]
    else:
        for c in range(n):
            face[m - c][0] = vals[c]

class Cube:
    def __init__(self, n=3, colors=False):
        self.n = n
        if colors:
            # TODO use the colorama library for colors
            self.labels = ['  ','  ','  ','  ','  ','  ']
        else:
            self.labels = ['0 ','1 ','2 ','3 ','4 ','5 ']
        self.reset()
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        res = ''
        for i in range(self.n):
            res += '      '
            for j in range(self.n):
                res += self.labels[self.faces[0][i][j]]
            res += '\n'
        
        for i in range(self.n):
            for f in range(1,5):
                for j in range(self.n):
                    res += self.labels[self.faces[f][i][j]]
            res += '\n'
        
        for i in range(self.n):
            res += '      '
            for j in range(self.n):
                res += self.labels[self.faces[5][i][j]]
            res += '\n'
        
        return res[:-1]
    
    def reset(self):
        self.faces = [[[i for c in range(self.n)] for r in range(self.n)] for i in range(6)]
    
    def turn(self, face, x=1):
        ls = turns[face]
        
        self.faces[face] = rotate_face(self.faces[face], x % 4)
        edges = [get_rotated_edge(self.faces[f], r) for f, r in ls]
        for i in range(4):
            f, r = ls[(i + x) % 4]
            set_rotated_edge(self.faces[f], r, edges[i])
    
    def rotate(self, face, x=1):
        x = x % 4
        if x == 3:
            face = opposites[face]
        ls = rotations[face]
        for i in range(x):
            self.faces = [rotate_face(self.faces[f], r) for f, r in ls]
