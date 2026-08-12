import json
import os


def generate_cross(n):
    return


def generate_x(n):
    matrix = []
    
    return


def generate_test_data(file_path):
    sizes = [5, 13, 25]
    data = {
        "filters": {},
        "patterns": {}
    }
    for n in sizes:
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
        json.dump(data, f, ensure_ascii=False, indent=2)

    return