from argparse import ArgumentParser


class Configuration:
	pass


def get_configuration() -> Configuration:
	parser = ArgumentParser()

	args = parser.parse_args()
	return Configuration()
