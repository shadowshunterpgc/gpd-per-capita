import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn.linear_model
import sklearn.neighbors


def load_data():
    # Load the dataset
    oecd_bli = pd.read_csv("dataset/oecd_bli_2015.csv", thousands=',')
    gdp_per_capita = pd.read_csv("dataset/gdp_per_capita.csv", thousands=',', delimiter='\t', encoding='latin1',
                                 na_values='n/a')

    # Prepare the dataset
    country_stats = prepare_country_stats(oecd_bli, gdp_per_capita)
    x = np.c_[country_stats["GDP per capita"]]
    y = np.c_[country_stats["Life satisfaction"]]

    # Visualize the dataset
    country_stats.plot(kind='scatter', x="GDP per capita", y='Life satisfaction')
    plt.show()

    # Select a linear model
    # model = sklearn.linear_model.LinearRegression()
    model = sklearn.neighbors.KNeighborsRegressor(n_neighbors=3)

    # Train model
    model.fit(x, y)

    # Make a prediction for Cyprus
    X_new = [[22587]]  # Cyprus's GPD per capita
    print(model.predict(X_new))


def prepare_country_stats(oecd_bli, gdp_per_capita):
    oecd_bli = oecd_bli[oecd_bli["INEQUALITY"] == "TOT"]
    oecd_bli = oecd_bli.pivot(index="Country", columns="Indicator", values="Value")
    gdp_per_capita.rename(columns={"2015": "GDP per capita"}, inplace=True)
    gdp_per_capita.set_index("Country", inplace=True)
    full_country_stats = pd.merge(left=oecd_bli, right=gdp_per_capita, left_index=True, right_index=True, how="inner", on=None, validate="many_to_many")
    full_country_stats.sort_values(by="GDP per capita", inplace=True)
    remove_indices = [0, 1, 6, 8, 33, 34, 35]
    keep_indices = list(set(range(36)) - set(remove_indices))
    return full_country_stats[["GDP per capita", 'Life satisfaction']].iloc[keep_indices]


if __name__ == '__main__':
    load_data()
