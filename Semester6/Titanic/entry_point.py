import math

import matplotlib.pyplot as plot
import pandas as pd
from pandas import DataFrame


def read_csv_file(csv_file: str) -> DataFrame:
	return pd.read_csv(csv_file, sep = ";")


def draw(ages, sexes, counts):
	colors = list("b" if sex == "male" else "r" for sex in sexes)

	figure, axis = plot.subplots()
	axis.bar(ages, counts, color = colors)

	plot.show()


dataset = read_csv_file("dataset.csv")

dataset["age"] = dataset["age"]\
	.apply(lambda age: float(str(age).replace(",", ".")))\
	.apply(lambda age: math.floor(age / 10) * 10 if not math.isnan(age) else math.nan)
group_counts = dataset.groupby(["age", "sex"]).size()

print(group_counts)
draw(
	list(keys[0] for keys in group_counts.keys()),
	list(keys[1] for keys in group_counts.keys()),
	list(group_counts.values))
