from __future__ import annotations

import random
from typing import List

import numpy


class DiophantineEquation:
	def __init__(self, coefficients: List[int], constant_term: int):
		self.coefficients = coefficients
		self.constant_term = constant_term

	def __str__(self):
		def with_sign(coefficient: int) -> str:
			sign = "-" if coefficient < 0 else "+"
			return f" {sign} {abs(coefficient)}"

		return str(self.coefficients[0]) + " x1" +\
			"".join(
				f"{with_sign(coefficient)} x{index}"
				for index, coefficient in enumerate(self.coefficients[1:], start = 2)) +\
			(with_sign(self.constant_term) if self.constant_term != 0 else "") +\
			" = 0"


class Solution:
	def __init__(self, equation: DiophantineEquation, variable_values: List[int]):
		if len(variable_values) != len(equation.coefficients):
			raise ValueError(
				f"Количество значений переменных {variable_values} должно совпадать " +
				f"с количеством переменных в уравнении {equation}")
		self.variable_values = variable_values
		self._equation = equation
		self._score = Solution._score(equation, variable_values)

	@property
	def score(self) -> float:
		return self._score

	def mutate(self, mutant_solution: Solution):
		value_mutation_probability = 1 / len(self.variable_values)
		self.variable_values = [numpy.random.choice(
				[old_value, new_value],
				p = [value_mutation_probability, 1 - value_mutation_probability])
			for old_value, new_value in zip(self.variable_values, mutant_solution.variable_values)]
		self._score = Solution._score(self._equation, self.variable_values)

	@staticmethod
	def breed(first: Solution, second: Solution) -> Solution:
		return Solution(
			first._equation,
			[numpy.random.choice([first_value, second_value])
				for first_value, second_value in zip(first.variable_values, second.variable_values)])

	def __str__(self):
		return ", ".join(
			f"x{index} = {value}"
			for index, value in enumerate(self.variable_values, start = 1))

	@staticmethod
	def _score(equation: DiophantineEquation, variable_values: List[int]) -> float:
		return 1 / abs(
			sum(numpy.multiply(equation.coefficients, variable_values)) +
			equation.constant_term)


def main():
	equation = generate_random_diophantine_equation(4)
	print("Equation: " + str(equation))

	solution = get_solution(equation)
	print("Solution: " + str(solution))


def generate_random_diophantine_equation(variables_count: int) -> DiophantineEquation:
	return DiophantineEquation(
		# При генерации коэффициентов переменных исключаем 0
		[numpy.random.choice(
				range(-30, 30 + 1),
				p = [1 / (30 * 2)] * 30 + [0] + [1 / (30 * 2)] * 30)
			for _ in range(variables_count)],
		random.randint(-100, 100))


def get_solution(equation: DiophantineEquation) -> Solution:
	initial_population_size = 50
	new_population_size = 50
	mutation_probability = 0.05
	population = generate_population(equation, initial_population_size)

	solution_found = False
	while not solution_found:
		population_score_sum = sum(solution.score for solution in population)
		solutions_probabilities = [solution.score / population_score_sum for solution in population]
		new_population = []
		for _ in range(new_population_size):
			first_parent, second_parent = numpy.random.choice(
				population,
				size = 2,
				replace = False,
				p = solutions_probabilities)
			child = Solution.breed(first_parent, second_parent)
			new_population.append(child)

			if child.score == 0:
				return child

		mutant_population = generate_population(equation, new_population_size)
		for index, solution in enumerate(new_population):
			need_mutation = numpy.random.choice([True, False], p = [mutation_probability, 1 - mutation_probability])
			if need_mutation:
				solution.mutate(mutant_population[index])
				if solution.score == 0:
					return solution

		population += new_population


def generate_population(equation: DiophantineEquation, size: int) -> List[Solution]:
	max_coefficient_modulus = max(abs(coefficient) for coefficient in equation.coefficients)
	max_solution_value_modulus = abs(
		max_coefficient_modulus *
		equation.constant_term if equation.constant_term != 0 else 1)
	return [
		Solution(
			equation,
			[random.randint(-max_solution_value_modulus, max_solution_value_modulus)
				for _ in range(len(equation.coefficients))])
		for _ in range(size)]


if __name__ == '__main__':
	main()
