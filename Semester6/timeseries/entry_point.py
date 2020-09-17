import matplotlib.pyplot as plot
import pandas as pd
from pandas import DataFrame


def read_csv_file(csv_file: str) -> DataFrame:
	return pd.read_csv(csv_file, sep = ",", index_col = 0)


# noinspection PyShadowingNames
def draw(dataset: DataFrame):
	date = list(dataset.Date)
	emission = list(dataset["Monthly Mean Total Sunspot Number"])

	plot.figure(figsize = (30, 10)) # Зададим размер графика вручную
	plot.plot(date, emission) # Соединим точки на графике

	# plot.xlim(0, 100) # Отобразим только первые 100 точек на графике
	plot.show()


dataset = read_csv_file("Sunspots.csv")
draw(dataset)
