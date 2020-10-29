import os

import pandas as pd
from pandas import DataFrame


def read_data_from_file(filename: str) -> DataFrame:
	return pd.read_csv(filename, delimiter = ";", index_col = 0)


def check_disease_names(diseases: DataFrame, symptoms_probabilities: DataFrame):
	diseases_names_from_diseases_file = list(diseases.index)
	diseases_names_from_symptoms_file = list(symptoms_probabilities.columns)
	if len(diseases_names_from_diseases_file) != len(diseases_names_from_symptoms_file) \
			or set(diseases_names_from_diseases_file) != set(diseases_names_from_symptoms_file):
		raise ValueError(
			"Названия болезней во входных csv-файлах не совпадают:" + os.linesep +
			"Файл с болезнями: " + str(sorted(diseases_names_from_diseases_file)) + os.linesep +
			"Файл с симптомами: " + str(sorted(diseases_names_from_symptoms_file)))


def main():
	diseases = read_data_from_file("diseases.csv")
	symptoms_probabilities = read_data_from_file("symptoms_probabilities.csv")
	check_disease_names(diseases, symptoms_probabilities)


if __name__ == '__main__':
	main()
