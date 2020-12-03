from time import time


class Timer:
	def __init__(self, delay_in_seconds: float = 0.0, run: bool = False):
		self.__is_running = run
		self.__delay_in_seconds = delay_in_seconds
		self.__current_time = 0.0

	def start(self, delay_in_seconds: float = None):
		self.__is_running = True
		self.__current_time = time()
		if delay_in_seconds is not None:
			self.__delay_in_seconds = delay_in_seconds

	def is_over(self) -> bool:
		if not self.__is_running:
			return True

		elapsed_time = time() - self.__current_time
		if elapsed_time < 0:
			self.start()
			return False

		if elapsed_time > self.__delay_in_seconds:
			self.__is_running = False
			return True

		return False
