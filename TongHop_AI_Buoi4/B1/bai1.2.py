"""
Bài toán 8-puzzle sử dụng thuật toán A* Search
Thuật toán này sử dụng f(n) = g(n) + h(n) để đánh giá các trạng thái
g(n): chi phí từ trạng thái đầu đến trạng thái hiện tại
h(n): hàm heuristic (Manhattan distance)
"""

import heapq
from collections import deque
import time

class PuzzleState:
    def __init__(self, board, parent=None, move=None, g_cost=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.g_cost = g_cost  # Chi phí từ trạng thái đầu
        self.h_cost = self.calculate_manhattan_distance()  # Heuristic
        self.f_cost = self.g_cost + self.h_cost  # Tổng chi phí
    
    def __lt__(self, other):
        if self.f_cost == other.f_cost:
            return self.h_cost < other.h_cost  # Tie-breaking bằng heuristic
        return self.f_cost < other.f_cost
    
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
                
                # Chi phí g tăng 1 cho mỗi bước di chuyển
                successor = PuzzleState(new_board, self, move_name, self.g_cost + 1)
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

def a_star_search(initial_state):
    """
    Thuật toán A* Search
    Sử dụng f(n) = g(n) + h(n) để chọn nút tối ưu
    """
    if initial_state.is_goal():
        return initial_state, 0, 1
    
    # Priority queue với f_cost làm priority
    open_list = []
    heapq.heappush(open_list, initial_state)
    
    # Dictionary để theo dõi chi phí tốt nhất đến mỗi trạng thái
    best_g_cost = {hash(initial_state): initial_state.g_cost}
    
    # Set để theo dõi các trạng thái đã được xử lý hoàn toàn
    closed_set = set()
    
    nodes_expanded = 0
    max_nodes = 200000  # Giới hạn để tránh chạy quá lâu
    
    while open_list and nodes_expanded < max_nodes:
        current_state = heapq.heappop(open_list)
        
        # Bỏ qua nếu đã tìm thấy đường đi tốt hơn đến trạng thái này
        if hash(current_state) in closed_set:
            continue
            
        if current_state.g_cost > best_g_cost.get(hash(current_state), float('inf')):
            continue
            
        closed_set.add(hash(current_state))
        nodes_expanded += 1
        
        if current_state.is_goal():
            return current_state, current_state.g_cost, nodes_expanded
        
        # Tạo các trạng thái kế tiếp
        successors = current_state.get_successors()
        
        for successor in successors:
            if hash(successor) in closed_set:
                continue
                
            # Kiểm tra xem có tìm thấy đường đi tốt hơn không
            successor_hash = hash(successor)
            if successor_hash not in best_g_cost or successor.g_cost < best_g_cost[successor_hash]:
                best_g_cost[successor_hash] = successor.g_cost
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
        print(f"g(n) = {state.g_cost}, h(n) = {state.h_cost}, f(n) = {state.f_cost}")
        print("-" * 20)

def compare_heuristics(initial_state):
    """So sánh hiệu quả của các hàm heuristic khác nhau"""
    print("\n=== SO SÁNH CÁC HÀM HEURISTIC ===")
    
    # Hàm heuristic 1: Manhattan Distance (đã sử dụng)
    print("1. Manhattan Distance (hiện tại):", initial_state.h_cost)
    
    # Hàm heuristic 2: Misplaced Tiles
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    misplaced = 0
    for i in range(3):
        for j in range(3):
            if initial_state.board[i][j] != 0 and initial_state.board[i][j] != goal[i][j]:
                misplaced += 1
    print("2. Misplaced Tiles:", misplaced)
    
    # Hàm heuristic 3: Linear Conflicts + Manhattan
    def linear_conflicts(board):
        conflicts = 0
        # Kiểm tra xung đột hàng ngang
        for i in range(3):
            for j in range(3):
                if board[i][j] != 0:
                    target_row = (board[i][j] - 1) // 3
                    if target_row == i:  # Số này thuộc hàng đúng
                        for k in range(j + 1, 3):
                            if board[i][k] != 0:
                                target_row_k = (board[i][k] - 1) // 3
                                if target_row_k == i and board[i][k] < board[i][j]:
                                    conflicts += 1
        
        # Kiểm tra xung đột hàng dọc
        for j in range(3):
            for i in range(3):
                if board[i][j] != 0:
                    target_col = (board[i][j] - 1) % 3
                    if target_col == j:  # Số này thuộc cột đúng
                        for k in range(i + 1, 3):
                            if board[k][j] != 0:
                                target_col_k = (board[k][j] - 1) % 3
                                if target_col_k == j and board[k][j] < board[i][j]:
                                    conflicts += 1
        
        return conflicts * 2  # Mỗi xung đột cần ít nhất 2 bước để giải quyết
    
    linear_conflict_cost = initial_state.h_cost + linear_conflicts(initial_state.board)
    print("3. Manhattan + Linear Conflicts:", linear_conflict_cost)

def main():
    print("A* SEARCH - BÀI TOÁN 8-PUZZLE")
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
    print(f"g(n) = {easy_state.g_cost}, h(n) = {easy_state.h_cost}, f(n) = {easy_state.f_cost}")
    print(f"Có thể giải được: {'Có' if is_solvable(easy_board) else 'Không'}")
    
    # So sánh các hàm heuristic
    compare_heuristics(easy_state)
    
    start_time = time.time()
    solution1, cost1, nodes_expanded1 = a_star_search(easy_state)
    end_time = time.time()
    
    if solution1:
        print(f"\n✅ TÌM THẤY LỜI GIẢI TỐI ƯU!")
        print(f"Chi phí tối ưu: {cost1} bước")
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
    print(f"g(n) = {medium_state.g_cost}, h(n) = {medium_state.h_cost}, f(n) = {medium_state.f_cost}")
    print(f"Có thể giải được: {'Có' if is_solvable(medium_board) else 'Không'}")
    
    start_time = time.time()
    solution2, cost2, nodes_expanded2 = a_star_search(medium_state)
    end_time = time.time()
    
    if solution2:
        print(f"\n✅ TÌM THẤY LỜI GIẢI TỐI ƯU!")
        print(f"Chi phí tối ưu: {cost2} bước")
        print(f"Số nút đã mở rộng: {nodes_expanded2}")
        print(f"Thời gian thực hiện: {end_time - start_time:.4f} giây")
        if cost2 <= 10:  # Chỉ hiển thị đường đi nếu ngắn
            print_solution_path(solution2)
        else:
            print("(Đường đi quá dài, chỉ hiển thị trạng thái cuối)")
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
    print(f"g(n) = {hard_state.g_cost}, h(n) = {hard_state.h_cost}, f(n) = {hard_state.f_cost}")
    print(f"Có thể giải được: {'Có' if is_solvable(hard_board) else 'Không'}")
    
    if is_solvable(hard_board):
        start_time = time.time()
        solution3, cost3, nodes_expanded3 = a_star_search(hard_state)
        end_time = time.time()
        
        if solution3:
            print(f"\n✅ TÌM THẤY LỜI GIẢI TỐI ƯU!")
            print(f"Chi phí tối ưu: {cost3} bước")
            print(f"Số nút đã mở rộng: {nodes_expanded3}")
            print(f"Thời gian thực hiện: {end_time - start_time:.4f} giây")
            print("(Đường đi quá dài, chỉ hiển thị trạng thái cuối)")
            print("Trạng thái cuối:")
            solution3.print_board()
        else:
            print(f"\n❌ KHÔNG TÌM THẤY LỜI GIẢI TRONG GIỚI HẠN!")
            print(f"Số nút đã mở rộng: {nodes_expanded3}")
            print(f"Thời gian thực hiện: {end_time - start_time:.4f} giây")
    else:
        print("\n⚠️ TRẠNG THÁI KHÔNG THỂ GIẢI ĐƯỢC!")
        
    print("\n" + "=" * 50)
    print("KẾT LUẬN VỀ THUẬT TOÁN A*:")
    print("- A* đảm bảo tìm được lời giải tối ưu nhất")
    print("- Sử dụng f(n) = g(n) + h(n) để đánh giá toàn diện")
    print("- Hiệu quả và chính xác hơn Greedy Best First Search")
    print("- Thời gian có thể lâu hơn nhưng đảm bảo chất lượng")

if __name__ == "__main__":
    main()
