import random
from copy import deepcopy
from queue import PriorityQueue

def create_tile_puzzle(rows, cols):
    board = []
    for i in range(rows):
        currentRow = []
        for j in range(cols):
            currentRow.append((i*cols + j + 1) % (rows*cols))
        board.append(currentRow)
    return TilePuzzle(board)

class TilePuzzle(object):

    def __init__(self, board):
        self.rows = len(board)
        self.board = board
        if self.rows == 0:
            self.columns = 0
        else:
            self.columns = len(board[0])
        self.zeroR, self.zeroC = self.locateZero()
        self.originalPosition = self.board

    def locateZero(self):
        for i, row in enumerate(self.board):
            for j, val in enumerate(row):
                if val == 0:
                    return i,j
        return None,None
    def get_board(self):
        return self.board

    def perform_move(self, direction):
        dir = ["up", "down", "left", "right"]
        if direction == "up" and self.zeroR > 0:
            swappedValue = self.board[self.zeroR-1][self.zeroC]
            self.board[self.zeroR - 1][self.zeroC] = 0
            self.board[self.zeroR][self.zeroC] = swappedValue
            self.zeroR -= 1
            return True

        if direction == "down" and self.zeroR < self.rows-1:
            swappedValue = self.board[self.zeroR + 1][self.zeroC]
            self.board[self.zeroR + 1][self.zeroC] = 0
            self.board[self.zeroR][self.zeroC] = swappedValue
            self.zeroR += 1
            return True

        if direction == "left" and self.zeroC > 0:
            swappedValue = self.board[self.zeroR][self.zeroC-1]
            self.board[self.zeroR][self.zeroC-1] = 0
            self.board[self.zeroR][self.zeroC] = swappedValue
            self.zeroC -= 1
            return True

        if direction == "right" and self.zeroC < self.columns -1 :
            swappedValue = self.board[self.zeroR][self.zeroC+1]
            self.board[self.zeroR][self.zeroC+1] = 0
            self.board[self.zeroR][self.zeroC] = swappedValue
            self.zeroC += 1
            return True
        return False

    def scramble(self, num_moves):
        moves = ["up", "down", "left", "right"]
        while num_moves > 0:
            randir = random.choice(moves)
            self.perform_move(randir)
            num_moves -= 1

    def is_solved(self):
        c = 1
        for i in range(self.rows):
            for j in range(self.columns):
                if i == self.rows -1 and j == self.columns -1:
                    if self.board[i][j] != 0:
                        return False
                elif self.board[i][j] != c:
                    return False
                c+=1
        return True


    def copy(self):
        copyboard = deepcopy(self.board)
        return TilePuzzle(copyboard)

    def successors(self):
        moves = ["up", "down", "left", "right"]
        for move in moves:
            nextState = self.copy()
            if nextState.perform_move(move):
                yield (move,nextState)


    # Required
    def iddfs_helper(self, limit, moves):
        directions = ["up", "down", "left", "right"]
        if self.is_solved():
            yield moves
        if limit > 0:
            for dir in directions:
                if moves and ((moves[-1], dir) in [('up', 'down'), ('down', 'up'), ('left', 'right'), ('right', 'left')]):
                    continue
                saved_board = self.copy()
                saved_zeroR, saved_zeroC = self.zeroR, self.zeroC
                if self.perform_move(dir):
                    self.zeroR, self.zeroC = self.locateZero()
                    yield from self.iddfs_helper(limit - 1, moves + [dir])
                    self.board = saved_board.board
                    self.zeroR, self.zeroC = saved_zeroR, saved_zeroC

    def find_solutions_iddfs(self):
        depth_limit = 0
        while True:
            solutions= list(self.iddfs_helper(depth_limit, []))
            if solutions:
                for solution in solutions:
                    yield solution
                break
            depth_limit +=1


    def manhattan(self, board):
        d = 0
        for i in range(len(board)):
           for j in range(len(board[i])):
               if board[i][j] != 0:
                   r = (board[i][j] - 1) // len(board)
                   c = (board[i][j] -1) % len(board[0])
                   d += abs(i-r) + abs(j-c)
        return d
    def find_solution_a_star(self):
        priorityQ = PriorityQueue()
        visited = set()

        priorityQ.put((self.manhattan(self.board), ([], self)))

        while not priorityQ.empty():
            currDistance, (currMoves, currState) = priorityQ.get()
            if currState.is_solved():
                return currMoves
            tup = tuple(map(tuple, currState.get_board()))
            visited.add(tup)

            for i, j in currState.successors():
                next = tuple(map(tuple,j.get_board()))
                if next not in visited:
                    priorityQ.put((self.manhattan(j.get_board()) +
                                   len(currMoves) + 1,(currMoves+ [i], j)))
                    visited.add(next)
        return []

