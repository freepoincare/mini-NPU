import time
from config import DATA_FILE_PATH, EPSILON, REPEAT
from utility import (
    input_matrix, mac, benchmark,
    load_json, analyze_patterns, run_performance_analysis
)


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

    # Performance measurement
    average_a = benchmark(pattern, filter_a)
    average_b = benchmark(pattern, filter_b)
    average = average_a + average_b

    # Result
    if abs(score_a - score_b) < EPSILON:
        print(f"A 점수: {score_a:.16f}")
        print(f"B 점수: {score_b:.16f}")
        print(f"판정: 판정 불가 (|A - B| < {EPSILON})")
    else:
        print(f"A 점수: {score_a}")
        print(f"B 점수: {score_b}")
        print(f"총 연산 시간(평균/{REPEAT}회): {average:.3f} ms")
        print(f"A 평균 시간: {average_a:.3f} ms")
        print(f"B 평균 시간: {average_b:.3f} ms")
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

    # Check for None
    if filters is None or patterns is None:
        print("❌ filters 또는 patterns가 None입니다. data.json을 먼저 생성해 주세요.")
        time.sleep(1)
        return

    # Check for type
    if not isinstance(filters, dict) or not isinstance(patterns, dict):
        print("❌ filters 또는 patterns 데이터 형식이 올바르지 않습니다.")
        time.sleep(1)
        return

    # Check for emptiness
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

    total_count, pass_count, fail_count, failed_cases = analyze_patterns(filters, patterns)

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