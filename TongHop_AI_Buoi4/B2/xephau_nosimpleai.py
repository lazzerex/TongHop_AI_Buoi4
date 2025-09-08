import random
import math

# ------------------------
# Lớp Bài toán 8 quân hậu
# ------------------------
class EightQueensProblem:
    def __init__(self, state=None, n=8):
        self.n = n
        if state is None:
            state = tuple(random.randint(0, n - 1) for _ in range(n))
        self.initial_state = state

    def value(self, state):
        """Hàm đánh giá: số cặp quân hậu không tấn công lẫn nhau"""
        non_attacking_pairs = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if not self.is_attacking(state, i, j):
                    non_attacking_pairs += 1
        return non_attacking_pairs

    def is_attacking(self, state, i, j):
        return (
            state[i] == state[j] or
            abs(state[i] - state[j]) == abs(i - j)
        )

    def neighbors(self, state):
        """Sinh ra tất cả các state láng giềng"""
        for col in range(self.n):
            for row in range(self.n):
                if row != state[col]:
                    new_state = list(state)
                    new_state[col] = row
                    yield tuple(new_state)

    def random_state(self):
        return tuple(random.randint(0, self.n - 1) for _ in range(self.n))

    def crossover(self, s1, s2):
        point = random.randint(1, self.n - 2)
        child1 = s1[:point] + s2[point:]
        child2 = s2[:point] + s1[point:]
        return child1, child2

    def mutate(self, state):
        s = list(state)
        col = random.randint(0, self.n - 1)
        s[col] = random.randint(0, self.n - 1)
        return tuple(s)


# ------------------------
# Các thuật toán
# ------------------------
def hill_climbing(problem, max_iter=1000):
    current = problem.initial_state
    for _ in range(max_iter):
        neighbors = list(problem.neighbors(current))
        if not neighbors:
            break
        neighbor = max(neighbors, key=problem.value)
        if problem.value(neighbor) <= problem.value(current):
            break
        current = neighbor
    return current


def simulated_annealing(problem, max_iter=1000, temp=1000, cooling=0.95):
    current = problem.initial_state
    for i in range(max_iter):
        T = temp * (cooling ** i)
        if T <= 0.0001:
            break
        neighbor = random.choice(list(problem.neighbors(current)))
        delta = problem.value(neighbor) - problem.value(current)
        if delta > 0 or random.random() < math.exp(delta / T):
            current = neighbor
    return current


def genetic_algorithm(problem, population_size=100, generations=200, mutation_rate=0.1):
    population = [problem.random_state() for _ in range(population_size)]

    for _ in range(generations):
        # Chọn lọc theo fitness
        population.sort(key=problem.value, reverse=True)
        next_gen = population[:10]  # elitism: giữ top 10

        while len(next_gen) < population_size:
            p1, p2 = random.sample(population[:50], 2)  # chọn từ top 50
            c1, c2 = problem.crossover(p1, p2)
            if random.random() < mutation_rate:
                c1 = problem.mutate(c1)
            if random.random() < mutation_rate:
                c2 = problem.mutate(c2)
            next_gen.extend([c1, c2])

        population = next_gen[:population_size]

    return max(population, key=problem.value)


# ------------------------
# Hàm hỗ trợ
# ------------------------
def print_board(state):
    n = len(state)
    print("\nBàn cờ 8x8:")
    print("  " + " ".join(str(i) for i in range(n)))
    for row in range(n):
        line = f"{row} "
        for col in range(n):
            line += "Q " if state[col] == row else ". "
        print(line)


def analyze(state, problem):
    conflicts = 28 - problem.value(state)
    print(f"Số conflict: {conflicts}")
    print(f"Giá trị hàm đánh giá: {problem.value(state)}/28")
    print_board(state)
    if conflicts == 0:
        print("Đã tìm được lời giải hoàn hảo!")
    else:
        print("Chưa tìm được lời giải hoàn hảo.")


# ------------------------
# Main
# ------------------------
if __name__ == "__main__":
    random.seed(40)

    print("=" * 60)
    print("HILL CLIMBING SEARCH")
    print("=" * 60)
    problem = EightQueensProblem()
    print(f"State ban đầu: {problem.initial_state}")
    print(f"Giá trị ban đầu: {problem.value(problem.initial_state)}/28")
    sol1 = hill_climbing(problem)
    print(f"Kết quả: {sol1}")
    analyze(sol1, problem)

    print("\n" + "=" * 60)
    print("SIMULATED ANNEALING SEARCH")
    print("=" * 60)
    problem2 = EightQueensProblem()
    print(f"State ban đầu: {problem2.initial_state}")
    print(f"Giá trị ban đầu: {problem2.value(problem2.initial_state)}/28")
    sol2 = simulated_annealing(problem2)
    print(f"Kết quả: {sol2}")
    analyze(sol2, problem2)

    print("\n" + "=" * 60)
    print("GENETIC ALGORITHM SEARCH")
    print("=" * 60)
    print("Genetic Algorithm khởi tạo quần thể ngẫu nhiên, không cần state ban đầu cụ thể")
    sol3 = genetic_algorithm(problem)
    print(f"Kết quả: {sol3}")
    analyze(sol3, problem)
