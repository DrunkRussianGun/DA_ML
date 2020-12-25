from numpy import ndarray
from sklearn.neural_network import MLPClassifier


def train_recognizer() -> MLPClassifier:
	return None


def recognize(recognizer: MLPClassifier, screenshot: ndarray) -> int:
	return None


def load_recognizer(file_name: str) -> MLPClassifier:
	raise NotImplementedError()


def save_recognizer(recognizer: MLPClassifier, file_name: str):
	raise NotImplementedError()
