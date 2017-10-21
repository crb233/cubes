
# get terminal colors!
import colorama
from colorama import Fore, Back, Style
colorama.init()


# Face numbers are assigned as follows:
#   0
# 1 2 3 4
#   5

# lists the opposite of each face
# OPPOSITES[0] = 5
OPPOSITES = [5, 3, 4, 1, 2, 0]

# pairs of adjacent faces and relative orientations with respect to another face
ROTATIONS = [
    [(4,0), (3,0), (2,0), (1,0)],
    [(4,3), (0,1), (2,1), (5,1)],
    [(5,0), (1,3), (0,2), (3,1)],
    [(4,1), (5,3), (2,3), (0,3)],
    [(1,1), (5,2), (3,3), (0,0)],
    [(1,2), (2,2), (3,2), (4,2)],
]

# for parsing moves
SIDES = {'U': 0, 'T': 0, 'L': 1, 'F': 2, 'R': 3, 'B': 4, 'D': 5}
AMOUNTS = {'1': 1, '2': 2, '3': 3, 'I': 3, '\'': 3, '*': 3}

def parse_move(string):
    string = string.upper()
    if len(string) == 1 and string[0] in SIDES:
        return SIDES[string[0]], 1
    if len(string) == 2 and string[0] in SIDES and string[1] in AMOUNTS:
        return SIDES[string[0]], AMOUNTS[string[1]]
    return None

def rotate_face(face, x):
    '''Returns a copy of the face with 'x' clockwise rotations.'''
    
    x = x % 4
    n = len(face)
    m = n - 1
    
    if x == 0:
        return [[face[r][c] for c in range(n)] for r in range(n)]
    elif x == 1:
        return [[face[m - c][r] for c in range(n)] for r in range(n)]
    elif x == 2:
        return [[face[m - r][m - c] for c in range(n)] for r in range(n)]
    else:
        return [[face[c][m - r] for c in range(n)] for r in range(n)]

def get_edge(face, x):
    '''Returns the colors on the edge corresponding to the top edge after the
    face executes 'x' clockwise rotations.'''
    
    x = x % 4
    n = len(face)
    m = n - 1
    
    if x == 0:
        return [face[0][c] for c in range(n)]
    elif x == 1:
        return [face[m - c][0] for c in range(n)]
    elif x == 2:
        return [face[m][m - c] for c in range(n)]
    else:
        return [face[c][m] for c in range(n)]

def set_edge(face, x, vals):
    '''Sets the colors on the edge corresponding to the top edge after the face
    executes 'x' clockwise rotations.'''
    
    x = x % 4
    n = len(face)
    m = n - 1
    
    if x == 0:
        for c in range(n):
            face[0][c] = vals[c]
    elif x == 1:
        for c in range(n):
            face[m - c][0] = vals[c]
    elif x == 2:
        for c in range(n):
            face[m][m - c] = vals[c]
    else:
        for c in range(n):
            face[c][m] = vals[c]


class Cube:
    '''Represents a 3-dimensional n by n Rubik's cube'''
    
    color_labels = [
        Back.LIGHTWHITE_EX + Fore.LIGHTWHITE_EX + 'W ',
        Back.LIGHTRED_EX + Fore.LIGHTRED_EX + 'R ',
        Back.LIGHTBLUE_EX + Fore.LIGHTBLUE_EX + 'B ',
        Back.YELLOW + Fore.YELLOW + 'O ',
        Back.LIGHTGREEN_EX + Fore.LIGHTGREEN_EX + 'G ',
        Back.LIGHTYELLOW_EX + Fore.LIGHTYELLOW_EX + 'Y ',
        Style.RESET_ALL]
    number_labels = ['0 ','1 ','2 ','3 ','4 ','5 ']
    letter_labels = ['W ','R ','B ','O ','G ','Y ']
    lower_labels = ['w ','r ','b ','o ','g ','y ']
    
    # default labels for cube faces
    default_labels = color_labels
    
    def __init__(self, n=3):
        self.n = n if n > 0 else 3
        self.set_labels(Cube.default_labels)
        self.reset()
    
    def __eq__(self, other):
        '''Determines if the face values of two cubes are exactly the same in
        their current orientation. Will return False for cubes which are in
        different orientations but are otherwise the same.'''
        
        for f in range(6):
            for r in range(self.n):
                for c in range(self.n):
                    if self.faces[f][r][c] != other.faces[f][r][c]:
                        return False
        return True
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        res = ''
        for i in range(self.n):
            res += '      '
            for j in range(self.n):
                res += self.labels[self.faces[0][i][j]]
            res += self.end + '\n'
        
        for i in range(self.n):
            for f in range(1,5):
                for j in range(self.n):
                    res += self.labels[self.faces[f][i][j]]
            res += self.end + '\n'
        
        for i in range(self.n):
            res += '      '
            for j in range(self.n):
                res += self.labels[self.faces[5][i][j]]
            res += self.end + '\n'
        
        return res[:-1]
    
    def set_labels(self, labels):
        if len(labels) == 7:
            self.end = labels[6]
            self.labels = labels[:-1]
        else:
            self.end = ''
            self.labels = labels[:]
    
    def reset(self):
        self.history = []
        self.faces = [[[i for c in range(self.n)] for r in range(self.n)] for i in range(6)]
    
    def move(self, face, x=1):
        self.history.append(('move', face, x))
        
        # rotate selected face
        self.faces[face] = rotate_face(self.faces[face], x)
        
        # move adjacent edges
        ls = ROTATIONS[face]
        edges = [get_edge(self.faces[f], r) for f, r in ls]
        for i in range(4):
            f, r = ls[(i + x) % 4]
            set_edge(self.faces[f], r, edges[i])
    
    def moves(self, vals):
        if isinstance(vals, str):
            for tup in map(parse_move, vals.split()):
                print(tup)
                if tup is not None:
                    self.move(tup[0], tup[1])
        else:
            for face, x in vals:
                self.move(face, x)
    
    def rotate(self, face, x=1):
        '''Rotates the entire cube around a face, changing its orientation'''
        
        self.history.append(('rotate', face, x))
        
        # rotate selected and opposite faces
        opp = OPPOSITES[face]
        self.faces[face] = rotate_face(self.faces[face], x)
        self.faces[opp] = rotate_face(self.faces[opp], 4 - x)
        
        # rotate and move adjacent faces
        ls = ROTATIONS[face]
        fs = [rotate_face(self.faces[f], r) for f, r in ls]
        for i in range(4):
            f, r = ls[(i + x) % 4]
            self.faces[f] = rotate_face(fs[i], 4 - r)
    
    def run_history(self, hist):
        for typ, face, x in hist:
            if typ == 'move':
                self.move(face, x)
            elif typ == 'rotate':
                self.rotate(face, x)
    
    def is_solved(self):
        for f in self.faces:
            val = f[0][0]
            for r in range(self.n):
                for c in range(self.n):
                    if f[r][c] != val:
                        return False
        return True
