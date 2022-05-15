"""
pygame-menu
https://github.com/ppizarror/pygame-menu

CONTROLS
Default controls of Menu object and key definition.
"""

__all__ = [

    # Joy pad
    'JOY_AXIS_X',
    'JOY_AXIS_Y',
    'JOY_BUTTON_BACK',
    'JOY_BUTTON_SELECT',
    'JOY_DEADZONE',
    'JOY_DELAY',
    'JOY_DOWN',
    'JOY_LEFT',
    'JOY_REPEAT',
    'JOY_RIGHT',
    'JOY_UP',

    # Keyboard events
    'KEY_APPLY',
    'KEY_BACK',
    'KEY_CLOSE_MENU',
    'KEY_LEFT',
    'KEY_MOVE_DOWN',
    'KEY_MOVE_UP',
    'KEY_RIGHT',

    # Controller object
    'Controller'

]

# Imports
import pygame.locals as _locals
from pygame.event import Event as EventType
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from pygame_menu.menu import Menu
    from pygame_menu.widgets import Widget

# Joy pad
JOY_AXIS_X = 0
JOY_AXIS_Y = 1
JOY_BUTTON_BACK = 1
JOY_BUTTON_SELECT = 0
JOY_DEADZONE = 0.5
JOY_DELAY = 300  # ms
JOY_DOWN = (0, -1)
JOY_LEFT = (-1, 0)
JOY_REPEAT = 100  # ms
JOY_RIGHT = (1, 0)
JOY_UP = (0, 1)

# Keyboard events
KEY_APPLY = _locals.K_RETURN
KEY_BACK = _locals.K_BACKSPACE
KEY_CLOSE_MENU = _locals.K_ESCAPE
KEY_LEFT = _locals.K_LEFT
KEY_MOVE_DOWN = _locals.K_UP
KEY_MOVE_UP = _locals.K_DOWN  # Consider keys are "inverted"
KEY_RIGHT = _locals.K_RIGHT
KEY_TAB = _locals.K_TAB


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class Controller(object):
    """
    Controller class. Accepts any object and provides functions to handle each
    event.
    """
    joy_delay: int
    joy_repeat: int

    def __init__(self) -> None:
        self.joy_delay = JOY_DELAY
        self.joy_repeat = JOY_REPEAT

    def apply(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts apply. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == KEY_APPLY

    def back(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts back. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == KEY_BACK

    def close_menu(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts close menu. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == KEY_CLOSE_MENU

    def escape(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts escape. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == _locals.K_ESCAPE

    def joy_axis_x_left(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts joy movement on x-axis (left direction). Requires ``pygame.JOYAXISMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.axis == JOY_AXIS_X and event.value < -JOY_DEADZONE

    def joy_axis_x_right(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts joy movement on x-axis (right direction). Requires ``pygame.JOYAXISMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.axis == JOY_AXIS_X and event.value > JOY_DEADZONE

    def joy_axis_y_down(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts joy movement on y-axis (down direction). Requires ``pygame.JOYAXISMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.axis == JOY_AXIS_Y and event.value > JOY_DEADZONE

    def joy_axis_y_up(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts joy movement on y-axis (up direction). Requires ``pygame.JOYAXISMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.axis == JOY_AXIS_Y and event.value < -JOY_DEADZONE

    def joy_back(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts joy back button. Requires ``pygame.JOYBUTTONDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.button == JOY_BUTTON_BACK

    def joy_down(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts joy movement to down direction. Requires ``pygame.JOYHATMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.value == JOY_DOWN

    def joy_left(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts joy movement to left direction. Requires ``pygame.JOYHATMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.value == JOY_LEFT

    def joy_right(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts joy movement to right direction. Requires ``pygame.JOYHATMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.value == JOY_RIGHT

    def joy_select(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts joy select button. Requires ``pygame.JOYBUTTONDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.button == JOY_BUTTON_SELECT

    def joy_up(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts joy movement to up direction. Requires ``pygame.JOYHATMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.value == JOY_UP

    def left(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts left. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == KEY_LEFT

    def move_down(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts move down. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == KEY_MOVE_DOWN

    def move_up(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts move up. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == KEY_MOVE_UP

    def right(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts right. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == KEY_RIGHT

    def tab(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts tab. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == KEY_TAB
