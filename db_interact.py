import sqlite3
from typing import List, Dict, Tuple


class DatabaseManager:
    def __init__(self, db_path: str):
        """
        Инициализирует менеджер базы данных.
        :param db_path: Путь к файлу базы данных
        """
        self.db_path = db_path

    def execute_query(self, query: str) -> List[Tuple]:
        """
        Выполняет запрос к базе данных SQLite.
        :param query: Строка запроса
        :return: Список кортежей с результатами запроса
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(query)
            results = cur.fetchall()
        return results

    def get_table_names(self):
        """
        Возвращает список таблиц в SQLite базе данных.
        :return: Список названий таблиц
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cur.fetchall()]  # Извлекаем названия таблиц
            return tables

    def delete_record_by_id(self, table_name: str, record_id: int) -> None:
        """
        Удаляет строку из таблицы базы данных SQLite по ID.
        :param table_name: Название таблицы
        :param record_id: Номер строки
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(f"DELETE FROM {table_name} WHERE ID = ?", (record_id,))
            conn.commit()

    def get_all_ids(self, table_name: str) -> List[Tuple[int]]:
        """
        Возвращает список ID всех строк в таблице.
        :param table_name: Название таблицы
        :return: Список кортежей с ID
        """
        query = f"SELECT ID FROM {table_name}"
        return self.execute_query(query)

    def add_record(self, table_name: str, data: Tuple) -> None:
        """
        Добавляет строку в таблицу базы данных.
        :param table_name: Название таблицы
        :param data: Данные для добавления
        """
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()

    def update_record(self, table_name: str, row_id: int, updated_data: Dict[str, any]) -> None:
        """
        Обновляет строку в таблице базы данных SQLite.
        :param table_name: Название таблицы
        :param row_id: ID строки, которую необходимо обновить
        :param updated_data: Словарь с обновленными данными
        """
        set_clause = ", ".join([f"{col} = ?" for col in updated_data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE ID = ?"
        params = list(updated_data.values()) + [row_id]
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            conn.commit()

    def get_column_count(self, table_name: str) -> int:
        """
        Возвращает количество столбцов в таблице.
        :param table_name: Название таблицы
        :return: Количество столбцов
        """
        query = f"PRAGMA table_info({table_name})"
        columns = self.execute_query(query)
        return len(columns)

    def get_column_names(self, table_name: str) -> List[str]:
        """
        Возвращает названия всех столбцов в таблице.
        :param table_name: Название таблицы
        :return: Список названий столбцов
        """
        query = f"PRAGMA table_info({table_name})"
        columns = self.execute_query(query)
        return [col[1] for col in columns]

    def get_table_rows(self, table_name: str) -> List[Tuple]:
        """
        Возвращает все строки таблицы.
        :param table_name: Название таблицы
        :return: Список всех строк таблицы
        """
        query = f"SELECT * FROM {table_name}"
        return self.execute_query(query)
