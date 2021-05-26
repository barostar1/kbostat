import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
from kbostat.config import homedir

def eramlr(my_pitch):
    path = homedir + '/static/2020KBOPML.csv'

    dataset = pd.read_csv(path, index_col=0)
    #dataset.head()

    dataset = dataset.drop(['Name'], axis=1)

    #print(dataset.isna().sum()) #

    dataset = dataset.dropna()


    #sns.heatmap(dataset.corr(),annot=True)
    #plt.show()


    baseball_playerdata=dataset.drop("ERA",axis=1)
    #print(baseball_playerdata.head())
    baseball_ERA=dataset["ERA"]
    #print(baseball_ERA.head())

    from sklearn.model_selection import train_test_split
    x = baseball_playerdata
    y = baseball_ERA
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, test_size=0.2)


    from sklearn.linear_model import LinearRegression
    mlr = LinearRegression()
    mlr.fit(x_train, y_train)
    my_predict = mlr.predict(my_pitch)

    print(my_predict)
    return(my_predict)