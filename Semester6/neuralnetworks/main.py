import os
from typing import Tuple

import numpy
import pygame
from PIL import Image, ImageOps

from configuration import Configuration, get_configuration
from digit_recognition import load_recognizer, recognize, save_recognizer, train_recognizer
from drag_and_drop_controller import DragAndDropController
from timer import Timer


def main():
	configuration = get_configuration()
	if configuration.debug:
		os.makedirs(Configuration.get_debug_file_path(""), exist_ok = True)

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
			screenshot_bytes = pygame.surfarray.array2d(screen).transpose()
			screenshot = Image\
				.fromarray(screenshot_bytes, "I")\
				.convert("L")
			prepared_screenshot = prepare_screenshot(screenshot, configuration.debug)

			recognized_digit = None
			if prepared_screenshot is not None:
				recognized_digit = recognize(digit_recognizer, prepared_screenshot, configuration.debug)
			recognition_result_message = f"Recognized as {recognized_digit}"\
				if recognized_digit is not None\
				else "Not recognized"
			print(recognition_result_message)
			set_caption(recognition_result_message)

			screen_capture_timer.start()


def set_caption(caption: str = None):
	new_caption = "Digit recognition"
	if caption is not None and len(caption) > 0:
		new_caption += f" ({caption})"
	pygame.display.set_caption(new_caption)


def prepare_screenshot(screenshot: Image, debug: bool) -> Image:
	if debug:
		screenshot.save(Configuration.get_debug_file_path("0.original.png"))

	# Нейронная сеть принимает на вход цифру белого цвета на чёрном фоне
	screenshot = ImageOps.invert(screenshot)
	if debug:
		screenshot.save(Configuration.get_debug_file_path("1.inverted.png"))

	# Находим пиксели, не относящиеся к фону
	pixels = numpy.asarray(screenshot)
	image_pixels_indexes = numpy.where(pixels > 0)
	if image_pixels_indexes[0].size == 0:
		return None

	# Вырезаем цифру из изображения
	left_bound, top_bound, right_bound, bottom_bound =\
		min(image_pixels_indexes[1]),\
		min(image_pixels_indexes[0]),\
		max(image_pixels_indexes[1]),\
		max(image_pixels_indexes[0])
	if left_bound == right_bound or top_bound == bottom_bound:
		return None
	screenshot = screenshot.crop((left_bound, top_bound, right_bound, bottom_bound))
	if debug:
		screenshot.save(Configuration.get_debug_file_path("2.cropped.png"))

	# Вписываем изображение в минимальный квадрат так, чтобы цифра оказалась посередине
	square_size = max(right_bound - left_bound, bottom_bound - top_bound)
	square = Image.new("L", (square_size, square_size))
	left_bound = (square_size - screenshot.size[0]) // 2
	top_bound = (square_size - screenshot.size[1]) // 2
	square.paste(screenshot, (left_bound, top_bound))
	screenshot = square
	if debug:
		screenshot.save(Configuration.get_debug_file_path("3.squared.png"))

	return screenshot


if __name__ == '__main__':
	main()
