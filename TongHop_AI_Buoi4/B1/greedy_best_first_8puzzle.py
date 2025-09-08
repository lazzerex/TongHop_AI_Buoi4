"""


Greedy Best First Search chỉ sử dụng hàm heuristic h(n) để chọn nút tiếp theo
"""

from simpleai.search import SearchProblem, greedy
import time

GOAL = '12345678_'

class EightPuzzleProblem(SearchProblem):

    
    def __init__(self, initial_board):
        # Chuyển board 2D thành string
        initial_state = self.board_to_string(initial_board)
        super(EightPuzzleProblem, self).__init__(initial_state)
        self.goal_state = GOAL
    
    def board_to_string(self, board):
        """Chuyển đổi board 2D thành string"""
        result = ""
        for row in board:
            for cell in row:
                if cell == 0:
                    result += "_"
                else:
                    result += str(cell)
        return result
    
    def string_to_board(self, state):
        """Chuyển string thành board 2D để hiển thị"""
        board = []
        for i in range(3):
            row = []
            for j in range(3):
                char = state[i * 3 + j]
                if char == '_':
                    row.append(0)
                else:
                    row.append(int(char))
            board.append(row)
        return board
    
    def actions(self, state):
        """Trả về danh sách các hành động có thể thực hiện từ trạng thái hiện tại"""
        empty_index = state.index('_')
        actions = []
        
        # Kiểm tra có thể di chuyển trái không (không ở cột đầu tiên)
        if empty_index % 3 > 0:
            actions.append('LEFT')
        
        # Kiểm tra có thể di chuyển phải không (không ở cột cuối)
        if empty_index % 3 < 2:
            actions.append('RIGHT')
        
        # Kiểm tra có thể di chuyển lên không (không ở hàng đầu)
        if empty_index // 3 > 0:
            actions.append('UP')
        
        # Kiểm tra có thể di chuyển xuống không (không ở hàng cuối)
        if empty_index // 3 < 2:
            actions.append('DOWN')
        
        return actions
    
    def result(self, state, action):
        """Trả về trạng thái mới sau khi thực hiện hành động"""
        empty_index = state.index('_')
        new_index = empty_index
        
        if action == 'LEFT':
            new_index -= 1
        elif action == 'RIGHT':
            new_index += 1
        elif action == 'UP':
            new_index -= 3
        elif action == 'DOWN':
            new_index += 3
        
        # Chuyển string thành list để hoán đổi
        state_list = list(state)
        state_list[empty_index], state_list[new_index] = state_list[new_index], state_list[empty_index]
        
        return ''.join(state_list)
    
    def is_goal(self, state):
        """Kiểm tra xem có phải trạng thái mục tiêu không"""
        return state == self.goal_state
    
    def heuristic(self, state):
        """
        Hàm heuristic: Manhattan Distance
        Tính tổng khoảng cách Manhattan từ mỗi ô đến vị trí đích
        """
        total_distance = 0
        for i, tile in enumerate(state):
            if tile != '_':  # Bỏ qua ô trống
                current_row, current_col = i // 3, i % 3
                goal_index = GOAL.index(tile)
                goal_row, goal_col = goal_index // 3, goal_index % 3
                
                distance = abs(current_row - goal_row) + abs(current_col - goal_col)
                total_distance += distance
        
        return total_distance

def print_board(state):
    """In trạng thái của bảng puzzle từ string"""
    for i in range(3):
        row = []
        for j in range(3):
            char = state[i * 3 + j]
            if char == '_':
                row.append(' ')
            else:
                row.append(char)
        print(' '.join(row))
    print()

def print_solution_path(result, problem):
    """In đường đi giải quyết"""
    if not result:
        print("Không tìm thấy lời giải!")
        return
    
    path = result.path()
    print(f"\n=== ĐƯỜNG ĐI GIẢI QUYẾT (Greedy Best First Search) ===")
    print(f"Tổng số bước: {len(path) - 1}")
    print()
    
    for i, (action, state) in enumerate(path):
        print(f"Bước {i}:")
        if action:
            print(f"Hành động: {action}")
        print_board(state)
        
        # Tính heuristic cho trạng thái này
        h_value = problem.heuristic(state)
        print(f"Heuristic (Manhattan Distance): {h_value}")
        print("-" * 30)

def is_solvable(board):
    """
    Kiểm tra xem puzzle có thể giải được không
    Một 8-puzzle có thể giải được nếu số lượng inversions là chẵn
    """
    # Chuyển board 2D thành list 1D, bỏ qua số 0
    flat = []
    for row in board:
        for cell in row:
            if cell != 0:
                flat.append(cell)
    
    # Đếm số inversions
    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1
    
    return inversions % 2 == 0

def main():
 
    print("=" * 60)
    
    # Trạng thái mục tiêu
    goal_board = [
        [1, 2, 3],
        [4, 5, 6], 
        [7, 8, 0]
    ]
    
    print("Trạng thái mục tiêu:")
    print_board(GOAL)
    
    # Test case 1: Trạng thái dễ (2 bước)
    print("=" * 60)
    print("TEST CASE 1")
    
    easy_board = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]
    
    print("Trạng thái ban đầu:")
    problem = EightPuzzleProblem(easy_board)
    print_board(problem.initial_state)
    
    if is_solvable(easy_board):
        print(f"Heuristic ban đầu: {problem.heuristic(problem.initial_state)}")
        
        start_time = time.time()
        result = greedy(problem, graph_search=True)
        end_time = time.time()
        
        print(f"⏱️  Thời gian thực hiện: {end_time - start_time:.4f} giây")
        print_solution_path(result, problem)
    
    # Test case 2: Trạng thái trung bình
    print("\n" + "=" * 60)
    print("TEST CASE 2")
    
    medium_board = [
        [1, 2, 3],
        [4, 5, 6],
        [0, 7, 8]
    ]
    
    print("Trạng thái ban đầu:")
    problem_medium = EightPuzzleProblem(medium_board)
    print_board(problem_medium.initial_state)
    
    if is_solvable(medium_board):
        problem = problem_medium
        print(f"Heuristic ban đầu: {problem.heuristic(problem.initial_state)}")
        
        start_time = time.time()
        result = greedy(problem, graph_search=True)
        end_time = time.time()
        
        print(f"⏱️  Thời gian thực hiện: {end_time - start_time:.4f} giây")
        print_solution_path(result, problem)
    
 


if __name__ == "__main__":
    main()
