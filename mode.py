import time
from config import DATA_FILE_PATH, EPSILON, REPEAT
from utility import input_matrix, mac, benchmark, load_json, extract_size, normalize_label, validate_matrix, decide_label, run_performance_analysis


def run_user_mode(n):
    # Filter
    print("\n" + "=" * 36)
    print("[1] 필터 입력")
    print("=" * 36)
    filter_a = input_matrix(n, "필터 A")
    print("")
    filter_b = input_matrix(n, "필터 B")

    # Pattern
    print("\n" + "=" * 36)
    print("[2] 패턴 입력")
    print("=" * 36)
    pattern = input_matrix(n, "패턴")

    # MAC
    print("\n" + "=" * 36)
    print("[3] MAC 결과")
    print("=" * 36)
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
    print(f"총 연산 시간(평균/{REPEAT}회): {average:.3f} ms")
    print(f"A 평균 시간: {average_a:.3f} ms")
    print(f"B 평균 시간: {average_b:.3f} ms")


    # Decision
    if score_a > score_b:
        print("판정: A")
    else:
        print("판정: B")
    time.sleep(1)


def run_json_mode():
    print("\n" + "=" * 36)
    print("[1] 필터 로드")
    print("=" * 36)

    data = load_json(DATA_FILE_PATH)

    if data is None:
        print("❌ data.json을 먼저 생성해 주세요.")
        time.sleep(1)
        return

    if "filters" not in data or "patterns" not in data:
        print("❌ filters 또는 patterns가 없습니다. data.json을 먼저 생성해 주세요.")
        time.sleep(1)
        return
    
    filters = data["filters"]
    patterns = data["patterns"]

    if not filters or not patterns:
        print("❌ filters 또는 patterns이 비어 있습니다. data.json을 먼저 생성해 주세요.")
        time.sleep(1)
        return

    print(f"✅ size_5 필터 로드 완료 (Cross, X)")
    print(f"✅ size_13 필터 로드 완료 (Cross, X)")
    print(f"✅ size_25 필터 로드 완료 (Cross, X)")

    time.sleep(1)

    print("\n" + "=" * 36) 
    print("[2] 패턴 분석 (라벨 정규화 적용)")
    print("=" * 36)

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

        pattern = pattern_data.get("input")

        expected = normalize_label(pattern_data.get("expected"))

        if expected is None:
            print(f"⚠️ {key}: FAIL - expected 라벨이 올바르지 않음")    # invalid expected; missing expected
            fail_count += 1
            failed_cases.append((key, "expected 라벨이 올바르지 않음"))
            continue

        filter_data = filters.get(f"size_{size}")

        if filter_data is None:
            print(f"⚠️ {key}: FAIL - 필터 {size}x{size}가 존재하지 않음")
            fail_count += 1
            failed_cases.append((key, f"필터 {size}x{size}가 존재하지 않음"))
            continue

        filter_cross = filter_data.get("cross")
        filter_x = filter_data.get("x")

        if filter_cross is None:
            print(f"⚠️ {key}: FAIL - cross 필터가 존재하지 않음")   # missing cross
            fail_count += 1
            failed_cases.append((key, "cross 필터가 존재하지 않음"))
            continue

        if filter_x is None:
            print(f"⚠️ {key}: FAIL - x 필터가 존재하지 않음")   # missing x
            fail_count += 1
            failed_cases.append((key, "x 필터가 존재하지 않음"))
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

    time.sleep(1)

    print("\n" + "=" * 36)
    print("[3] 성능 분석 (평균/10회)")
    print("=" * 36)
    print("크기      평균 시간 (ms)     연산 횟수")
    print("=" * 36)

    run_performance_analysis(filters, size_list=[3, 5, 13, 25])

    time.sleep(1)

    print("\n" + "=" * 36)
    print("[4] 결과 요약")
    print("=" * 36)
    print(f"총 테스트: {total_count}개")
    print(f"통과: {pass_count}개")
    print(f"실패: {fail_count}개")

    if failed_cases:
        print("\n실패 케이스:")
        for key, reason in failed_cases:
            print(f"- {key}: {reason}")
    else:
        print("\n실패 케이스: 없음")

    time.sleep(1)