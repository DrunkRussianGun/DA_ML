from typing import Tuple

import pygame

import digit_recognition
from configuration import get_configuration
from drag_and_drop_controller import DragAndDropController


def main():
	configuration = get_configuration()

	pygame.init()
	pygame.display.set_caption("Digit recognition")
	screen = pygame.display.set_mode((configuration.window_width, configuration.window_height))
	background_color = pygame.color.THECOLORS["white"]
	screen.fill(background_color)

	line_width = 10
	eraser_width = 30
	black_color = pygame.color.THECOLORS["black"]

	def get_mouse_position() -> Tuple[float, float]:
		return pygame.mouse.get_pos()

	def draw_line(old_mouse_position: Tuple[float, float], new_mouse_position: Tuple[float, float]):
		pygame.draw.line(screen, black_color, old_mouse_position, new_mouse_position, line_width)

	def erase_line(old_mouse_position: Tuple[float, float], new_mouse_position: Tuple[float, float]):
		pygame.draw.line(screen, background_color, old_mouse_position, new_mouse_position, eraser_width)

	left_click_controller = DragAndDropController(get_mouse_position, draw_line)
	right_click_controller = DragAndDropController(get_mouse_position, erase_line)

	game_running = True
	while game_running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_running = False
			elif event.type == pygame.MOUSEMOTION:
				# Важно, чтобы сначала вызывался метод move, и только после него — start_dragging,
				# иначе текущая позиция мыши в контроллерах постоянно будет перезатираться,
				# из-за чего рисование работать не будет
				left_click_controller.move()
				right_click_controller.move()

				left_button_pressed, middle_button_pressed, right_button_pressed = event.buttons
				if left_button_pressed:
					left_click_controller.start_dragging()
				else:
					left_click_controller.stop_dragging()

				if right_button_pressed:
					right_click_controller.start_dragging()
				else:
					right_click_controller.stop_dragging()

		pygame.display.update()

		# digit_recognition.recognize()


if __name__ == '__main__':
	main()
