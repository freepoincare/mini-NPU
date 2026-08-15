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

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# def validate_test_data():
#     with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
#         data = json.load(f)

#     for n in TEST_SIZES:
#         filter_key = f"size_{n}"
#         pattern_key = f"size_{n}_1"
#         pattern_key_2 = f"size_{n}_2"
#         if filter_key not in data["filters"]:
#             return False
#         if pattern_key not in data["patterns"]:
#             return False
#         if pattern_key_2 not in data["patterns"]:
#             return False

#         cross = data["filters"][filter_key]["cross"]
#         x = data["filters"][filter_key]["x"]

#         if not validate_matrix(cross, n):
#             return False
#         if not validate_matrix(x, n):
#             return False

#     return True