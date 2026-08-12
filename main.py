import time
from pathlib import Path
from .mode import *
from .utility import *
from .pattern_generator import generate_test_data

file_path = "data.json"


def show_main_menu():
    print("\n" + "🔹" * 18)
    print("     Mini NPU Simulator")
    print("🔹" * 18)
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    print("3. 테스트 데이터 생성")
    print("0. 종료")
    print("🔹" * 18)


def run_program():
    while True:
        show_main_menu()
        choice = input("선택: ").strip()
        if choice == "1":
            run_user_mode(3)
        elif choice == "2":
            run_json_mode()
        elif choice == "3":
            if Path(file_path).exists():
                while True:
                    answer = input(
                        f"{file_path}이 이미 존재합니다.\n"
                        "기존 파일을 덮어쓰겠습니까? (y/n): "
                    ).strip().lower()
                    if answer in ["y", "yes"]:
                        generate_test_data(file_path)
                        print("✅ data.json 생성 완료")
                        break
                    elif answer in ["n", "no"]:
                        print("데이터 생성을 취소합니다.")
                        break
                    else:
                        print("y 또는 n 를 입력해주세요.")
            else:
                generate_test_data(file_path)
                print("✅ data.json 생성 완료")
        elif choice == "0":
            print("\n프로그램을 종료합니다...")
            break
        else:
            print("\n 잘못된 입력입니다. 0-3 사이의 숫자를 입력하세요.")
            time.sleep(1)


def main():
    try:
        run_program()
    except (KeyboardInterrupt, EOFError):
        print("\n\n비정상 종료: 프로그램을 종료합니다...")


if __name__ == "__main__":
    main()