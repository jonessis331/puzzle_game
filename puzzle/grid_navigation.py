import math
from heapq import heappop, heappush

class State:
    def __init__(self,position,parent= None):
        self.position = position
        self.parent = parent
        self.sDist = 0
        self.heuristic = 0
        self.cost = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.cost < other.cost


def get_neighbors(pos, scene):
    neighbors = [(pos[0] - 1, pos[1]),
        (pos[0] + 1, pos[1]),
        (pos[0], pos[1] - 1),
        (pos[0], pos[1] + 1),
        (pos[0] - 1, pos[1] - 1),
        (pos[0] - 1, pos[1] + 1),
        (pos[0] + 1, pos[1] - 1),
        (pos[0] + 1, pos[1] + 1)
    ]

    # Filter valid neighbors
    neighborsCut = []
    for x in neighbors:
        if  0 <= x[0] < len(scene) and 0 <= x[1] < len(scene[0]) and not scene[x[0]][x[1]]:
            neighborsCut.append(x)
    neighbors = neighborsCut
    return neighbors

def euclidean_distance(position1, position2):
    return math.sqrt((position1[0] - position2[0])**2 + (position1[1] - position2[1])**2)


def find_path(start, goal, scene):
    if(scene[start[0]][start[1]] or scene[goal[0]][goal[1]]):
        return None

    startState = State(start)
    goalState = State(goal)

    openList = []
    closedList = []
    heappush(openList, startState)

    while openList:
        currentState = heappop(openList)
        if currentState == goalState:
            path = []
            while currentState:
                path.append(currentState.position)
                currentState = currentState.parent
            return path [::-1]
        closedList.append(currentState)

        for p in get_neighbors(currentState.position,scene):
            neighbor = State(p,currentState)
            if neighbor in closedList:
                continue
            neighbor.sDist = currentState.sDist + euclidean_distance(
                currentState.position, neighbor.position)

            neighbor.heuristic = euclidean_distance(
                neighbor.position, goalState.position)

            neighbor.cost =neighbor.sDist + neighbor.heuristic

            if neighbor in openList:
                for s in openList:
                    if s == neighbor and s.cost > neighbor.cost:
                        openList.remove(s)
                        heappush(openList,neighbor)
                        break
            else:
                heappush(openList, neighbor)

    return None


