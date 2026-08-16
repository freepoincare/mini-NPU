import time
from pathlib import Path
from config import DATA_FILE_PATH
from mode import run_user_mode, run_json_mode
from utility import clear_data
from pattern_generator import generate_test_data


def show_main_menu():
    print("\n" + "🔹" * 18)
    print("         Mini NPU Simulator")
    print("🔹" * 18)
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    print("3. data.json 생성")
    print("4. data.json 초기화")
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
            if Path(DATA_FILE_PATH).exists():
                while True:
                    answer = input(
                        f"{DATA_FILE_PATH}이 이미 존재합니다.\n"
                        "기존 파일을 덮어쓰겠습니까? (y/n): "
                    ).strip().lower()
                    if answer in ["y", "yes"]:
                        generate_test_data(DATA_FILE_PATH)
                        print("✅ data.json 생성 완료")
                        time.sleep(1)
                        break
                    elif answer in ["n", "no"]:
                        print("데이터 생성을 취소합니다.")
                        break
                    else:
                        print("y 또는 n 를 입력해주세요.\n")
            else:
                generate_test_data(DATA_FILE_PATH)
                print("✅ data.json 생성 완료")
                time.sleep(1)
        elif choice == "4":
            clear_data(DATA_FILE_PATH)
            print("✅ data.json이 초기화 되었습니다.")
            time.sleep(1)
        elif choice == "0":
            print("\n프로그램을 종료합니다...")
            time.sleep(1)
            break
        else:
            print("\n잘못된 입력입니다. 0-4 사이의 숫자를 입력하세요.")
            time.sleep(1)


def main():
    try:
        run_program()
    except (KeyboardInterrupt, EOFError):
        print("\n\n비정상 종료: 프로그램을 종료합니다...")


if __name__ == "__main__":
    main()