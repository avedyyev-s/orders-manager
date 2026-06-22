import psycopg2

try:
    # Пытаемся подключиться к нашей базе в Docker
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="mysecretpassword",
        database="taxi_db"
    )
    print("Ура! Связь с PostgreSQL успешно установлена!")
    connection.close()
except Exception as e:
    print(f"Ошибка подключения: {e}")
