from argparse import ArgumentParser


class Configuration:
	def __init__(self, window_width: int, window_height: int, force_train: bool, save_to_file: bool):
		self.window_width = window_width
		self.window_height = window_height
		self.force_train = force_train
		self.save_to_file = save_to_file


def get_configuration() -> Configuration:
	parser = ArgumentParser()
	parser.add_argument(
		"-ww",
		"--window_width",
		type = int,
		help = "Width of the game window (default 640)",
		default = 640)
	parser.add_argument(
		"-wh",
		"--window_height",
		type = int,
		help = "Height of the game window (default 480)",
		default = 480)
	parser.add_argument(
		"-t",
		"--force-train",
		help = "Always train recognizer instead of loading from file",
		action = "store_true")
	parser.add_argument(
		"--no-save",
		help = "Don't save trained recognizer to file",
		action = "store_true")

	args = parser.parse_args()
	return Configuration(args.window_width, args.window_height, args.force_train, not args.no_save)
