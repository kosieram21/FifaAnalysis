import database_connection


def execute(db):
    print(f"deleting {db} database...")
    connection = database_connection.create_dbms_connection()

    cursor = connection.cursor()
    cursor.execute(f"DROP DATABASE {db}")

    cursor.close()
    connection.close()
    print("done")
