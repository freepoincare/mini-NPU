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
        # normal case: Cross
        data["patterns"][f"size_{n}_1"] = {
            "input": cross,
            "expected": "+"
        }
        # normal case: X
        data["patterns"][f"size_{n}_2"] = {
            "input": x,
            "expected": "x"
        }
        # error case: invalid label
        data["patterns"][f"size_{n}_3"] = {
            "input": x,
            "expected": "T"
        }
        # error case: wrong matrix size
        data["patterns"][f"size_{n}_4"] = {
            "input": [[1, 1], [1, 1]],
            "expected": "x"
        }

    # Special schema-error cases
    # error case: key size mismatch
    data["patterns"][f"size_7_5"] = {
        "input": generate_cross(5),
        "expected": "+"
    }
    # error case: invalid key format
    data["patterns"][f"invalid_key_6"] = {
        "input": generate_cross(5),
        "expected": "+"
    }
    # error case: missing input
    data["patterns"][f"size_5_7"] = {
        "expected": "+"
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
