import json
from config import TEST_SIZES


def generate_cross(n):
    n = int(n)
    if n % 2 == 0:
        print("홀수를 입력하세요.")
        return
    matrix = [[0] * n for _ in range(n)]
    mid_idx = n // 2
    for i in range(n):
        matrix[i][mid_idx] = 1
        matrix[mid_idx][i] = 1
    return matrix


def generate_x(n):
    n = int(n)
    if n % 2 == 0:
        print("홀수를 입력하세요.")
        return
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 1
        matrix[i][n - 1 - i] = 1
    return matrix


def generate_test_data(file_path):
    data = {
        "filters": {},
        "patterns": {}
    }
    for n in TEST_SIZES:
        cross = generate_cross(n)
        x = generate_x(n)
        data["filters"][f"size_{n}"] = {
            "cross": cross,
            "x": x
        }
        data["patterns"][f"size_{n}_1"] = {
            "input": cross,
            "expected": "+"
        }
        data["patterns"][f"size_{n}_2"] = {
            "input": x,
            "expected": "x"
        }
        # error case: invalid label
        data["patterns"][f"size_{n}_3"] = {
            "input": x,
            "expected": "T"
        }
        # error case: wrong matrix size; invalid label
        data["patterns"][f"size_{n}_4"] = {
            "input": [[0, 1], [1, 0]],
            "expected": "/"
        }
        # error case: wrong size
        data["patterns"][f"size_7_5"] = {
            "input": cross,
            "expected": "+"
        }
        # error case: missing size
        data["patterns"][f"size"] = {
            "input": cross,
            "expected": "+"
        }
        # error case: missing key
        data["patterns"][f"size"] = {
            "expected": "+"
        }


    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
