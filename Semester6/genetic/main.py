from __future__ import annotations

from typing import List


class DiophantineEquation:
	def __init__(self, coefficients: List[int], constant_term: int):
		self.coefficients = coefficients
		self.constant_term = constant_term

	def __str__(self):
		raise NotImplementedError()


class Solution:
	def __init__(self, equation: DiophantineEquation, variable_values: List[int]):
		if len(variable_values) != len(equation.coefficients):
			raise ValueError(
				f"Количество значений переменных {variable_values} должно совпадать " +
				f"с количеством переменных в уравнении {equation}")
		self.variable_values = variable_values
		self._score = Solution._score(equation, variable_values)

	@property
	def score(self) -> float:
		return self._score

	def mutate(self):
		raise NotImplementedError()

	@staticmethod
	def breed(first: Solution, second: Solution) -> Solution:
		raise NotImplementedError()

	def __str__(self):
		raise NotImplementedError()

	@staticmethod
	def _score(equation: DiophantineEquation, variable_values: List[int]) -> float:
		raise NotImplementedError()


def main():
	equation = generate_random_diophantine_equation(4)
	print("Equation: " + str(equation))

	solution = get_solution(equation)
	print("Solution: " + str(solution))


def generate_random_diophantine_equation(variables_count: int) -> DiophantineEquation:
	raise NotImplementedError()


def get_solution(equation: DiophantineEquation) -> Solution:
	raise NotImplementedError()


def generate_solution(equation: DiophantineEquation) -> Solution:
	raise NotImplementedError()


if __name__ == '__main__':
	main()
