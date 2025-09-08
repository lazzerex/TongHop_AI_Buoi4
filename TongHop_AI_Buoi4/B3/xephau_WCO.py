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
# Whale Optimization Algorithm (WCO)
# ------------------------
def whale_optimization(problem, population_size=30, max_iter=200, b=1.5):
    # Khởi tạo quần thể
    whales = [problem.random_state() for _ in range(population_size)]
    fitness = [problem.value(w) for w in whales]

    # Xác định con mồi (tốt nhất hiện tại)
    best_whale = whales[fitness.index(max(fitness))][:]
    best_score = max(fitness)

    for t in range(max_iter):
        a = 2 - 2 * (t / max_iter)  # giảm dần từ 2 -> 0

        for i in range(population_size):
            r1 = random.random()
            r2 = random.random()
            A = 2 * a * r1 - a
            C = 2 * r2
            p = random.random()

            whale = whales[i][:]

            if p < 0.5:
                if abs(A) < 1:
                    # Khai thác quanh best whale
                    for j in range(problem.n):
                        D = abs(C * best_whale[j] - whale[j])
                        whale[j] = int(best_whale[j] - A * D)
                else:
                    # Khám phá ngẫu nhiên
                    rand_whale = whales[random.randint(0, population_size - 1)]
                    for j in range(problem.n):
                        D = abs(C * rand_whale[j] - whale[j])
                        whale[j] = int(rand_whale[j] - A * D)
            else:
                # Vòng xoáy (spiral update)
                l = random.uniform(-1, 1)
                for j in range(problem.n):
                    D = abs(best_whale[j] - whale[j])
                    whale[j] = int(
                        D * math.exp(b * l) * math.cos(2 * math.pi * l)
                        + best_whale[j]
                    )

            # Đảm bảo trong phạm vi [0, n-1]
            whale = [max(0, min(problem.n - 1, x)) for x in whale]

            # Cập nhật
            whales[i] = whale
            score = problem.value(whale)
            if score > best_score:
                best_score = score
                best_whale = whale[:]

        # Nếu đã tìm được nghiệm hoàn hảo thì dừng
        if best_score == 28:
            break

    return best_whale, best_score


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


# ------------------------
# Main
# ------------------------
if __name__ == "__main__":

    # for s in range(1000):  # thử seed
        #random.seed(s)
        #problem = EightQueensProblem()
        #best_state, best_score = whale_optimization(problem)
        #if best_score == 28:
            #print("Seed tìm được:", s)
            #print("State:", best_state)
            #break
        
    random.seed(113)
    problem = EightQueensProblem()

    print("=" * 60)
    print("WHALE OPTIMIZATION ALGORITHM (WCO) SEARCH")
    print("=" * 60)

    best_state, best_score = whale_optimization(problem)

    print(f"Kết quả: {best_state}")
    print(f"Giá trị hàm đánh giá: {best_score}/28")
    print_board(best_state)

    if best_score == 28:
        print("Đã tìm được lời giải hoàn hảo!")
    else:
        print("Chưa tìm được lời giải hoàn hảo.")
