import json
import time

from pattern_generator import generate_cross


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
                    raise ValueError(f"각 줄에 정확히 {n}개의 숫자를 공백으로 구분하여 입력하세요.")
                # check the value (0 or 1)
                row = []
                for v in values:
                    if not v.isdigit() or int(v) not in [0, 1]:
                        raise ValueError(f"0 또는 1을 입력하세요.")
                    row.append(float(v))
                matrix.append(row)
            return matrix
        except ValueError as e:
            print(f"\n⚠️ 입력 오류: {e} 처음부터 다시 입력해주세요.")
            time.sleep(1)


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
    parts = key.split("_")
    return int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None


def benchmark(pattern, filter_matrix, repeat=REPEAT):
    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        mac(pattern, filter_matrix)
        end = time.perf_counter()
        times.append((end - start) * 1000)
    return sum(times) / len(times)


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def run_performance_analysis(filters, size_list=[3, 5, 13, 25], repeat=REPEAT):
    # performance analysis for each filter size
    for size in size_list:
        filter_data = filters.get(f"size_{size}")
        filter_cross = filter_data["cross"]
        filter_x = filter_data["x"]

        # benchmark with a sample pattern (Cross)
        pattern = generate_cross(size)
        average_cross = benchmark(pattern, filter_cross)
        average_x = benchmark(pattern, filter_x)
        average_total = average_cross + average_x

        print(f"{size:<10} {average_total:<20.3f} {repeat * 2}")
    return