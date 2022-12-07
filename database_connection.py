import mysql.connector


HOST = "localhost"
USER = "root"
PASSWORD = "admin"


def create_database_connection(db):
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=db
    )


def create_dbms_connection():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD
    )
