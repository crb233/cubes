
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

def parse_moves(string):
    return filter(lambda x: x is not None, map(parse_move, string.split()))

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

def normalize_history(hist):
    '''Return a modified history such that the resulting cube is the same, but
    no rotations are used'''
    pass

def invert_moves(vals):
    res = []
    for f, x in reversed(vals):
        res.append((f, x if x == 0 else 4 - x))
    return res

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
        
        # TODO smarter equality checks
        
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
            vals = parse_moves(vals)
        for face, x in vals:
            self.move(face, x)
    
    def rotate(self, face, x=1):
        '''Rotates the entire cube around a face, changing its orientation'''
        
        self.history.append(('rotate', face, x))
        
        new_faces = [None] * 6
        
        # rotate selected and opposite faces
        opp = OPPOSITES[face]
        new_faces[face] = rotate_face(self.faces[face], x)
        new_faces[opp] = rotate_face(self.faces[opp], 4 - x)
        
        # rotate and move adjacent faces
        ls = ROTATIONS[face]
        for i in range(4):
            f0, r0 = ls[i]
            f1, r1 = ls[(i + x) % 4]
            new_faces[f1] = rotate_face(self.faces[f0], r0 - r1)
        
        self.faces = new_faces
    
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

def main(args):
    c = Cube()
    print(c)
    
    hist = []
    while 1:
        inp = input(Fore.LIGHTMAGENTA_EX + 'm' + str(len(hist)) + Fore.RESET + '> ').strip()
        if inp in ['q', 'exit', 'quit']:
            break
        elif inp in ['r', 'reset']:
            c.reset()
        else:
            if inp.startswith(':'):
                try:
                    i = int(inp[1:])
                    m = hist[i]
                except Exception as err:
                    print_err('Syntax error')
                    continue
            else:
                m = parse_moves(inp)
            
            m = list(m)
            if len(m) == 0:
                print_err('Invalid moves')
                continue
            
            hist.append(m)
            c.moves(m)
            print(c)
    print("Goodbye")

def print_err(msg):
    print(Fore.LIGHTRED_EX + str(msg) + Fore.RESET)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
