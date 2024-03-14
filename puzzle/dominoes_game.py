import random
import math
from collections import namedtuple
from heapq import heappop, heappush

Node = namedtuple('Node', ['state', 'parent', 'action', 'g'])
def diskSuccessors(state):
    empty = state.index('E')
    moves = []

    for i in [-1,1]:
        if 0 <= empty + i < len(state) and state[empty+i] != 'E':
            new = list(state)
            new[empty], new[empty+i] =  new[empty+i], new[empty]
            moves.append((tuple(new), (empty, empty + i)))
    for j in [-2,2]:
        if 0 <= empty + j < len(state) and state[empty+j//2] != 'E'\
                and state[empty + j] != 'E':
            new = list(state)
            new[empty], new[empty+j] =  new[empty+j], new[empty]
            moves.append((tuple(new), (empty, empty + i)))
    return moves

def heuristicSolver(state):
    reversedDisks = []
    for i in range(len(state)-1):
        reversedDisks.insert(0,str(i))
    reversedDisks = tuple(reversedDisks)+ ('E',)
    notMatch = 0
    for st, re in zip(state,reversedDisks):
        if st != re and st != 'E':
            notMatch+=1
    return notMatch

def solve_distinct_disks(length, n):
    startState = tuple(str(i) for i in range(n)) + ('E', ) * (length - n)
    goalState = tuple(str(i) for i in reversed(range(n))) + ('E',) * (length - n)

    openList = [(heuristicSolver(startState), Node(startState, None, None, 0))]
    closedList = set()


    while openList:
        _, currentNode = heappop(openList)
        if currentNode.state == goalState:
            moves = []
            while currentNode.parent:
                moves.append(currentNode.action)
                currentNode = currentNode.parent
            return moves[::-1]
        closedList.add(currentNode.state)
        for next, action in diskSuccessors(currentNode.state):
            if next not in closedList:
                g = currentNode.g + 1
                f = g + heuristicSolver(next)
                cont = Node(next, currentNode, action, g)
                heappush(openList, (f, cont))

    return None  

def create_dominoes_game(rows, cols):
    board = []
    for i in range(rows):
        board.append([False]*cols)
    return DominoesGame(board)

class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = [row.copy() for row in board]
        self.rows = len(board)
        if board:
            self.cols = len(board[0])
        else:
            self.cols = 0
    def get_board(self):
        fullBoard = []
        for row in self.board:
            fullBoard.append(row.copy())
        return fullBoard

    def reset(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = False

    def is_legal_move(self, row, col, vertical):
        if vertical:
            if row+1 < self.rows:
                if self.board[row][col] == False and self.board[row+1][col] == False:
                     return True
        else:
            if col+1 < self.cols:
                if self.board[row][col] == False and self.board[row][col+1] == False:
                     return True
        return False



    def legal_moves(self, vertical):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.is_legal_move(i,j, vertical):
                    yield (i,j)


    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row,col,vertical):
            if vertical:
                self.board[row][col] = True
                self.board[row+1][col] = True
            else:
                self.board[row][col] = True
                self.board[row][col+1] = True
            return True
        return False


    def game_over(self, vertical):

        for i in range(self.rows):
            for j in range(self.cols):
                if self.is_legal_move(i,j, vertical):
                    return False
        return True


    def copy(self):
        copyboard = [row.copy() for row in self.board]
        return DominoesGame(copyboard)

    def successors(self, vertical):
        for move in self.legal_moves(vertical):
            nextState = self.copy()
            if nextState.perform_move(move[0], move[1], vertical):
                yield (move, nextState.get_board())

    def get_random_move(self, vertical):
        moves = list(self.legal_moves(vertical))
        if not moves:
            return None
        randir = random.choice(moves)
        return randir

    # Required
    def get_best_move(self, vertical, limit):
        bestValue = -math.inf
        alpha = -math.inf
        beta = math.inf
        bestAction = None
        visitedLeaves = [0]

        for a in sorted(self.legal_moves(vertical)):
            v = self.min_value(self.result(a,vertical),
                               alpha, beta, 1, limit, not vertical, visitedLeaves)
            if v > bestValue:
                bestValue = v
                bestAction = a
            alpha = max(alpha, v)
        print("Re1")
        return bestAction, bestValue, visitedLeaves[0]

    def max_value(self, state,alpha, beta, depth, limit, vertical, visitedLeaves):
        if depth == limit or state.game_over(vertical):
            visitedLeaves[0] += 1
            print("Re2")
            return self.utility(state, vertical)

        v = -math.inf
        for m in sorted(state.legal_moves(vertical)):
            v = max(v,
                    self.min_value(state.result(m, vertical),
                                   alpha, beta, depth + 1, limit,
                                   not vertical, visitedLeaves))
            if v >= beta:
                print("Re3")
                return v
            alpha = max(alpha, v)
        print("Re4")
        return v

    def min_value(self, state,alpha, beta, depth, limit, vertical, visitedLeaves):
        if depth == limit or state.game_over(vertical):
            visitedLeaves[0] += 1
            return self.utility(state, vertical)

        v = math.inf
        for m in sorted(state.legal_moves(vertical)):
            v = min(v,
                    self.max_value(state.result(m, vertical),
                                   alpha, beta, depth + 1, limit,
                                   not vertical, visitedLeaves))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
    def result(self, move,vertical):
        new = self.copy()
        new.perform_move(move[0], move[1], vertical)
        return new

    def utility(self, state, vertical):
        differenceMoves =  len(list(state.legal_moves(vertical))) - \
                len(list(state.legal_moves(not vertical)))
        return differenceMoves

