import pandas as pd

from pandas import DataFrame


def read_csv_file(csv_file: str) -> DataFrame:
	return pd.read_csv(csv_file, sep = ";")


dataset = read_csv_file("dataset.csv")
for index, row in dataset.iterrows():
	print(f"{index}: {row.values}")
