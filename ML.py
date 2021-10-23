import csv
import os
import shutil
import warnings
import bs4
import numpy as np
import requests
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split


warnings.filterwarnings('ignore')


def choose_model(inp_year, int_month, inp_day):
    with open('DATA/my_data/C0_data.csv', newline='') as File:
        reader = csv.reader(File)
        mass = [*reader]
    X, Y = np.array([list(map(float, i[0:3])) for i in mass]), [float(i[3]) for i in mass]
    X_train, X_test, Y_train, Y_test = train_test_split(X,
                                                        Y,
                                                        test_size=0.2)
    estimators = [GradientBoostingRegressor(), LinearRegression()]
    parametrs_grid_1 = {
        'loss': ['ls', 'lad', 'huber', 'quantile'],
        'alpha': [10, 0.001, 0.01],
        'learning_rate': [0.1, 0.01]
    }
    parametrs_grid_2 = {
        'fit_intercept': [True, False],
        'normalize': [False, True],
        'copy_X': [True, False],
        'positive': [False, True]
    }
    errors = []
    good_pars = []
    for estimator, par in zip(estimators, [parametrs_grid_1, parametrs_grid_2]):
        grid_cv = GridSearchCV(estimator, par, cv=4)
        grid_cv.fit(X_train, Y_train)
        errors.append(mean_squared_error(Y_test, grid_cv.predict(X_test)))
        good_pars.append(grid_cv.best_params_)
    best_param = good_pars[errors.index(min(errors))]
    best_estimator = estimators[errors.index(min(errors))]
    best_param = {i: j for i, j in zip(best_param, map(lambda x: [best_param[x]], best_param))}
    print(best_estimator, best_param)
    return best_estimator, best_param


def predict(inp_year, int_month, inp_day):
    with open('DATA/my_data/C0_data.csv', newline='') as File:
        reader = csv.reader(File)
        mass = [*reader]
    X, Y = np.array([list(map(float, i[0:3])) for i in mass]), [float(i[3]) for i in mass]
    X_train, X_test, Y_train, Y_test = train_test_split(X,
                                                        Y,
                                                        test_size=0.2)
    best_param = {'alpha': [0.001],
                  'learning_rate': [0.01],
                  'loss': ['huber']}
    best_estimator = GradientBoostingRegressor()
    model = GridSearchCV(estimator=best_estimator, param_grid=best_param).fit(X_train, Y_train)
    return model.predict([[inp_year, int_month, inp_day]])


if __name__ == '__main__':
    choose_model_and_predict()
