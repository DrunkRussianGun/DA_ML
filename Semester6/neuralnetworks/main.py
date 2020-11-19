import pygame

import digit_recognition
from configuration import get_configuration


def main():
	configuration = get_configuration()

	pygame.init()
	pygame.display.set_caption("Digit recognition")
	screen = pygame.display.set_mode((configuration.window_width, configuration.window_height))
	screen.fill(pygame.color.THECOLORS["white"])

	game_running = True
	while game_running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_running = False

		pygame.display.update()

		# digit_recognition.recognize()


if __name__ == '__main__':
	main()
