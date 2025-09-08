from simpleai.search import SearchProblem
from simpleai.search.local import hill_climbing, simulated_annealing, genetic
import random
import math

class EightQueensProblem(SearchProblem):
    """
    Bài toán 8 quân hậu sử dụng các thuật toán local search
    
    State representation: tuple 8 phần tử, mỗi phần tử là vị trí hàng của quân hậu trong cột tương ứng
    Ví dụ: (0, 4, 7, 5, 2, 6, 1, 3) có nghĩa là:
    - Cột 0: quân hậu ở hàng 0
    - Cột 1: quân hậu ở hàng 4
    - ...
    """
    
    def __init__(self, initial_state=None):
        # Tạo state ngẫu nhiên nếu không có initial_state
        if initial_state is None:
            initial_state = tuple(random.randint(0, 7) for _ in range(8))
        super().__init__(initial_state)
    
    def actions(self, state):
        """
        Trả về tất cả các action có thể từ state hiện tại
        Action: (cột, hàng_mới) - di chuyển quân hậu ở cột đến hàng_mới
        """
        actions = []
        for col in range(8):
            for new_row in range(8):
                if new_row != state[col]:  # Chỉ di chuyển đến vị trí khác
                    actions.append((col, new_row))
        return actions
    
    def result(self, state, action):
        """
        Trả về state mới sau khi thực hiện action
        """
        col, new_row = action
        new_state = list(state)
        new_state[col] = new_row
        return tuple(new_state)
    
    def value(self, state):
        """
        Hàm đánh giá: số cặp quân hậu không tấn công lẫn nhau
        Giá trị cao hơn = tốt hơn
        Giá trị tối đa = 28 (tổng số cặp có thể = 8*7/2 = 28)
        """
        non_attacking_pairs = 0
        n = len(state)
        
        # Kiểm tra tất cả các cặp quân hậu
        for i in range(n):
            for j in range(i + 1, n):
                # Kiểm tra xem 2 quân hậu có tấn công nhau không
                if not self.is_attacking(state, i, j):
                    non_attacking_pairs += 1
        
        return non_attacking_pairs
    
    def is_attacking(self, state, i, j):
        """
        Kiểm tra xem 2 quân hậu ở cột i và j có tấn công nhau không
        """
        # Cùng hàng
        if state[i] == state[j]:
            return True
        
        # Cùng đường chéo
        if abs(state[i] - state[j]) == abs(i - j):
            return True
        
        return False
    
    def generate_random_state(self):
        """
        Tạo state ngẫu nhiên cho genetic algorithm
        """
        return tuple(random.randint(0, 7) for _ in range(8))
    
    def crossover(self, state1, state2):
        """
        Lai ghép 2 state để tạo state mới cho genetic algorithm
        Trả về 1 state con duy nhất (để tương thích simpleai)
        """
        crossover_point = random.randint(1, 6)
        child1 = state1[:crossover_point] + state2[crossover_point:]
        child2 = state2[:crossover_point] + state1[crossover_point:]
        # Trả về ngẫu nhiên một trong hai con
        return random.choice([child1, child2])
    
    def mutate(self, state):
        """
        Đột biến state cho genetic algorithm
        """
        state = list(state)
        mutate_col = random.randint(0, 7)
        state[mutate_col] = random.randint(0, 7)
        return tuple(state)


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


def analyze_solution(state):
    """
    Phân tích solution và đếm số conflict
    """
    conflicts = 0
    n = len(state)
    
    for i in range(n):
        for j in range(i + 1, n):
            # Cùng hàng
            if state[i] == state[j]:
                conflicts += 1
            # Cùng đường chéo
            elif abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    
    print(f"Số conflicts: {conflicts}")
    print(f"Giá trị hàm đánh giá: {28 - conflicts}/28")
    
    if conflicts == 0:
        print("Đã tìm được lời giải hoàn hảo!")
    else:
        print("Chưa tìm được lời giải hoàn hảo")
    
    return conflicts == 0


def solve_with_hill_climbing():
    """
    Giải bài toán bằng Hill Climbing
    """
    print("=" * 60)
    print("HILL CLIMBING SEARCH")
    print("=" * 60)
    
    problem = EightQueensProblem()
    print(f"State ban đầu: {problem.initial_state}")
    print(f"Giá trị ban đầu: {problem.value(problem.initial_state)}/28")
    
    result = hill_climbing(problem, iterations_limit=1000)
    
    print(f"\nKết quả: {result.state}")
    print_board(result.state)
    
    is_perfect = analyze_solution(result.state)
    return result.state, is_perfect


def solve_with_simulated_annealing():
    """
    Giải bài toán bằng Simulated Annealing
    """
    print("=" * 60)
    print("SIMULATED ANNEALING SEARCH")
    print("=" * 60)
    
    def custom_schedule(t):
        """Schedule function cho simulated annealing"""
        return math.exp(-t / 100)
    
    problem = EightQueensProblem()
    print(f"State ban đầu: {problem.initial_state}")
    print(f"Giá trị ban đầu: {problem.value(problem.initial_state)}/28")
    
    result = simulated_annealing(problem, schedule=custom_schedule, iterations_limit=1000)
    
    print(f"\nKết quả: {result.state}")
    print_board(result.state)
    
    is_perfect = analyze_solution(result.state)
    return result.state, is_perfect


def solve_with_genetic():
    """
    Giải bài toán bằng Genetic Algorithm
    """
    print("=" * 60)
    print("GENETIC ALGORITHM SEARCH")
    print("=" * 60)
    
    # Genetic Algorithm không cần initial_state, nó sẽ tự tạo quần thể
    problem = EightQueensProblem((0, 0, 0, 0, 0, 0, 0, 0))  # Dummy initial state
    print("Genetic Algorithm không cần state ban đầu cụ thể")
    
    result = genetic(problem, population_size=100, mutation_chance=0.1, iterations_limit=100)
    
    print(f"\nKết quả: {result.state}")
    print_board(result.state)
    
    is_perfect = analyze_solution(result.state)
    return result.state, is_perfect


def main():
    """
    Chạy tất cả các thuật toán và so sánh kết quả
    """
    print("BÀI TOÁN 8 QUÂN HẬU VỚI SIMPLEAI LOCAL SEARCH")
    print("=" * 80)
    
    results = {}
    
    # Hill Climbing
    try:
        state_hc, perfect_hc = solve_with_hill_climbing()
        results['Hill Climbing'] = (state_hc, perfect_hc)
    except Exception as e:
        print(f"Lỗi Hill Climbing: {e}")
        results['Hill Climbing'] = (None, False)
    
    # Simulated Annealing
    try:
        state_sa, perfect_sa = solve_with_simulated_annealing()
        results['Simulated Annealing'] = (state_sa, perfect_sa)
    except Exception as e:
        print(f"Lỗi Simulated Annealing: {e}")
        results['Simulated Annealing'] = (None, False)
    
    # Genetic Algorithm
    try:
        state_ga, perfect_ga = solve_with_genetic()
        results['Genetic Algorithm'] = (state_ga, perfect_ga)
    except Exception as e:
        print(f"Lỗi Genetic Algorithm: {e}")
        results['Genetic Algorithm'] = (None, False)
    
    # Tổng kết
    print("\n" + "=" * 80)
    print("TỔNG KẾT KẾT QUẢ")
    print("=" * 80)
    
    for algorithm, (state, is_perfect) in results.items():
        if state:
            status = "Thành công" if is_perfect else "Chưa hoàn hảo"
            print(f"{algorithm:20}: {status} - {state}")
        else:
            print(f"{algorithm:20}: Lỗi")
    
    # Hiển thị một lời giải hoàn hảo nếu có
    perfect_solutions = [(alg, state) for alg, (state, perfect) in results.items() if perfect and state]
    if perfect_solutions:
        print(f"\nLời giải hoàn hảo từ {perfect_solutions[0][0]}:")
        print_board(perfect_solutions[0][1])
    else:
        print("\nKhông tìm được lời giải hoàn hảo từ các thuật toán trên")
        print("Thử chạy lại với các tham số khác hoặc nhiều lần hơn")


if __name__ == "__main__":
    # Thiết lập seed cho reproducible results
    random.seed(42)
    main()
