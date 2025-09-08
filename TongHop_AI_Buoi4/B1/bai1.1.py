"""
Bài toán 8-puzzle sử dụng thuật toán Greedy Best First Search
Thuật toán này chỉ sử dụng hàm heuristic h(n) để đánh giá các trạng thái
"""

import heapq
from collections import deque
import time

class PuzzleState:
    def __init__(self, board, parent=None, move=None, depth=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.heuristic = self.calculate_manhattan_distance()
    
    def __lt__(self, other):
        return self.heuristic < other.heuristic
    
    def __eq__(self, other):
        return self.board == other.board
    
    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))
    
    def find_blank(self):
        """Tìm vị trí của ô trống (số 0)"""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j
        return None
    
    def calculate_manhattan_distance(self):
        """Tính khoảng cách Manhattan từ trạng thái hiện tại đến trạng thái mục tiêu"""
        target = {1: (0, 0), 2: (0, 1), 3: (0, 2), 
                  4: (1, 0), 5: (1, 1), 6: (1, 2), 
                  7: (2, 0), 8: (2, 1), 0: (2, 2)}
        
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    target_row, target_col = target[self.board[i][j]]
                    distance += abs(i - target_row) + abs(j - target_col)
        return distance
    
    def is_goal(self):
        """Kiểm tra xem có phải trạng thái mục tiêu không"""
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        return self.board == goal
    
    def get_successors(self):
        """Tạo ra các trạng thái kế tiếp có thể"""
        successors = []
        blank_row, blank_col = self.find_blank()
        
        # Các hướng di chuyển có thể: lên, xuống, trái, phải
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        for dr, dc, move_name in moves:
            new_row, new_col = blank_row + dr, blank_col + dc
            
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                # Tạo bảng mới
                new_board = [row[:] for row in self.board]
                # Hoán đổi ô trống với ô kế tiếp
                new_board[blank_row][blank_col] = new_board[new_row][new_col]
                new_board[new_row][new_col] = 0
                
                successor = PuzzleState(new_board, self, move_name, self.depth + 1)
                successors.append(successor)
        
        return successors
    
    def print_board(self):
        """In bảng puzzle"""
        for row in self.board:
            print(' '.join(str(cell) if cell != 0 else ' ' for cell in row))
        print()

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

def greedy_best_first_search(initial_state):
    """
    Thuật toán Greedy Best First Search
    Chỉ sử dụng hàm heuristic h(n) để chọn nút tiếp theo
    """
    if initial_state.is_goal():
        return initial_state, 0, 1
    
    # Priority queue với heuristic làm priority
    open_list = []
    heapq.heappush(open_list, initial_state)
    
    # Set để theo dõi các trạng thái đã thăm
    closed_set = set()
    
    nodes_expanded = 0
    max_nodes = 200000  # Giới hạn để tránh chạy quá lâu
    
    while open_list and nodes_expanded < max_nodes:
        current_state = heapq.heappop(open_list)
        
        if hash(current_state) in closed_set:
            continue
            
        closed_set.add(hash(current_state))
        nodes_expanded += 1
        
        if current_state.is_goal():
            return current_state, current_state.depth, nodes_expanded
        
        # Tạo các trạng thái kế tiếp
        successors = current_state.get_successors()
        
        for successor in successors:
            if hash(successor) not in closed_set:
                heapq.heappush(open_list, successor)
    
    return None, -1, nodes_expanded  # Không tìm thấy lời giải

def print_solution_path(solution_state):
    """In đường đi từ trạng thái đầu đến trạng thái cuối"""
    path = []
    current = solution_state
    
    while current:
        path.append(current)
        current = current.parent
    
    path.reverse()
    
    print("=== ĐƯỜNG ĐI GIẢI QUYẾT ===")
    for i, state in enumerate(path):
        print(f"Bước {i}:")
        if state.move:
            print(f"Nước đi: {state.move}")
        state.print_board()
        print(f"Heuristic (Manhattan Distance): {state.heuristic}")
        print("-" * 20)

def main():
    print("GREEDY BEST FIRST SEARCH - BÀI TOÁN 8-PUZZLE")
    print("=" * 50)
    
    # Trạng thái mục tiêu
    goal_board = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    print("\nTrạng thái mục tiêu:")
    goal_state = PuzzleState(goal_board)
    goal_state.print_board()
    
    # Test case 1: Trạng thái dễ (2 bước)
    print("=" * 50)
    print("TEST CASE 1: TRẠNG THÁI DỄ (2 BƯỚC)")
    
    easy_board = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]
    
    print("Trạng thái đầu:")
    easy_state = PuzzleState(easy_board)
    easy_state.print_board()
    print(f"Heuristic ban đầu: {easy_state.heuristic}")
    print(f"Có thể giải được: {'Có' if is_solvable(easy_board) else 'Không'}")
    
    start_time = time.time()
    solution1, depth1, nodes_expanded1 = greedy_best_first_search(easy_state)
    end_time = time.time()
    
    if solution1:
        print(f"\n✅ TÌM THẤY LỜI GIẢI!")
        print(f"Độ sâu: {depth1} bước")
        print(f"Số nút đã mở rộng: {nodes_expanded1}")
        print(f"Thời gian thực hiện: {end_time - start_time:.4f} giây")
        print_solution_path(solution1)
    else:
        print(f"\n❌ KHÔNG TÌM THẤY LỜI GIẢI!")
        print(f"Số nút đã mở rộng: {nodes_expanded1}")
        print(f"Thời gian thực hiện: {end_time - start_time:.4f} giây")

    # Test case 2: Trạng thái trung bình (khoảng 4 bước)
    print("\n" + "=" * 50)
    print("TEST CASE 2: TRẠNG THÁI TRUNG BÌNH")
    
    medium_board = [
        [1, 2, 3],
        [4, 5, 6],
        [0, 7, 8]
    ]
    
    print("Trạng thái đầu:")
    medium_state = PuzzleState(medium_board)
    medium_state.print_board()
    print(f"Heuristic ban đầu: {medium_state.heuristic}")
    print(f"Có thể giải được: {'Có' if is_solvable(medium_board) else 'Không'}")
    
    start_time = time.time()
    solution2, depth2, nodes_expanded2 = greedy_best_first_search(medium_state)
    end_time = time.time()
    
    if solution2:
        print(f"\n✅ TÌM THẤY LỜI GIẢI!")
        print(f"Độ sâu: {depth2} bước")
        print(f"Số nút đã mở rộng: {nodes_expanded2}")
        print(f"Thời gian thực hiện: {end_time - start_time:.4f} giây")
        if depth2 <= 10:  # Chỉ hiển thị đường đi nếu ngắn
            print_solution_path(solution2)
    else:
        print(f"\n❌ KHÔNG TÌM THẤY LỜI GIẢI!")
        print(f"Số nút đã mở rộng: {nodes_expanded2}")
        print(f"Thời gian thực hiện: {end_time - start_time:.4f} giây")

    # Test case 3: Trạng thái khó hơn
    print("\n" + "=" * 50)
    print("TEST CASE 3: TRẠNG THÁI KHÓ HƠN")
    
    hard_board = [
        [2, 8, 3],
        [1, 6, 4],
        [7, 0, 5]
    ]
    
    print("Trạng thái đầu:")
    hard_state = PuzzleState(hard_board)
    hard_state.print_board()
    print(f"Heuristic ban đầu: {hard_state.heuristic}")
    print(f"Có thể giải được: {'Có' if is_solvable(hard_board) else 'Không'}")
    
    if is_solvable(hard_board):
        start_time = time.time()
        solution3, depth3, nodes_expanded3 = greedy_best_first_search(hard_state)
        end_time = time.time()
        
        if solution3:
            print(f"\n✅ TÌM THẤY LỜI GIẢI!")
            print(f"Độ sâu: {depth3} bước")
            print(f"Số nút đã mở rộng: {nodes_expanded3}")
            print(f"Thời gian thực hiện: {end_time - start_time:.4f} giây")
            print("(Đường đi quá dài, chỉ hiển thị trạng thái cuối)")
        else:
            print(f"\n❌ KHÔNG TÌM THẤY LỜI GIẢI TRONG GIỚI HẠN!")
            print(f"Số nút đã mở rộng: {nodes_expanded3}")
            print(f"Thời gian thực hiện: {end_time - start_time:.4f} giây")
    else:
        print("\n⚠️ TRẠNG THÁI KHÔNG THỂ GIẢI ĐƯỢC!")
        
    print("\n" + "=" * 50)
    print("KẾT LUẬN VỀ GREEDY BEST FIRST SEARCH:")
    print("- Thuật toán tham lam chỉ dựa vào heuristic h(n)")
    print("- Tốc độ nhanh nhưng không đảm bảo lời giải tối ưu") 
    print("- Có thể bị kẹt trong local optimum")
    print("- Thích hợp cho các bài toán cần giải pháp nhanh")

if __name__ == "__main__":
    main()
