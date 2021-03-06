import os

import joblib
import numpy
from PIL import Image
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

from configuration import Configuration


def train_recognizer() -> MLPClassifier:
	digits = datasets.load_digits()
	images = digits.images.reshape((len(digits.images), -1))
	train_images, test_images, train_targets, test_targets = train_test_split(
		images,
		digits.target,
		test_size = 0.3)

	recognizer = MLPClassifier(
		hidden_layer_sizes = 16,
		activation = "logistic",
		alpha = 1e-4,
		solver = "sgd",
		tol = 1e-4,
		learning_rate_init = .1)
	recognizer.fit(train_images, train_targets)
	accuracy = recognizer.score(test_images, test_targets)

	print(f"Recognizer accuracy: {accuracy * 100:.2f}%")
	return recognizer


def recognize(recognizer: MLPClassifier, screenshot: Image, debug: bool) -> int:
	screenshot = screenshot.resize((8, 8), Image.LANCZOS)
	if debug:
		screenshot.save(Configuration.get_debug_file_path("4.resized.png"))

	recognizer_input = numpy\
		.array([x / 255 * 16 for x in screenshot.tobytes()])\
		.reshape(1, -1)
	return recognizer.predict(recognizer_input)[0]


def load_recognizer(file_name: str) -> MLPClassifier:
	if not os.path.isfile(file_name):
		return None
	return joblib.load(file_name)


def save_recognizer(recognizer: MLPClassifier, file_name: str):
	joblib.dump(recognizer, file_name, compress = ("lzma", 9))
