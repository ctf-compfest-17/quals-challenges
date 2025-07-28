import re

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
TABLE = [[22, 2, 15, 5, 19, 17, 11, 61], [60, 59, 27, 18, 7, 23, 21, 44], [26, 34, 58, 38, 37, 4, 14, 20], [29, 39, 13, 56, 57, 47, 9, 46], [54, 62, 33, 42, 48, 12, 45, 53], [35, 55, 36, 25, 52, 41, 49, 8], [24, 50, 16, 6, 40, 28, 3, 63], [51, 0, 1, 30, 31, 32, 10, 43]]
TARGETS = [[63, 63, 63, 63, 63, 62, 63, 63], [63, 63, 62, 62, 61, 61, 59, 63], [55, 63, 63, 61, 63, 62, 62, 63], [63, 62, 61, 61, 61, 59, 61, 63], [63, 63, 60, 61, 63, 60, 51, 54], [62, 55, 39, 35, 61, 58, 43, 52], [44, 48, 56, 54, 54, 31, 23, 27], [58, 46, 48, 39, 23, 31, 33, 21]]

def countOptions(grid, x, y, dir):
    """
    Count the number of valid knight moves from position (x, y).This helps 
    apply Warnsdorff's heuristic: prefer moves with fewer onward options.
    """
    count = 0
    n = len(grid)
    for dx, dy in dir:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 0:
            count += 1
    return count

def getSortedMoves(grid, x, y, dir):
    """
    Generate all valid knight moves from (x, y),and sort them based on the 
    number of onward options available from the new position.
    """
    options = []
    n = len(grid)
    for i, (dx, dy) in enumerate(dir):
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 0:
            # Store the count of further moves and the move index
            options.append((countOptions(grid, nx, ny, dir), i))
    
    # Sort moves with least onward options first (Warnsdorff's rule)
    options.sort()
    return options

def knightTourUtil(n, x, y, grid, step, dir):
    """
    Recursively try to complete the Knight's Tour from current position 
    (x, y). If all squares are visited (step == n*n), return True.
    Uses backtracking if a path fails.
    """
    if step == n * n:
        # if (x, y) in visited:
            # return False
        # visited.add((x, y))
        return True

    # Get next possible moves from current position
    for _, idx in getSortedMoves(grid, x, y, dir):
        nx = x + dir[idx][0]
        ny = y + dir[idx][1]

        # Mark the next move with the current step
        grid[nx][ny] = step

        # Recursively proceed from the new position
        if knightTourUtil(n, nx, ny, grid, step + 1, dir):
            return True

        # Backtrack: unmark the move
        grid[nx][ny] = 0

    # No valid move found from this position
    return False

def knightTour(n, x, y):
    """
    Initializes the chessboard and starts the Knight's Tour from position 
    (0, 0) Returns the completed board or [[-1]] if no solution exists.
    """
    # Create an n x n board initialized with 0
    grid = [[0] * n for _ in range(n)]

    # Start from top-left corner
    grid[x][y] = -1  # Temporarily mark the start cell

    # Define all 8 possible knight moves (dx, dy)
    dir = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]

    # Begin the knight's traversal from (0, 0)
    if not knightTourUtil(n, x, y, grid, 1, dir):
        return [[-1]]  # No solution found

    # Set the first move to 0 (as it was marked -1)
    grid[x][y] = 0

    # Validate that only one cell (starting cell) was initially unmarked
    empty = sum(row.count(0) for row in grid)
    return grid if empty == 1 else [[-1]]

class JavaRandom:
    def __init__(self, seed=None):
        if seed is None:
            import time
            seed = int(time.time() * 1000)  # Similar to Java's default seeding
        self.seed = self.initial_scramble(seed)

    def initial_scramble(self, seed):
        return (seed ^ 0x5DEECE66D) & ((1 << 48) - 1)

    def next(self, bits):
        self.seed = (self.seed * 0x5DEECE66D + 0xB) & ((1 << 48) - 1)
        return (self.seed >> (48 - bits)) & 0xFFFFFFFF

    # def next_int(self, bound=None):
        # if bound is None:
            # return self.next(32)  # Standard 32-bit int
        # if bound <= 0:
            # raise ValueError("bound must be positive")
        # # Java's algorithm for bounded nextInt
        # bits = self.next(31)
        # val = bits % bound
        # while (bits - val + bound - 1) < 0:
            # bits = self.next(31)
            # val = bits % bound
        # return val

    def next_int(self, bound=None):
        if bound is None:
            return self.next(32)  # Standard 32-bit int
        if bound <= 0:
            raise ValueError("bound must be positive")
        
        r = self.next(31)  # Java uses 31 bits for bounded nextInt
        m = bound - 1
        if (bound & m) == 0:  # Power of 2: faster path
            return (bound * r) >> 31
        else:
            # Rejection-based correction to avoid modulo bias
            u = r
            while True:
                val = u % bound
                if u - val + m >= 0:
                    return val
                u = self.next(31)

    # Additional methods (similar to Java's Random)
    def next_long(self):
        return (self.next(32) << 32) + self.next(32)

    def next_boolean(self):
        return self.next(1) != 0

    def next_float(self):
        return self.next(24) / (1 << 24)

mapping = {}
visited = set()
for x in range(8):
    for y in range(8):
        tour = knightTour(8, x, y)
        if tour == [[-1]]:
            mapping[(x, y)] = (y, x)
        else:
            done = False
            restart = False
            target = TARGETS[x][y]
            for cx in range(8):
                for cy in range(8):
                    if tour[cx][cy] == target:
                        if (cx, cy) in visited:
                            target = max(0, target-1)
                            restart = True
                            break
                        mapping[(x, y)] = (cx, cy)
                        visited.add((cx, cy))
                        done = True
                        target = 63
                        break
                
                if done: break
            
            if not done:
                mapping[(x, y)] = (y, x)

rev_map = {v: k for k, v in mapping.items()}

tmap = {}
for x in range(8):
    for y in range(8):
        tmap[TABLE[x][y]] = (x, y)

enc = "MnbaMT3hEIwrv1waw9d3vxwrw+cebKacvqba6rbevgvMhZwbaTr3wshrdgabwa+7a36MwYbzxg3x"
dec = ""
rnd = 0
for c in range(0, len(enc), 4):
    ch1 = CHARS.index(enc[c])
    ch2 = CHARS.index(enc[c+1])
    ch3 = None
    ch4 = None
    if enc[c+2] != "=":
        ch3 = CHARS.index(enc[c+2])
    if enc[c+3] != "=":
        ch4 = CHARS.index(enc[c+3])
    
    # print(f"{rnd = }, {ch1 = }, {ch2 = }, {ch3 = }, {ch4 = }")
    
    tmp1 = rev_map[tmap[ch1]]
    n1 = (8*tmp1[0] + tmp1[1])
    tmp2 = rev_map[tmap[ch2]]
    n2 = (8*tmp2[0] + tmp2[1])
    # if ch3 == None:
        # n = (n1 << 18) + (n2 << 12)
        # dec += chr((n >> 16) & 0xFF)
        # break

    tmp3 = rev_map[tmap[ch3]]
    n3 = (8*tmp3[0] + tmp3[1])
    # if ch4 == None:
        # n = (n1 << 18) + (n2 << 12) + (n3 << 6)
        # dec += chr((n >> 16) & 0xFF) + chr((n >> 8) & 0xFF)
        # break
    
    tmp4 = rev_map[tmap[ch4]]
    n4 = (8*tmp4[0] + tmp4[1])

    p1 = (n2 & 0b001100) >> 2
    p3 = (n2 & 0b110000) >> 4
    p4 = n2 & 0b000011
    n1 = (n1 << 2) + p1
    n3 = (n3 << 2) + p3
    n4 = (n4 << 2) + p4
    dec += chr(n3) + chr(n1) + chr(n4)
    # n = (n1 << 18) + (n2 << 12) + (n3 << 6) + n4
    # dec += chr((n >> 16) & 0xFF) + chr((n >> 8) & 0xFF) + chr(n & 0xFF)

    rnd += 1

seed = 0
for c in dec:
    seed ^= ord(c)
rnd = JavaRandom(seed)
idxs = []
for i in range(len(dec[:-2])-1, -1, -1):
    idxs.append(rnd.next_int(i+1))

dec = list(dec)
for i, idx in enumerate(idxs[::-1]):
    # print(f"{i = }, {idx = }")
    tmp = dec[idx]
    dec[idx] = dec[i]
    dec[i] = tmp
print("".join(dec))
