import matplotlib.pyplot as plot
import pandas as pd
from pandas import DataFrame


def read_csv_file(csv_file: str) -> DataFrame:
	return pd.read_csv(csv_file, sep = ",", index_col = 0)


def calculate_simple_exponential_smoothing(values: list, alpha: float) -> list:
	predicted_values = list()
	if len(values) == 0:
		return predicted_values

	reversed_alpha = 1 - alpha
	predicted_values.append(values[0])
	for i in range(1, len(values)):
		predicted_value = alpha * values[i] + reversed_alpha * predicted_values[i - 1]
		predicted_values.append(predicted_value)
	return predicted_values


# noinspection PyShadowingNames
def draw(dataset: DataFrame):
	date = list(dataset.Date)
	emission = list(dataset["Monthly Mean Total Sunspot Number"])
	predicted_emission = calculate_simple_exponential_smoothing(emission, 0.5)

	plot.figure(figsize = (30, 10)) # Зададим размер графика вручную
	plot.plot(date, emission) # Соединим точки исходных данных на графике
	plot.plot(date, predicted_emission, color = "r")

	# plot.xlim(0, 100) # Отобразим только первые 100 точек на графике
	plot.show()


dataset = read_csv_file("Sunspots.csv")
draw(dataset)
