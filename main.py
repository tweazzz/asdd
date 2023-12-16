import mysql.connector
import sqlite3
from decimal import Decimal

# Подключение к MySQL
mysql_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='888kaz888',
    database='kestesi_db'
)

mysql_cursor = mysql_conn.cursor(dictionary=True)

# Получение списка таблиц в MySQL
mysql_cursor.execute("SHOW TABLES")
tables = [table['Tables_in_kestesi_db'] for table in mysql_cursor.fetchall()]

# Подключение к SQLite
sqlite_conn = sqlite3.connect('sqlite_database.db')
sqlite_cursor = sqlite_conn.cursor()

# Перенос данных из MySQL в SQLite
for table in tables:
    # Получение данных из MySQL
    mysql_cursor.execute(f"SELECT * FROM {table}")
    data = mysql_cursor.fetchall()

    # Получение структуры таблицы
    mysql_cursor.execute(f"DESCRIBE {table}")
    columns = [column['Field'] for column in mysql_cursor.fetchall()]

    # Создание таблицы в SQLite
    sqlite_cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({', '.join([f'{column} TEXT' for column in columns])})")

    # Вставка данных в SQLite
    sqlite_cursor.executemany(
        f"INSERT INTO {table} VALUES ({', '.join(['?' for _ in columns])})",
        [tuple(str(row[column]) if isinstance(row[column], Decimal) else row[column] for column in columns) for row in data]
    )

# Сохранение изменений в SQLite
sqlite_conn.commit()

# Закрытие соединений
mysql_cursor.close()
mysql_conn.close()
sqlite_cursor.close()
sqlite_conn.close()