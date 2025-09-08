import random
import math

# ------------------------
# Bài toán 8 quân hậu
# ------------------------
class EightQueensProblem:
    def __init__(self, n=8):
        self.n = n

    def value(self, state):
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

    def random_state(self):
        return [random.randint(0, self.n - 1) for _ in range(self.n)]


# ------------------------
# Ant Colony Optimization (ACO)
# ------------------------
def ant_colony_optimization(problem, num_ants=30, max_iter=200, alpha=1, beta=2, rho=0.5, Q=100):
    n = problem.n
    pheromone = [[1.0 for _ in range(n)] for _ in range(n)]

    best_state = None
    best_score = -1

    for _ in range(max_iter):
        solutions = []
        scores = []

        for _ in range(num_ants):
            state = []
            for col in range(n):
                probs = [pheromone[col][row] ** alpha for row in range(n)]
                s = sum(probs)
                probs = [p / s for p in probs]
                row = random.choices(range(n), probs)[0]
                state.append(row)

            score = problem.value(state)
            solutions.append(state)
            scores.append(score)

            if score > best_score:
                best_state = state[:]
                best_score = score

        # Bốc hơi pheromone
        for col in range(n):
            for row in range(n):
                pheromone[col][row] *= (1 - rho)

        # Cập nhật pheromone
        for state, score in zip(solutions, scores):
            for col, row in enumerate(state):
                pheromone[col][row] += Q * (score / 28.0)

        if best_score == 28:
            break

    return best_state, best_score


# ------------------------
# Artificial Bee Colony (ABC)
# ------------------------
def bee_colony(problem, population_size=30, max_iter=200, limit=50):
    population = [problem.random_state() for _ in range(population_size)]
    fitness = [problem.value(ind) for ind in population]
    trial = [0] * population_size

    best_state = population[fitness.index(max(fitness))][:]
    best_score = max(fitness)

    for _ in range(max_iter):
        # Employed bees
        for i in range(population_size):
            k = random.randint(0, population_size - 1)
            while k == i:
                k = random.randint(0, population_size - 1)
            j = random.randint(0, problem.n - 1)

            new = population[i][:]
            new[j] = population[i][j] if random.random() > 0.5 else population[k][j]
            new_score = problem.value(new)

            if new_score > fitness[i]:
                population[i] = new
                fitness[i] = new_score
                trial[i] = 0
            else:
                trial[i] += 1

        # Onlooker bees
        probs = [f / sum(fitness) for f in fitness]
        for _ in range(population_size):
            i = random.choices(range(population_size), probs)[0]
            k = random.randint(0, population_size - 1)
            while k == i:
                k = random.randint(0, population_size - 1)
            j = random.randint(0, problem.n - 1)

            new = population[i][:]
            new[j] = population[i][j] if random.random() > 0.5 else population[k][j]
            new_score = problem.value(new)

            if new_score > fitness[i]:
                population[i] = new
                fitness[i] = new_score
                trial[i] = 0
            else:
                trial[i] += 1

        # Scout bees
        for i in range(population_size):
            if trial[i] > limit:
                population[i] = problem.random_state()
                fitness[i] = problem.value(population[i])
                trial[i] = 0

        # Cập nhật best
        idx = fitness.index(max(fitness))
        if fitness[idx] > best_score:
            best_score = fitness[idx]
            best_state = population[idx][:]

        if best_score == 28:
            break

    return best_state, best_score


# ------------------------
# Gray Wolf Optimizer (GWO)
# ------------------------
def gray_wolf_optimizer(problem, population_size=30, max_iter=200):
    wolves = [problem.random_state() for _ in range(population_size)]
    fitness = [problem.value(w) for w in wolves]

    best_state = wolves[fitness.index(max(fitness))][:]
    best_score = max(fitness)

    for t in range(max_iter):
        a = 2 - 2 * (t / max_iter)

        sorted_wolves = sorted(zip(wolves, fitness), key=lambda x: x[1], reverse=True)
        alpha, beta, delta = sorted_wolves[:3]
        alpha, beta, delta = alpha[0], beta[0], delta[0]

        new_wolves = []
        for i in range(population_size):
            wolf = wolves[i][:]
            new = []
            for j in range(problem.n):
                r1, r2 = random.random(), random.random()
                A1 = 2 * a * r1 - a
                C1 = 2 * r2
                D_alpha = abs(C1 * alpha[j] - wolf[j])
                X1 = alpha[j] - A1 * D_alpha

                r1, r2 = random.random(), random.random()
                A2 = 2 * a * r1 - a
                C2 = 2 * r2
                D_beta = abs(C2 * beta[j] - wolf[j])
                X2 = beta[j] - A2 * D_beta

                r1, r2 = random.random(), random.random()
                A3 = 2 * a * r1 - a
                C3 = 2 * r2
                D_delta = abs(C3 * delta[j] - wolf[j])
                X3 = delta[j] - A3 * D_delta

                X = (X1 + X2 + X3) / 3
                new.append(int(max(0, min(problem.n - 1, X))))
            new_wolves.append(new)

        wolves = new_wolves
        fitness = [problem.value(w) for w in wolves]

        idx = fitness.index(max(fitness))
        if fitness[idx] > best_score:
            best_score = fitness[idx]
            best_state = wolves[idx][:]

        if best_score == 28:
            break

    return best_state, best_score


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


def analyze(state, score):
    print(f"Giá trị hàm đánh giá: {score}/28")
    print_board(state)
    if score == 28:
        print("Đã tìm được lời giải hoàn hảo!")
    else:
        print("Chưa tìm được lời giải hoàn hảo.")


# ------------------------
# Main
# ------------------------
if __name__ == "__main__":
    random.seed(42)
    problem = EightQueensProblem()

    print("=" * 60)
    print("ANT COLONY OPTIMIZATION (ACO)")
    print("=" * 60)
    state, score = ant_colony_optimization(problem)
    print(f"Kết quả: {state}")
    analyze(state, score)

    print("\n" + "=" * 60)
    print("BEE COLONY (BCO)")
    print("=" * 60)
    state, score = bee_colony(problem)
    print(f"Kết quả: {state}")
    analyze(state, score)

    print("\n" + "=" * 60)
    print("GRAY WOLF OPTIMIZER (GWO)")
    print("=" * 60)
    state, score = gray_wolf_optimizer(problem)
    print(f"Kết quả: {state}")
    analyze(state, score)
