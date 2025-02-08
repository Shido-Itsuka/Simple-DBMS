import sqlite3

# Устанавливаем соединение с базой данных
conn = sqlite3.connect('car_rental.db')
cur = conn.cursor()

# Создаем таблицы для базы данных "Прокат автомобилей"

# Таблица "Автомобили"
cur.execute('''CREATE TABLE IF NOT EXISTS Cars (
               Id INTEGER PRIMARY KEY,
               Brand TEXT,
               Model TEXT,
               Year INTEGER,
               LicensePlate TEXT,
               Category TEXT,
               PricePerDay REAL,
               Status TEXT)''')

# Таблица "Клиенты"
cur.execute('''CREATE TABLE IF NOT EXISTS Customers (
               Id INTEGER PRIMARY KEY,
               FirstName TEXT,
               LastName TEXT,
               PhoneNumber TEXT,
               Email TEXT,
               DrivingLicense TEXT)''')

# Таблица "Аренда"
cur.execute('''CREATE TABLE IF NOT EXISTS Rentals (
               Id INTEGER PRIMARY KEY,
               CustomerId INTEGER,
               CarId INTEGER,
               RentalDate TEXT,
               ReturnDate TEXT,
               TotalPrice REAL,
               Status TEXT,
               FOREIGN KEY (CustomerId) REFERENCES Customers(Id),
               FOREIGN KEY (CarId) REFERENCES Cars(Id))''')

# Таблица "Платежи"
cur.execute('''CREATE TABLE IF NOT EXISTS Payments (
               Id INTEGER PRIMARY KEY,
               RentalId INTEGER,
               PaymentDate TEXT,
               Amount REAL,
               PaymentMethod TEXT,
               FOREIGN KEY (RentalId) REFERENCES Rentals(Id))''')

# Заполняем таблицы тестовыми данными

# Данные для таблицы "Автомобили"
cars_data = [
    ("Toyota", "Camry", 2020, "A123BC77", "Седан", 3000, "доступен"),
    ("BMW", "X5", 2019, "B456DE77", "Внедорожник", 5000, "в аренде"),
    ("Mercedes", "E-Class", 2021, "C789FG77", "Седан", 4000, "доступен"),
    ("Honda", "Civic", 2018, "D123HI77", "Седан", 2500, "на техобслуживании"),
    ("Tesla", "Model 3", 2022, "E456JK77", "Электрокар", 4500, "доступен"),
    ("Hyundai", "Sonata", 2017, "F789LM77", "Седан", 2800, "в аренде"),
    ("Nissan", "Qashqai", 2020, "G123NO77", "Внедорожник", 3200, "доступен"),
    ("Volkswagen", "Polo", 2019, "H456PQ77", "Седан", 2300, "доступен"),
    ("Audi", "A6", 2021, "I789RS77", "Седан", 4500, "доступен"),
    ("Chevrolet", "Tahoe", 2018, "J123TU77", "Внедорожник", 5000, "на техобслуживании")
]

cur.executemany('''INSERT INTO Cars (Brand, Model, Year, LicensePlate, Category, PricePerDay, Status)
                   VALUES (?, ?, ?, ?, ?, ?, ?)''', cars_data * 2)  # Удваиваем записи

# Данные для таблицы "Клиенты"
customers_data = [
    ("Иван", "Иванов", "+79161234567", "ivanov@example.com", "77AA123456"),
    ("Мария", "Петрова", "+79169876543", "petrova@example.com", "77BB654321"),
    ("Алексей", "Сидоров", "+79163456789", "sidorov@example.com", "77CC789123"),
    ("Ольга", "Кузнецова", "+79164567890", "kuznetsova@example.com", "77DD456789"),
    ("Дмитрий", "Попов", "+79167890123", "popov@example.com", "77EE987654")
]

cur.executemany('''INSERT INTO Customers (FirstName, LastName, PhoneNumber, Email, DrivingLicense)
                   VALUES (?, ?, ?, ?, ?)''', customers_data * 2)  # Удваиваем записи

# Данные для таблицы "Аренда"
rentals_data = [
    (1, 2, "2025-01-20", "2025-01-25", 15000, "активна"),
    (2, 1, "2025-01-10", "2025-01-15", 12500, "завершена"),
    (3, 3, "2025-01-05", "2025-01-12", 17500, "активна"),
    (4, 4, "2025-01-18", "2025-01-22", 20000, "завершена"),
    (5, 5, "2025-01-12", "2025-01-17", 13500, "активна")
]

cur.executemany('''INSERT INTO Rentals (CustomerId, CarId, RentalDate, ReturnDate, TotalPrice, Status)
                   VALUES (?, ?, ?, ?, ?, ?)''', rentals_data * 2)  # Удваиваем записи

# Данные для таблицы "Платежи"
payments_data = [
    (1, "2025-01-20", 15000, "Карта"),
    (2, "2025-01-10", 12500, "Наличные"),
    (3, "2025-01-05", 17500, "Карта"),
    (4, "2025-01-18", 20000, "Карта"),
    (5, "2025-01-12", 13500, "Наличные")
]

cur.executemany('''INSERT INTO Payments (RentalId, PaymentDate, Amount, PaymentMethod)
                   VALUES (?, ?, ?, ?)''', payments_data * 2)  # Удваиваем записи

# Подтверждаем изменения и закрываем соединение
conn.commit()
conn.close()

print("База данных успешно создана и заполнена удвоенным количеством записей.")
