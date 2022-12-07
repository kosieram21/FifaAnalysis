from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
import matplotlib.pyplot as plt
import pandas as pd
import database_connection


TRAIN_SIZE = 0.80
RANDOM_STATE = 25


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


def model_performance(num_features, x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=TRAIN_SIZE, random_state=RANDOM_STATE)

    model = LinearRegression()
    rfe = RFE(model, n_features_to_select=num_features)
    rfe.fit(x, y)

    reduced_x_train = rfe.transform(x_train)
    reduced_x_test = rfe.transform(x_test)

    model.fit(reduced_x_train, y_train)
    y_prediction = model.predict(reduced_x_test)
    error = round(metrics.mean_absolute_error(y_test, y_prediction), 2)

    return error


def find_optimal_number_of_features(model_performances):
    best = 0
    for i in range(len(model_performances)):
        if model_performances[i] < model_performances[best]:
            best = i
    return best + 1


def optimal_model_results(model_performances, x, y):
    optimal_number_of_features = find_optimal_number_of_features(model_performances)
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=TRAIN_SIZE, random_state=RANDOM_STATE)

    model = LinearRegression()
    rfe = RFE(model, n_features_to_select=optimal_number_of_features)
    rfe.fit(x, y)

    reduced_x_train = rfe.transform(x_train)
    reduced_x_test = rfe.transform(x_test)

    model.fit(reduced_x_train, y_train)
    y_prediction = model.predict(reduced_x_test)

    return y_test, y_prediction


def execute(db):
    connection = database_connection.create_database_connection(db)
    cursor = connection.cursor()

    x, y = get_data_set(cursor)

    num_features = []
    model_performances = []
    for i in range(len(x[0])):
        num_features.append(i + 1)
        model_performances.append(model_performance(num_features[i], x, y))

    df = pd.DataFrame(list(zip(num_features, model_performances)),
                      columns=['number of features', 'mean absolute error'])
    df.plot(kind='scatter', x='number of features', y='mean absolute error',
            title="number of features vs model performance")
    plt.show()

    y_test, y_prediction = optimal_model_results(model_performances, x, y)

    df = pd.DataFrame(list(zip(y_test, y_prediction)),
                      columns=['actual win score', 'predicted win score'])
    df.plot(kind='scatter', x='actual win score', y='predicted win score',
            title="actual win score vs predicted win score")
    plt.plot([0, 13], [0, 13], 'r')
    plt.show()

    cursor.close()
    connection.close()
