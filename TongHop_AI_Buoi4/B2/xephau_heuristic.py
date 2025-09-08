from simpleai.search import SearchProblem
from simpleai.search import astar, greedy
import random

class EightQueensHeuristicProblem(SearchProblem):
    """
    Bài toán 8 quân hậu cho heuristic search (Greedy Best-First, A*).
    State: tuple 8 phần tử, mỗi phần tử là vị trí hàng (0..7) của quân hậu trong cột tương ứng.
    """

    def __init__(self, initial_state=None):
        if initial_state is None:
            initial_state = tuple(random.randint(0, 7) for _ in range(8))
        super().__init__(initial_state)

    def actions(self, state):
        """
        Action = (col, new_row): di chuyển quân hậu ở cột col đến hàng new_row
        """
        actions = []
        for col in range(8):
            for new_row in range(8):
                if new_row != state[col]:
                    actions.append((col, new_row))
        return actions

    def result(self, state, action):
        """
        Thực hiện action trên state
        """
        col, new_row = action
        new_state = list(state)
        new_state[col] = new_row
        return tuple(new_state)

    def is_goal(self, state):
        """
        Trạng thái đích: không quân hậu nào tấn công nhau
        """
        return self.value(state) == 28

    def value(self, state):
        """
        Trả về số cặp quân hậu không tấn công nhau.
        Tối đa = 28 (8*7/2)
        """
        non_attacking_pairs = 0
        n = len(state)
        for i in range(n):
            for j in range(i + 1, n):
                if not self.is_attacking(state, i, j):
                    non_attacking_pairs += 1
        return non_attacking_pairs

    def heuristic(self, state):
        """
        Heuristic = số cặp quân hậu đang xung đột
        """
        return 28 - self.value(state)

    def is_attacking(self, state, i, j):
        if state[i] == state[j]:
            return True
        if abs(state[i] - state[j]) == abs(i - j):
            return True
        return False


def print_board(state):
    """
    In bàn cờ ra màn hình
    """
    print("\nBàn cờ 8x8:")
    print("  " + " ".join(str(i) for i in range(8)))
    for row in range(8):
        line = f"{row} "
        for col in range(8):
            if state[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)
    print()


def solve_with_greedy():
    print("=" * 60)
    print("GREEDY BEST-FIRST SEARCH")
    print("=" * 60)
    problem = EightQueensHeuristicProblem()
    print(f"State ban đầu: {problem.initial_state}")
    result = greedy(problem, problem.heuristic)
    print(f"\nKết quả: {result.state}")
    print_board(result.state)
    print(f"Số cặp không xung đột: {problem.value(result.state)}/28")


def solve_with_astar():
    print("=" * 60)
    print("A* SEARCH")
    print("=" * 60)
    problem = EightQueensHeuristicProblem()
    print(f"State ban đầu: {problem.initial_state}")
    result = astar(problem, problem.heuristic)
    print(f"\nKết quả: {result.state}")
    print_board(result.state)
    print(f"Số cặp không xung đột: {problem.value(result.state)}/28")


def main():
    print("BÀI TOÁN 8 QUÂN HẬU VỚI HEURISTIC SEARCH")
    print("=" * 80)
    try:
        solve_with_greedy()
    except Exception as e:
        print(f"Lỗi Greedy: {e}")

    try:
        solve_with_astar()
    except Exception as e:
        print(f"Lỗi A*: {e}")


if __name__ == "__main__":
    random.seed(42)
    main()
