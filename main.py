import time

FILTER_SIZE = 3

def user_input():
    print("\n" + "=" * 18)
    print("     [1] 필터 입력")
    print("=" * 18)
    print("필터 A (3줄 입력, 공백 구분):")

    pattern = [[0 for _ in range(FILTER_SIZE)] for _ in range(FILTER_SIZE)]  # initialize with zeros without numpy
    for i in range(FILTER_SIZE):
        line = input("").strip()
    return

def data_json_analysis():
    return

def show_main_menu():
    print("\n" + "🔹" * 18)
    print("     Mini NPU Simulator")
    print("🔹" * 18)
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    print("0. 종료")
    print("🔹" * 18)


def run_program():
    while True:
        show_main_menu()
        choice = input("선택: ").strip()
        if choice == "1":
            user_input()
        elif choice == "2":
            data_json_analysis()
        elif choice == "0":
            print("\n프로그램을 종료합니다...")
            break
        else:
            print("\n 잘못된 입력입니다. 0-2 사이의 숫자를 입력하세요.")
            time.sleep(1)


def main():
    try:
        run_program()
    except (KeyboardInterrupt, EOFError):
        print("\n\n비정상 종료: 프로그램을 종료합니다...")


if __name__ == "__main__":
    main()