import sqlite3


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)

    def close(self):
        if self.conn:
            self.conn.close()

    def create_table(self, table_name, columns):
        query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {columns}
            )
        """
        self.conn.execute(query)

    def insert_data(self, table_name, values):
        query = f"""
            INSERT INTO {table_name} VALUES ({','.join('?' for _ in values)})
        """
        self.conn.execute(query, values)

    def select_data(self, table_name, where_clause=None):
        query = f"""
            SELECT * FROM {table_name}
        """
        if where_clause:
            query += f" WHERE {where_clause}"
        return self.conn.execute(query).fetchall()

    def update_data(self, table_name, set_clause, where_clause):
        query = f"""
            UPDATE {table_name} SET {set_clause}
            WHERE {where_clause}
        """
        self.conn.execute(query)

    def delete_data(self, table_name, where_clause):
        query = f"""
            DELETE FROM {table_name}
            WHERE {where_clause}
        """
        self.conn.execute(query)

    def drop_table(self, table_name):
        query = f"""
            DROP TABLE IF EXISTS {table_name}
        """
        self.conn.execute(query)


# Пример использования

db = Database("cars.db")

# Подключение к базе данных
db.connect()

# Создание таблицы
columns = """
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_model TEXT NOT NULL,
    year INTEGER NOT NULL,
    color TEXT NOT NULL,
    body_type TEXT NOT NULL,
    engine_type TEXT NOT NULL,
    engine_power INTEGER NOT NULL,
    mileage INTEGER NOT NULL,
    price REAL NOT NULL,
    transmission_type TEXT NOT NULL,
    additional_features TEXT
"""
db.create_table("cars", columns)

# Добавление записей
cars = [
    ("Toyota Camry", 2018, "Серебристый", "Седан", "Бензиновый", 180, 45000, 15000, "Автоматическая",
     "Кожаный салон, навигационная система"),
    ("BMW X5", 2020, "Черный", "Внедорожник", "Дизельный", 250, 25000, 40000, "Автоматическая",
     "Панорамная крыша, система помощи при парковке"),
    ("Volkswagen Golf", 2016, "Синий", "Хэтчбек", "Бензиновый", 110, 60000, 10000, "Механическая",
     "Климат-контроль, система антиблокировки (ABS)"),
]
for car in cars:
    db.insert_data("cars", car)

# Вывод всех записей
print("Все записи:")
for row in db.select_data("cars"):
    print(row)

# Вывод записи по id
print("Запись с id=2:")
row = db.select_data("cars", "id=2")[0]
print(row)

# Изменение записи
db.update_data("cars", "price=12000", "id=3")

# Удаление записи
db.delete_data("cars", "id=1")

# Отображение таблицы
print("Таблица cars:")
db.select_data("cars", None)

# Отключение от базы данных
db.close()
