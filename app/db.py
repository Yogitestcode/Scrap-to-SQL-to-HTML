
from mysql.connector import pooling

def get_connection_pool():
    pool = pooling.MySQLConnectionPool(
        pool_name="my_pool",
        pool_size=5,
        host="localhost",
        database='books_db',
        user='root',
        password='',
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )

    return pool

pool = get_connection_pool()