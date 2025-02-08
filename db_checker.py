import os


def find_databases_folder():
    """
    Проверяет, существует ли папка databases, и возвращает путь к ней.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_folder = os.path.join(base_path, 'databases')
    if not os.path.exists(db_folder):
        raise FileNotFoundError("Папка 'databases' не найдена. Создайте её в корневом каталоге проекта.")
    return db_folder


def list_databases(db_folder):
    """
    Находит все папки в папке databases и проверяет наличие файла .db в каждой.
    Возвращает словарь вида {имя базы данных: путь к файлу}.
    """
    databases = {}
    for folder in os.listdir(db_folder):
        folder_path = os.path.join(db_folder, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith('.db'):
                    databases[folder] = os.path.join(folder_path, file)
                    break  # Предполагается, что в каждой папке только один .db файл
    if not databases:
        raise FileNotFoundError("Базы данных не найдены. Убедитесь, что в папках содержатся файлы с расширением .db.")
    return databases


def get_databases():
    """
    Основная функция для получения всех баз данных.
    Возвращает словарь вида {имя базы данных: путь к файлу}.
    """
    db_folder = find_databases_folder()
    return list_databases(db_folder)


if __name__ == "__main__":
    try:
        databases = get_databases()
        print("Найдены базы данных:")
        for name, path in databases.items():
            print(f"{name}: {path}")
    except Exception as e:
        print(f"Ошибка: {e}")
