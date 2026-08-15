from pathlib import Path
from config import DATA_FILE_PATH, EPSILON, REPEAT
from utility import *


def run_user_mode(n):
    # Filter
    print("\n" + "=" * 18)
    print("[1] 필터 입력")
    print("=" * 18)
    filter_a = input_matrix(n, "필터 A")
    print("")
    filter_b = input_matrix(n, "필터 B")

    # Pattern
    print("\n" + "=" * 18)
    print("[2] 패턴 입력")
    print("=" * 18)
    pattern = input_matrix(n, "패턴")

    # MAC
    print("\n" + "=" * 18)
    print("[3] MAC 결과")
    print("=" * 18)
    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")

    if abs(score_a - score_b) < EPSILON:
        print(f"판정: 판정 불가 (|A - B| < {EPSILON})")
        time.sleep(1)
        return
    
    # Performance measurement
    average_a = benchmark(pattern, filter_a)
    average_b = benchmark(pattern, filter_b)
    average = average_a + average_b
    print(f"연산 시간(평균/{REPEAT}회): {average:.3f} ms")

    # Decision
    if score_a > score_b:
        print("판정: A")
    else:
        print("판정: B")
    time.sleep(1)


def run_json_mode():
    print("\n" + "=" * 18)
    print("[1] 필터 로드")
    print("=" * 18)

    data = load_json(DATA_FILE_PATH)

    filters = data["filters"]
    patterns = data["patterns"]

    print(f"✅ size_5 필터 로드 완료 (Cross, X)")
    print(f"✅ size_13 필터 로드 완료 (Cross, X)")
    print(f"✅ size_25 필터 로드 완료 (Cross, X)")

    time.sleep(1)

    print("\n" + "=" * 18)
    print("[2] 패턴 분석 (라벨 정규화 적용)")
    print("=" * 18)

    total_count, pass_count, fail_count = 0, 0, 0

    for key, pattern_data in patterns.items():
        total_count += 1

        size = extract_size(key)
        pattern = pattern_data["input"]
        expected = normalize_label(pattern_data["expected"])

        filter_data = filters.get(f"size_{size}")
        filter_cross = filter_data["cross"]
        filter_x = filter_data["x"]

        if not validate_matrix(pattern, size):
            print(f"⚠️ {key}: FAIL - 패턴 크기 불일치 (기대: {size}x{size})")
            fail_count += 1
            continue

        if not validate_matrix(filter_cross, size):
            print(f"⚠️ {key}: FAIL - Cross 필터 크기 불일치 (기대: {size}x{size})")
            fail_count += 1
            continue

        if not validate_matrix(filter_x, size):
            print(f"⚠️ {key}: FAIL - X 필터 크기 불일치 (기대: {size}x{size})")
            fail_count += 1
            continue

        score_cross = mac(pattern, filter_cross)
        score_x = mac(pattern, filter_x)

        result = decide_label(score_cross, score_x)
        
        if result == expected:
            status = "PASS"
            pass_count += 1
        else:
            status = "FAIL"
            fail_count += 1

        print(f"\n--- {key} ---")
        print(f"Cross 점수: {score_cross}")
        print(f"X 점수: {score_x}")
        tie = ""
        if result == "UNDECIDED":
            tie = " (동점 규칙)"
        print(f"판정: {result} | expected: {expected} | {status}{tie}")

    time.sleep(1)

    print("\n" + "=" * 18)
    print("[3] 성능 분석 (평균/10회)")
    print("=" * 18)
    print("크기      평균 시간 (ms)     연산 횟수")
    print("=" * 18)

    run_performance_analysis(filters, size_list=[3, 5, 13, 25])

    time.sleep(1)

    print("\n" + "=" * 18)
    print("[4] 결과 요약")
    print("=" * 18)
    print(f"총 테스트: {total_count}개")
    print(f"통과: {pass_count}개")
    print(f"실패: {fail_count}개")
    print(f"\n실패 케이스:")
    for i in range(fail_count):
        continue

    time.sleep(1)