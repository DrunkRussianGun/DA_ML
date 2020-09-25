import math

import matplotlib.pyplot as plot
import pandas as pd

import plotting

dataset = pd.read_csv("dataset.csv", sep = ";")

dataset["age"] = dataset["age"]\
	.apply(lambda age: float(str(age).replace(",", ".")))\
	.apply(lambda age: math.floor(age / 10) * 10 if not math.isnan(age) else math.nan)
group_counts = dataset.groupby(["age", "sex"]).size()
print(group_counts)

ages = group_counts.keys().map(lambda key: key[0]).drop_duplicates()
counts = {
	"male": [group_counts.get((age, "male"), 0) for age in ages],
	"female": [group_counts.get((age, "female"), 0) for age in ages]
}

figure, axis = plot.subplots()
plotting.bar_plot(axis, ages, counts, colors = ["b", "r"])
plot.show()
