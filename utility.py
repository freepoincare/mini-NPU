import json
import time
from pattern_generator import generate_cross, generate_x
from config import REPEAT, EPSILON


def normalize_label(label):
    label = str(label).strip().lower()
    if label in ["+", "cross"]:
        return "Cross"
    if label == "x":
        return "X"
    if label in ["undecided", "tie", "draw"]:
        return "UNDECIDED"
    return None


def validate_matrix(matrix, n):
    if matrix is None or not isinstance(matrix, list) or len(matrix) != n:
        return False
    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            return False
        for v in row:
            if not isinstance(v, (int, float)) or v not in [0, 1]:
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
                    row.append(int(v))
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


# Performance measurement
def benchmark(pattern, filter_matrix, repeat=REPEAT):
    if repeat is None or repeat <= 0:
        raise ValueError("repeat must be >= 1")
    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        mac(pattern, filter_matrix)
        end = time.perf_counter()
        times.append((end - start) * 1000)
    return sum(times) / len(times)


def load_json(file_path):
    try: 
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
    except json.JSONDecodeError:
        print(f"❌ 올바른 JSON 파일이 아닙니다: {file_path}")
    except PermissionError:
        print(f"❌ 파일을 읽을 권한이 없습니다: {file_path}")
    except Exception as e:
        print(f"❌ 예상하지 못한 오류가 발생했습니다: {e}")
    return None


def clear_data(file_path):
    try:
        data = {"filters": {}, "patterns": {}}
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
    except PermissionError:
        print(f"❌ 파일을 쓸 권한이 없습니다: {file_path}")
    except Exception as e:
        print(f"❌ 예상하지 못한 오류가 발생했습니다: {e}")
    return None   # no need


def analyze_patterns(filters, patterns):
    """
    Validate and analyze patterns against filters.
    Checks include:
    - pattern key format (size_n_k)
    - pattern_data type
    - input existence/type
    - expected label validity
    - per-size filter existence/type
    - cross / x existence/type
    - matrix shape/value validity (validate_matrix)
    - tie rule (UNDECIDED => FAIL)
    - pass/fail counting + failed case logging
    """

    total_count, pass_count, fail_count = 0, 0, 0
    failed_cases = []

    for key, pattern_data in patterns.items():
        print(f"\n--- {key} ---")

        total_count += 1

        size = extract_size(key)

        if size is None:
            print(f"⚠️ {key}: FAIL - 잘못된 패턴 키 형식")  # invalid pattern key
            fail_count += 1
            failed_cases.append((key, "잘못된 패턴 키 형식"))
            continue

        if pattern_data is None or not isinstance(pattern_data, dict):
            print(f"⚠️ {key}: FAIL - 패턴 데이터가 올바르지 않음")  # invalid pattern data
            fail_count += 1
            failed_cases.append((key, "패턴 데이터가 올바르지 않음"))
            continue

        pattern = pattern_data.get("input")

        if pattern is None or not isinstance(pattern, list):
            print(f"⚠️ {key}: FAIL - 패턴 입력이 올바르지 않음")  # invalid pattern input
            fail_count += 1
            failed_cases.append((key, "패턴 입력이 올바르지 않음"))
            continue

        expected = normalize_label(pattern_data.get("expected"))

        if expected is None:
            print(f"⚠️ {key}: FAIL - expected 라벨이 올바르지 않음")    # invalid expected; missing expected
            fail_count += 1
            failed_cases.append((key, "expected 라벨이 올바르지 않음"))
            continue

        filter_data = filters.get(f"size_{size}")

        if filter_data is None or not isinstance(filter_data, dict):
            print(f"⚠️ {key}: FAIL - 필터 {size}x{size}가 존재하지 않거나 데이터 형식이 올바르지 않음")  # missing filter or invalid filter data
            fail_count += 1
            failed_cases.append((key, f"필터 {size}x{size}가 존재하지 않거나 데이터 형식이 올바르지 않음"))
            continue

        filter_cross = filter_data.get("cross")
        filter_x = filter_data.get("x")

        if filter_cross is None or not isinstance(filter_cross, list):
            print(f"⚠️ {key}: FAIL - cross 필터가 존재하지 않거나 데이터 형식이 올바르지 않음")   # missing cross or invalid data
            fail_count += 1
            failed_cases.append((key, "cross 필터가 존재하지 않거나 데이터 형식이 올바르지 않음"))
            continue

        if filter_x is None or not isinstance(filter_x, list):
            print(f"⚠️ {key}: FAIL - x 필터가 존재하지 않거나 데이터 형식이 올바르지 않음")   # missing x or invalid data
            fail_count += 1
            failed_cases.append((key, "x 필터가 존재하지 않거나 데이터 형식이 올바르지 않음"))
            continue

        if not validate_matrix(pattern, size):
            print(f"⚠️ {key}: FAIL - 패턴 크기 불일치 (기대: {size}x{size})")   # wrong matrix size
            fail_count += 1
            failed_cases.append((key, "패턴 크기 불일치"))
            continue

        if not validate_matrix(filter_cross, size):
            print(f"⚠️ {key}: FAIL - Cross 필터 크기 불일치 (기대: {size}x{size})")   # wrong matrix size
            fail_count += 1
            failed_cases.append((key, "Cross 필터 크기 불일치"))
            continue

        if not validate_matrix(filter_x, size):
            print(f"⚠️ {key}: FAIL - X 필터 크기 불일치 (기대: {size}x{size})")   # wrong matrix size
            fail_count += 1
            failed_cases.append((key, "X 필터 크기 불일치"))
            continue

        score_cross = mac(pattern, filter_cross)
        score_x = mac(pattern, filter_x)

        result = decide_label(score_cross, score_x)

        tie = ""
        if result == "UNDECIDED":
            status = "FAIL"
            tie = " (동점 규칙)"
            fail_count += 1
            failed_cases.append((key, "동점(UNDECIDED) 처리 규칙에 따라 FAIL")) 
        elif result == expected:
            status = "PASS"
            pass_count += 1
        else:
            status = "FAIL"
            fail_count += 1
            failed_cases.append((key, "expected 라벨과 다르므로 FAIL"))

        print(f"Cross 점수: {score_cross}")
        print(f"X 점수: {score_x}")
        print(f"판정: {result} | expected: {expected} | {status}{tie}")

    return total_count, pass_count, fail_count, failed_cases


def run_performance_analysis(filters, size_list=None, repeat=REPEAT):
    if size_list is None:
        size_list = [3, 5, 13, 25]

    # performance analysis for each filter size
    for size in size_list:
        filter_data = filters.get(f"size_{size}")

        if filter_data is None:
            if size in [3, 5, 13, 25]:
                filter_cross = generate_cross(size)
                filter_x = generate_x(size)
                #print(f"⚠️ size_{size}: JSON 데이터가 없어 기본 패턴을 생성하여 측정합니다.")
            else:
                print(f"⚠️ size_{size}: 지원하지 않는 크기이므로 건너뜁니다.")
                continue
        else:
            filter_cross = filter_data.get("cross")
            filter_x = filter_data.get("x")

            if filter_cross is None or filter_x is None:
                print(f"⚠️ size_{size}: 필터 키가 누락되어 건너뜁니다.")
                continue

        if not validate_matrix(filter_cross, size) or not validate_matrix(filter_x, size):
            print(f"⚠️ size_{size}: 필터 크기 불일치로 측정을 건너뜁니다.")
            continue

        # benchmark with a sample pattern (Cross)
        pattern = generate_cross(size)

        average_cross = benchmark(pattern, filter_cross, repeat=repeat)
        average_x = benchmark(pattern, filter_x, repeat=repeat)
        average_total = average_cross + average_x

        mac_operation = size * size

        size_str = f"{size}x{size}"
        print(f"{size_str:<10} {average_total:<20.3f} {mac_operation}")
    return