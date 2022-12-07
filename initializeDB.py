import database_connection


def create_database(db):
    print(f"creating {db} database...")
    connection = database_connection.create_dbms_connection()

    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE {db}")

    cursor.close()
    connection.close()
    print("done")


def create_database_tables(cursor):
    print("creating squads table...")
    cursor.execute("""CREATE TABLE squads(
        country VARCHAR(50) NOT NULL,
        year VARCHAR(8) NOT NULL,
        players INT,
        age FLOAT,
        possession FLOAT,
        matches_played INT,
        starts INT,
        min_playing_time INT,
        minutes_played_90s FLOAT,
        goals INT,
        assists INT,
        non_penalty_goals INT,
        penalty_kicks_made INT,
        penalty_kicks_attempted INT,
        yellow_cards INT,
        red_cards INT,
        goals_per_90 FLOAT,
        assists_per_90 FLOAT,
        PRIMARY KEY (country, year))""")
    print("done")

    print("creating players table...")
    cursor.execute("""CREATE TABLE players(
        name VARCHAR(50) NOT NULL,
        year VARCHAR(8) NOT NULL,
        country VARCHAR(50),
        position VARCHAR(2),
        age INT,
        cap INT,
        goals INT,
        club VARCHAR(255),
        PRIMARY KEY (name, year))""")
    print("done")

    print("creating games table...")
    cursor.execute("""CREATE TABLE games(
        team1 VARCHAR(50) NOT NULL,
        team2 VARCHAR(50) NOT NULL,
        year VARCHAR(8) NOT NULL,
        score1 INT,
        score2 INT,
        round VARCHAR(255),
        winner VARCHAR(255),
        PRIMARY KEY (team1, team2, year))""")
    print("done")

    print("creating member_of table...")
    cursor.execute("""CREATE TABLE member_of(
        name VARCHAR(50) NOT NULL REFERENCES players(name),
        country VARCHAR(50) NOT NULL REFERENCES squads(country),
        year VARCHAR(8) NOT NULL REFERENCES squads(year),
        PRIMARY KEY (name, country, year))""")
    print("done")

    print("creating played_in table...")
    cursor.execute("""CREATE TABLE played_in(
        country VARCHAR(50) NOT NULL REFERENCES squads(country),
        year VARCHAR(8) NOT NULL REFERENCES squads(country),
        team1 VARCHAR(50) NOT NULL REFERENCES games(team1),
        team2 VARCHAR(50) NOT NULL REFERENCES games(team2),
        PRIMARY KEY (country, year, team1, team2))""")
    print("done")


def initialize_squads_table(cursor):
    print("loading data into squads table...")
    squads_file = open("womens-world-cup.csv", encoding="utf-8")
    lines = squads_file.readlines()

    vals = []
    for line in lines:
        entries = line.strip('\n').split(',')
        vals.append((entries[1], coerce_value(entries[2]), coerce_value(entries[3]), coerce_value(entries[4]),
                     coerce_value(entries[5]), coerce_value(entries[6]), coerce_value(entries[7]),
                     coerce_value(entries[8]), coerce_value(entries[9]), coerce_value(entries[10]),
                     coerce_value(entries[11]), coerce_value(entries[12]), coerce_value(entries[13]),
                     coerce_value(entries[14]), coerce_value(entries[15]), coerce_value(entries[16]),
                     coerce_value(entries[17]), coerce_value(entries[18])))

    sql = """INSERT INTO squads 
        (country, year, players, age, possession, matches_played, starts,
        min_playing_time, minutes_played_90s, goals, assists,
        non_penalty_goals, penalty_kicks_made, penalty_kicks_attempted,
        yellow_cards, red_cards, goals_per_90, assists_per_90) VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    cursor.executemany(sql, vals)
    squads_file.close()
    print("done")


def initialize_players_table(cursor):
    print("loading data into players table...")
    players_file = open("players.csv", encoding="utf-8")
    lines = players_file.readlines()

    vals = []
    for line in lines:
        entries = line.strip('\n').split(',')
        vals.append((entries[3], coerce_value(entries[9]), entries[1], entries[2],
                     coerce_value(entries[5]), coerce_value(entries[6]),
                     coerce_value(entries[7]), entries[8]))

    sql = """INSERT INTO players 
            (name, year, country, position, age, cap, goals, club) VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s)"""

    cursor.executemany(sql, vals)
    players_file.close()
    print("done")


def initialize_games_table(cursor):
    print("loading data into games table...")
    results2_file = open("results_2.csv", encoding="utf-8")
    lines = results2_file.readlines()

    vals = []
    for line in lines:
        entries = line.strip('\n').split(',')
        vals.append((entries[1], entries[3], coerce_value(entries[0]),
                     coerce_value(entries[2]), coerce_value(entries[4]),
                     entries[5], entries[6]))

    sql = """INSERT INTO games 
            (team1, team2, year, score1, score2, round, winner) VALUES 
            (%s, %s, %s, %s, %s, %s, %s)"""

    cursor.executemany(sql, vals)
    results2_file.close()
    print("done")


def initialize_member_of_table(cursor):
    print("loading data into members_of table...")
    cursor.execute("""SELECT P.name,S.country,S.year FROM
        players P, squads S
        WHERE S.year = P.year AND P.country = S.country""")

    vals = []
    for r in cursor:
        vals.append(r)

    sql = """INSERT INTO member_of
        (name, country, year) VALUES
        (%s, %s, %s)"""

    cursor.executemany(sql, vals)
    print("done")


def initialize_played_in_table(cursor):
    print("loading data into played_in table...")
    cursor.execute("""SELECT S.country,S.year,G.team1,G.team2 FROM
        squads S, games G
        WHERE S.year = G.year AND (S.country = G.team1 OR S.country = G.team2)""")

    vals = []
    for r in cursor:
        vals.append(r)

    sql = """INSERT INTO played_in
        (country, year, team1, team2) VALUES
        (%s, %s, %s, %s)"""

    cursor.executemany(sql, vals)
    print("done")


def coerce_value(val):
    return val if val != '' else "-1"


def execute(db):
    create_database(db)
    connection = database_connection.create_database_connection(db)
    cursor = connection.cursor()
    create_database_tables(cursor)
    initialize_squads_table(cursor)
    initialize_players_table(cursor)
    initialize_games_table(cursor)
    initialize_member_of_table(cursor)
    initialize_played_in_table(cursor)
    connection.commit()
    cursor.close()
    connection.close()
