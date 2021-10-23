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


def get_html():
    for i in range(0, 22):
        shutil.rmtree(f'20{str(i).zfill(2)}', ignore_errors=True)
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.0.1488 Yowser/2.5 Safari/537.36'}
    for year in range(22):
        os.mkdir(f'DATA/20{str(year).zfill(2)}')
        for month in range(1, 13):
            data = requests.get(f'https://www.gismeteo.ru/diary/4368/20{str(year).zfill(2)}/{str(month)}/',
                                headers=headers)
            with open(f'DATA/20{str(year).zfill(2)}/20{str(year).zfill(2)}_{str(month)}.html', 'w',
                      encoding='utf8') as f:
                f.write(data.text)


def get_data(inp_year, int_month, inp_day):
    shutil.rmtree('DATA/my_data', ignore_errors=True)
    os.mkdir('DATA/my_data')
    with open('DATA/my_data/C0_data.csv', 'w'):
        pass
    for year in range(22):
        with open(f'DATA/20{str(year).zfill(2)}/20{str(year).zfill(2)}_{str(int_month)}.html', 'r',
                  encoding='utf8') as f:
            soup = bs4.BeautifulSoup(f.read(), 'lxml')
        # mass_of_temp = []
        with open('DATA/my_data/C0_data.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([f'20{str(year).zfill(2)}', f'{str(int_month)}', str(inp_day), str(sum(
                map(lambda x: int(x.text),
                    soup.find_all('tr', align='center')[inp_day - 1].find_all('td', class_='first_in_group'))) / 2)])


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
    get_html()
    get_data()
    choose_model_and_predict()
