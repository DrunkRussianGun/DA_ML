from argparse import ArgumentParser


class Configuration:
	def __init__(
			self,
			debug: bool,
			window_width: int,
			window_height: int,
			force_train: bool,
			save_to_file: bool):
		self.debug = debug
		self.window_width = window_width
		self.window_height = window_height
		self.force_train = force_train
		self.save_to_file = save_to_file

	@staticmethod
	def get_debug_file_path(file_name: str):
		import os
		return os.path.join("debug", file_name)


def get_configuration() -> Configuration:
	parser = ArgumentParser()
	parser.add_argument(
		"--debug",
		help = "Save intermediate images during converting screen image to recognizer input",
		action = "store_true")
	parser.add_argument(
		"-ww",
		"--window-width",
		metavar = "<width>",
		type = int,
		help = "Width of the game window (default 640)",
		default = 640)
	parser.add_argument(
		"-wh",
		"--window-height",
		metavar = "<height>",
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
	return Configuration(
		args.debug,
		args.window_width,
		args.window_height,
		args.force_train,
		not args.no_save)
