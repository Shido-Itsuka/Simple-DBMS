import sqlite3

db_name = 'car_catalog.db'


def execute_query(query: str):
    """
    Выполняет запрос к базе данных SQLite.

    :param query: Строка запроса
    :return: Список кортежей с результатами запроса
    """
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    conn.close()
    return results


def delete_record_by_id(table_name: str, record_id: str):
    """
    Удаляет строку из таблицы базы данных SQLite по ID.

    :param table_name: Название таблицы
    :param record_id: Номер строки
    :return:
    """
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    # Выполнение запроса на удаление записи
    cur.execute("DELETE FROM {} WHERE ID = ?".format(table_name), (record_id,))
    # Подтверждение изменений в базе данных
    conn.commit()
    # Закрытие соединения с базой данных
    conn.close()


def get_all_ids(table_name):
    """
    Возвращает список ID всех строк в таблице.

    :param table_name: Название таблицы
    :return: Список кортежей с ID: [('ID'), ('ID'), ('ID'), ...]
    """
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    # Выполнение запроса для выбора всех ID из таблицы
    cur.execute("SELECT ID FROM {}".format(table_name))
    # Получение результатов запроса
    ids = cur.fetchall()
    # Закрытие соединения с базой данных
    conn.close()
    # Возвращение списка ID
    return ids


def add_record(table_name, data):
    """
    Добавляет строку в таблицу базы данных.

    :param table_name: Название таблицы
    :param data: Данные для добавления
    """
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    # Выполнение запроса на добавление записи
    questions = ', '.join(['?'] * len(data))
    print(questions)
    cur.execute(f"INSERT INTO {table_name} VALUES ({questions})", data)
    # Подтверждение изменений в базе данных
    conn.commit()
    # Закрытие соединения с базой данных
    conn.close()


def update_record(table_name: str, row_id: int, updated_data: dict):
    """
    Обновляет строку в таблице базы данных SQLite.

    :param table_name: Название таблицы обновляемой строки
    :param row_id: ID строки, которую необходимо обновить
    :param updated_data: Словарь с обновленными данными (название столбца: новое значение)
    """
    # Подключаемся к базе данных
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Формируем строку запроса для обновления
    set_clause = ", ".join([f"{col} = ?" for col in updated_data.keys()])
    query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"

    # Подготавливаем параметры для запроса
    params = list(updated_data.values())
    params.append(row_id)

    try:
        # Выполняем запрос
        cursor.execute(query, params)

        # Сохраняем изменения
        conn.commit()

        print(f"Row with ID {row_id} in table '{table_name}' successfully updated.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Закрываем соединение с базой данных
        conn.close()


def get_column_count(table_name):
    """
    Возвращает количество столбцов в таблице.
    :param table_name: Название таблицы
    :return: Количество столбцов: int
    """
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    # Выполнение запроса на получение информации о столбцах таблицы
    cur.execute("PRAGMA table_info({})".format(table_name))
    # Получение результатов запроса и подсчет количества строк
    column_count = len(cur.fetchall())
    # Закрытие соединения с базой данных
    conn.close()
    # Возвращение количества столбцов
    return column_count


# Функция для получения названий столбцов
def get_column_names(table_name):
    """
    Возвращает названия всех столбцов в таблице
    :param table_name: Название таблицы
    :return: Список названий столбцов
    """
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info({})".format(table_name))
    columns = [row[1] for row in cur.fetchall()]
    conn.close()
    return columns


# Функция для получения всех строк таблицы
def get_table_rows(table_name):
    """
    Возвращает все строки таблицы

    :param table_name: Название таблицы
    :return: Список всех строк таблицы
    """
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("SELECT * FROM {}".format(table_name))
    rows = cur.fetchall()
    conn.close()
    return rows
