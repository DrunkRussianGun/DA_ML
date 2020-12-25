from typing import Tuple

import pygame

from configuration import get_configuration
from digit_recognition import load_recognizer, recognize, save_recognizer, train_recognizer
from drag_and_drop_controller import DragAndDropController
from timer import Timer


def main():
	configuration = get_configuration()

	digit_recognizer = None
	file_name_with_recognizer = "trained_recognizer.sav"
	if not configuration.force_train:
		digit_recognizer = load_recognizer(file_name_with_recognizer)
	if digit_recognizer is None:
		digit_recognizer = train_recognizer()
		if configuration.save_to_file:
			save_recognizer(digit_recognizer, file_name_with_recognizer)

	pygame.init()
	screen = pygame.display.set_mode((configuration.window_width, configuration.window_height))
	background_color = pygame.color.THECOLORS["white"]
	screen.fill(background_color)
	set_caption()

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

	screen_capture_interval_in_seconds = 0.5
	screen_capture_timer = Timer(screen_capture_interval_in_seconds, True)
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

		if screen_capture_timer.is_over():
			screenshot = pygame.surfarray.array2d(screen)

			recognized_digit = recognize(digit_recognizer, screenshot)
			set_caption(
				f"recognized as {recognized_digit}"
				if recognized_digit is not None
				else "not recognized")

			screen_capture_timer.start()


def set_caption(caption: str = None):
	new_caption = "Digit recognition"
	if caption is not None and len(caption) > 0:
		new_caption += f" ({caption})"
	pygame.display.set_caption(new_caption)


if __name__ == '__main__':
	main()
