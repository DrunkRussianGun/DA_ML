from typing import Callable, Tuple


class DragAndDropController:
	def __init__(
			self,
			mouse_position_getter: Callable[[], Tuple[float, float]],
			drag_action: Callable[[Tuple[float, float], Tuple[float, float]], None]):
		self.__dragging_started = False
		self.__mouse_position_getter = mouse_position_getter
		self.__mouse_position = (0.0, 0.0)
		self.__drag_action = drag_action

	def start_dragging(self):
		self.__dragging_started = True
		self.__mouse_position = self.__mouse_position_getter()

	def move(self):
		if not self.__dragging_started or self.__drag_action is None:
			return

		new_mouse_position = self.__mouse_position_getter()
		self.__drag_action(self.__mouse_position, new_mouse_position)
		self.__mouse_position = new_mouse_position

	def stop_dragging(self):
		self.__dragging_started = False
