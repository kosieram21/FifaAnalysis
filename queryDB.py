import database_connection


def query_countries_that_played_in_all_world_cups(cursor):
    cursor.execute("""SELECT DISTINCT PI.country FROM
        played_in PI WHERE PI.year = '1991'
        INTERSECT
        SELECT DISTINCT PI.country FROM
        played_in PI WHERE PI.year = '1995'
        INTERSECT
        SELECT DISTINCT PI.country FROM
        played_in PI WHERE PI.year = '1999'
        INTERSECT
        SELECT DISTINCT PI.country FROM
        played_in PI WHERE PI.year = '2003'
        INTERSECT
        SELECT DISTINCT PI.country FROM
        played_in PI WHERE PI.year = '2007'
        INTERSECT
        SELECT DISTINCT PI.country FROM
        played_in PI WHERE PI.year = '2011'
        INTERSECT
        SELECT DISTINCT PI.country FROM
        played_in PI WHERE PI.year = '2015'
        INTERSECT
        SELECT DISTINCT PI.country FROM
        played_in PI WHERE PI.year = '2019'""")

    print("countries that played in every world cup")
    for r in cursor:
        print(r[0])


def query_number_of_times_country_made_it_to_finals(cursor):
    cursor.execute("""SELECT PI.country, COUNT(*) FROM
        played_in PI, games G
        WHERE PI.team1 = G.team1 AND PI.team2 = G.team2 AND PI.year = G.year AND G.round = 'Final'
        GROUP BY PI.country""")

    print("number of times countries made it to the finals stage")
    for r in cursor:
        print(f"{r[0]}: {r[1]}")


def query_number_of_times_country_won_world_cup(cursor):
    cursor.execute("""SELECT PI.country, COUNT(*) FROM
            played_in PI, games G
            WHERE PI.team1 = G.team1 AND PI.team2 = G.team2 AND PI.year = G.year AND G.round = 'Final'
            AND G.winner = PI.country
            GROUP BY PI.country""")

    print("number of times countries won the world cup")
    for r in cursor:
        print(f"{r[0]}: {r[1]}")


def query_player_that_played_in_the_most_world_cups(cursor):
    cursor.execute("""SELECT PW.name, PW.C FROM
        (SELECT P.name, COUNT(*) AS C FROM
        players P
        GROUP BY P.name) AS PW
        ORDER BY PW.C DESC
        LIMIT 1""")

    print("player who played in the most world cups")
    for r in cursor:
        print(f"{r[0]}: {r[1]}")


def query_player_that_played_in_the_most_finals(cursor):
    cursor.execute(""" SELECT PP.name, PP.C FROM
        (SELECT P.name, COUNT(*) AS C FROM
        players P, played_in PI, games G
        WHERE PI.team1 = G.team1 AND PI.team2 = G.team2 AND PI.year = G.year AND G.round = 'Final'
        AND P.country = PI.country AND P.year = PI.year
        GROUP BY P.name) as PP
        WHERE PP.C = 3""")

    print("players who played in the most finals")
    for r in cursor:
        print(f"{r[0]}: {r[1]}")


def execute(db):
    connection = database_connection.create_database_connection(db)
    cursor = connection.cursor()

    query_countries_that_played_in_all_world_cups(cursor)
    print('')
    query_number_of_times_country_made_it_to_finals(cursor)
    print('')
    query_number_of_times_country_won_world_cup(cursor)
    print('')
    query_player_that_played_in_the_most_world_cups(cursor)
    print('')
    query_player_that_played_in_the_most_finals(cursor)

    cursor.close()
    connection.close()
