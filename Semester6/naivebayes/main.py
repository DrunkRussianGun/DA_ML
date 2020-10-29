import math
import os
import random
from typing import List

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


def get_patient_symptoms(count: int) -> List[bool]:
	return [bool(random.getrandbits(1)) for _ in range(count)]


def get_diseases_probabilities(diseases: DataFrame) -> DataFrame:
	total_count = diseases["Количество пациентов"].sum()

	probabilities = diseases.rename(columns = {"Количество пациентов": "Вероятность"})
	probabilities["Вероятность"] = probabilities["Вероятность"].apply(lambda x: x / total_count)
	return probabilities


def sort_diseases_by_probability(
		diseases_probabilities: DataFrame,
		symptoms_probabilities: DataFrame,
		patient_symptoms: DataFrame) -> List[str]:
	patient_diseases = pd.DataFrame([], index = diseases_probabilities.index, columns = ["Ключ сортировки"])
	for disease_name in diseases_probabilities.index:
		disease_value = math.prod(
				probability if presense else 1 - probability
				for probability, presense
				in zip(symptoms_probabilities[disease_name], patient_symptoms["Наличие"]))\
			* diseases_probabilities.at[disease_name, "Вероятность"]
		patient_diseases.at[disease_name, "Ключ сортировки"] = disease_value

	patient_diseases = patient_diseases[patient_diseases["Ключ сортировки"] > 0]
	patient_diseases.sort_values(["Ключ сортировки"], ascending = False, inplace = True)
	return list(patient_diseases.index)


def main():
	diseases = read_data_from_file("diseases.csv")
	symptoms_probabilities = read_data_from_file("symptoms_probabilities.csv")
	check_disease_names(diseases, symptoms_probabilities)

	patient_symptoms = pd.DataFrame(
		get_patient_symptoms(len(symptoms_probabilities.index)),
		index = symptoms_probabilities.index,
		columns = ["Наличие"])

	diseases_probabilities = get_diseases_probabilities(diseases)

	patient_diseases = sort_diseases_by_probability(
		diseases_probabilities,
		symptoms_probabilities,
		patient_symptoms)
	if len(patient_diseases) > 0:
		print("Болезни, отсортированные в порядке убывания вероятности наличия у данного пациента:")
		for patient_disease in patient_diseases:
			print(patient_disease)
		print(os.linesep + "Наиболее вероятная у пациента болезнь: " + patient_diseases[0])
	else:
		print("Не найдено болезней, которые могут присутствовать у пациента")


if __name__ == '__main__':
	main()
