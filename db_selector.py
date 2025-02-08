import sys


def main():
    databases = sys.argv[1:]  # Получаем список баз данных из аргументов командной строки

    print("Найдено несколько баз данных:")
    for i, db in enumerate(databases, start=1):
        print(f"{i}. {db}")

    while True:
        try:
            choice = int(input("Введите номер базы данных для работы: "))
            if 1 <= choice <= len(databases):
                # Возвращаем выбранное имя базы данных
                print(databases[choice - 1])
                return
            else:
                print(f"Пожалуйста, введите число от 1 до {len(databases)}.")
        except ValueError:
            print("Некорректный ввод. Введите число.")


if __name__ == "__main__":
    main()
