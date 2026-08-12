from .utility import *
from .pattern_generator import generate_cross, generate_x


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


def run_json_mode():
    return


def run_performance_analysis():
    return