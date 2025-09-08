"""


A* Search sử dụng f(n) = g(n) + h(n) để đảm bảo lời giải tối ưu
g(n): chi phí từ trạng thái đầu đến trạng thái hiện tại  
h(n): heuristic từ trạng thái hiện tại đến mục tiêu
"""

from simpleai.search import SearchProblem, astar
import time

GOAL = '12345678_'

class EightPuzzleProblem(SearchProblem):
    """
    Sử dụng string để biểu diễn trạng thái: '12345678_' (ô trống là '_')
    """
    
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
    
    def cost(self, state, action, state2):
        """
        Chi phí để di chuyển từ state đến state2 bằng action
        Trong 8-puzzle, mỗi bước di chuyển có chi phí là 1
        """
        return 1
    
    def heuristic(self, state):
        """
        Hàm heuristic: Manhattan Distance
        Tính tổng khoảng cách Manhattan từ mỗi ô đến vị trí đích
        Đây là heuristic admissible (không bao giờ overestimate)
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

def calculate_misplaced_tiles(state):
    """
    Hàm heuristic thay thế: Misplaced Tiles
    Đếm số ô không đúng vị trí (trừ ô trống)
    """
    misplaced = 0
    for i, tile in enumerate(state):
        if tile != '_' and tile != GOAL[i]:
            misplaced += 1
    return misplaced

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
    """In đường đi giải quyết với thông tin chi tiết về A*"""
    if not result:
        print("Không tìm thấy lời giải!")
        return
    
    path = result.path()
    print(f"\n=== ĐƯỜNG ĐI GIẢI QUYẾT TỐI ƯU (A* Search) ===")
    print(f"Tổng số bước: {len(path) - 1}")
    print(f"Chi phí tối ưu: {len(path) - 1}")
    print()
    
    for i, (action, state) in enumerate(path):
        print(f"Bước {i}:")
        if action:
            print(f"Hành động: {action}")
        print_board(state)
        
        # Tính g(n), h(n), f(n)
        g_cost = i  # Chi phí từ trạng thái đầu
        h_cost = problem.heuristic(state)  # Heuristic
        f_cost = g_cost + h_cost  # Tổng chi phí
        
        print(f"g(n) = {g_cost}, h(n) = {h_cost}, f(n) = {f_cost}")
        
        # Hiển thị thêm heuristic Misplaced Tiles để so sánh
        misplaced = calculate_misplaced_tiles(state)
        print(f"Misplaced Tiles: {misplaced}")
        print("-" * 40)

def is_solvable(board):

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

def compare_heuristics(problem, state):
    """So sánh các hàm heuristic khác nhau"""
    print("--- So sánh hàm Heuristic ---")
    print(f"Manhattan Distance: {problem.heuristic(state)}")
    print(f"Misplaced Tiles: {calculate_misplaced_tiles(state)}")
    print()

def main():
    print("A* SEARCH - 8-PUZZLE với SimpleAI")
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
        print(f"Chi phí ban đầu - g(n) = 0, h(n) = {problem.heuristic(problem.initial_state)}, f(n) = {problem.heuristic(problem.initial_state)}")
        
        # So sánh heuristics
        compare_heuristics(problem, problem.initial_state)
        
        start_time = time.time()
        result = astar(problem, graph_search=True)
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
    print(f"Có thể giải được: {'Có' if is_solvable(medium_board) else 'Không'}")
    
    if is_solvable(medium_board):
        problem = problem_medium
        print(f"Chi phí ban đầu - g(n) = 0, h(n) = {problem.heuristic(problem.initial_state)}, f(n) = {problem.heuristic(problem.initial_state)}")
        
        compare_heuristics(problem, problem.initial_state)
        
        start_time = time.time()
        result = astar(problem, graph_search=True)
        end_time = time.time()
        
        print(f"⏱️  Thời gian thực hiện: {end_time - start_time:.4f} giây")
        print_solution_path(result, problem)
    


    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
