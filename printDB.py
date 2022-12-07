import database_connection


def execute(db):
    connection = database_connection.create_database_connection(db)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM squads")
    for r in cursor:
        print(r)

    print("-----------------------------")

    cursor.execute("SELECT * FROM players")
    for r in cursor:
        print(r)

    print("-----------------------------")

    cursor.execute("SELECT * FROM games")
    for r in cursor:
        print(r)

    print("-----------------------------")

    cursor.execute("SELECT * FROM member_of")
    for r in cursor:
        print(r)

    print("-----------------------------")

    cursor.execute("SELECT * FROM played_in")
    for r in cursor:
        print(r)

    cursor.close()
    connection.close()
