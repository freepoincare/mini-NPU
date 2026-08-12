import time

EPSILON = 1e-9
REPEAT = 10


def normalize_label(label):
    label = str(label).strip().lower()
    if label in ["+", "cross"]:
        return "Cross"
    if label == "x":
        return "X"
    return None


def validate_matrix(matrix, n):
    if len(matrix) != n:
        return False
    for row in matrix:
        if len(row) != n:
            return False
    return True


def input_matrix(n, name):
    while True:
        print(f"{name} ({n}x{n}, {n}줄 입력, 공백 구분):")
        matrix = []
        try:
            for i in range(n):
                values = input(f"Row {i + 1}: ").split()
                # check number of elements
                if len(values) != n:
                    raise ValueError(f"각 줄에 정확히 {n}개의 숫자를 입력하세요.")
                # check the value (0 or 1)
                row = []
                for v in values:
                    if not v.isdigit() or int(v) not in [0, 1]:
                        raise ValueError(f"0 또는 1을 입력하세요.")
                    row.append(float(v))
                matrix.append(row)
            return matrix
        except ValueError as e:
            print(f"⚠️ 입력 오류: {e} 처음부터 다시 입력해주세요.")


def mac(pattern, filter_matrix):
    n = len(pattern)
    score = 0.0
    for i in range(n):
        for j in range(n):
            score += pattern[i][j] * filter_matrix[i][j]
    return score


def decide_label(score_cross, score_x):
    if abs(score_cross - score_x) < EPSILON:
        return "UNDECIDED"
    if score_cross > score_x:
        return "Cross"
    return "X"


def extract_size(key):
    return


def benchmark(pattern, filter_matrix, repeat=REPEAT):
    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        mac(pattern, filter_matrix)
        end = time.perf_counter()
        times.append((end - start) * 1000)
    return sum(times) / len(times)


def load_json(filename):
    return

