from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE
import database_connection


def get_x_dictionary(cursor):
    cursor.execute("""SELECT * FROM squads""")

    x = {}
    for r in cursor:
        key = F"{r[0]}-{r[1]}"
        x[key] = [r[2 + i] for i in range(16)]

    return x


def get_y_dictionary(cursor):
    cursor.execute("""SELECT S.country, PI.year, G.winner FROM
            squads S, played_in PI, games G
            WHERE S.country = PI.country 
            AND S.year = PI.year 
            AND PI.team1 = G.team1 
            AND PI.team2 = G.team2
            AND PI.year = G.year
            ORDER BY S.country, PI.year""")

    y = {}
    for r in cursor:
        key = f"{r[0]}-{r[1]}"
        if key not in y:
            y[key] = 0
        if r[2] == 'Draw' or r[2] == r[0]:
            y[key] = y[key] + (1 if r[2] == 'Draw' else 2)

    return y


def get_data_set(cursor):
    x_dictionary = get_x_dictionary(cursor)
    y_dictionary = get_y_dictionary(cursor)

    x = []
    y = []
    for key in x_dictionary:
        x.append(x_dictionary[key])
        y.append(y_dictionary[key])

    return x, y


def execute(db):
    connection = database_connection.create_database_connection(db)
    cursor = connection.cursor()

    x, y = get_data_set(cursor)
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.80)

    #model = DecisionTreeRegressor()
    model = LogisticRegression()
    rfe = RFE(model, n_features_to_select=4)
    rfe.fit(x, y)
    print(rfe.ranking_)

    model.fit(x_train, y_train)
    y_prediction = model.predict(x_test)
    print(metrics.mean_absolute_error(y_test, y_prediction))
    for i in range(len(y_test)):
        print(f"{i}: {y_test[i]} {y_prediction[i]}")

    cursor.close()
    connection.close()
