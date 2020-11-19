from argparse import ArgumentParser


class Configuration:
	def __init__(self, window_width: int, window_height: int):
		self.window_width = window_width
		self.window_height = window_height


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

	args = parser.parse_args()
	return Configuration(args.window_width, args.window_height)
