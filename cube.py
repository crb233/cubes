
#   0
# 1 2 3 4
#   5

# for each face, a list of adjacent faces and their relative orientations
orientations = [
    [(4,0), (3,0), (2,0), (1,0)],
    [(4,1), (0,3), (2,3), (5,3)],
    [(5,0), (1,1), (0,2), (3,3)],
    [(4,3), (5,1), (2,1), (0,1)],
    [(1,3), (5,2), (3,1), (0,0)],
    [(1,2), (2,2), (3,2), (4,2)],
]

def rotate(face, rot):
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
    def __init__(self, n):
        self.n = n
        self.reset()
    
    def __str__(self):
        res = ''
        for i in range(self.n):
            res += '      '
            for j in range(self.n):
                res += str(self.faces[0][i][j]) + ' '
            res += '\n'
        
        for i in range(self.n):
            for f in range(1,5):
                for j in range(self.n):
                    res += str(self.faces[f][i][j]) + ' '
            res += '\n'
        
        for i in range(self.n):
            res += '      '
            for j in range(self.n):
                res += str(self.faces[5][i][j]) + ' '
            res += '\n'
        
        return res[:-1]
    
    def reset(self):
        self.faces = [[[i for c in range(self.n)] for r in range(self.n)] for i in range(6)]
    
    def turn(self, face, x):
        ls = orientations[face]
        
        self.faces[face] = rotate(self.faces[face], x)
        edges = [get_rotated_edge(self.faces[f], r) for f, r in ls]
        for i in range(4):
            f, r = ls[(i + x) % 4]
            set_rotated_edge(self.faces[f], r, edges[i])
    
    def turns(self, ls):
        for face, x in ls:
            self.turn(face, x)
