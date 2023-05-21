import psycopg2

try:
    conn = psycopg2.connect(
        host="db",
        database="carprices",
        user="postgres",
        password="admin")
except Exception as e:
    print(e)
    print('Connection denied')
    exit(0)

if conn is not None:
    print('Connection established to a DB')
else:
    print('Connection not established')

    cur = conn.cursor()
    conn.commit()

