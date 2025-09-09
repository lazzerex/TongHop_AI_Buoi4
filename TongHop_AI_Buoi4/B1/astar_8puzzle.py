from simpleai.search import SearchProblem, astar

GOAL = '12345678_'

class EightPuzzle(SearchProblem):
    def __init__(self, board2d):
        super().__init__(self.board_to_str(board2d))
    def board_to_str(self, board):
        return ''.join(str(cell) if cell != 0 else '_' for row in board for cell in row)
    def actions(self, state):
        idx = state.index('_')
        acts = []
        if idx % 3 > 0: acts.append('LEFT')
        if idx % 3 < 2: acts.append('RIGHT')
        if idx // 3 > 0: acts.append('UP')
        if idx // 3 < 2: acts.append('DOWN')
        return acts
    def result(self, state, action):
        idx = state.index('_')
        swap = idx + {'LEFT': -1, 'RIGHT': 1, 'UP': -3, 'DOWN': 3}[action]
        l = list(state)
        l[idx], l[swap] = l[swap], l[idx]
        return ''.join(l)
    def is_goal(self, state):
        return state == GOAL
    def cost(self, a, b, c):
        return 1
    def heuristic(self, state):
        return sum(
            abs(i//3 - GOAL.index(tile)//3) + abs(i%3 - GOAL.index(tile)%3)
            for i, tile in enumerate(state) if tile != '_'
        )

def is_solvable(board):
    flat = [cell for row in board for cell in row if cell != 0]
    inv = sum(flat[i] > flat[j] for i in range(len(flat)) for j in range(i+1, len(flat)))
    return inv % 2 == 0

def print_board(state):
    for i in range(0, 9, 3):
        print(' '.join(state[i:i+3]).replace('_', ' '))
    print()

def misplaced_tiles(state):
    return sum(tile != '_' and tile != GOAL[i] for i, tile in enumerate(state))

if __name__ == '__main__':
    # Dễ: 2 bước
    board = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]
    problem = EightPuzzle(board)
    print("Trạng thái ban đầu:")
    print_board(problem.initial_state)
    if not is_solvable(board):
        print("Không giải được!")
    else:
        print(f"g(n)=0, h(n)={problem.heuristic(problem.initial_state)}, misplaced={misplaced_tiles(problem.initial_state)}")
        result = astar(problem, graph_search=True)
        for i, (action, state) in enumerate(result.path()):
            print(f"Bước {i}: {'-> '+action if action else ''}")
            print_board(state)
            print(f"g={i}, h={problem.heuristic(state)}, f={i+problem.heuristic(state)}, misplaced={misplaced_tiles(state)}\n")
