"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SCROLLBAR
ScrollBar class, manage the selection in a range of values.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

__all__ = ['ScrollBar']

import pygame
import pygame_menu.locals as _locals

from pygame_menu.utils import make_surface, assert_orientation, assert_color
from pygame_menu.widgets.core import Widget

from pygame_menu._types import Optional, List, VectorIntType, ColorType, Tuple2IntType, \
    CallbackType, NumberInstance, ColorInputType, NumberType, Literal, EventVectorType


# noinspection PyMissingOrEmptyDocstring
class ScrollBar(Widget):
    """
    A scroll bar include 3 separate controls: a slider, scroll arrows, and a page control:

        a. The slider provides a way to quickly go to any part of the document.
        b. The scroll arrows are push buttons which can be used to accurately navigate
           to a particular place in a document.
        c. The page control is the area over which the slider is dragged (the scroll bar's
           background). Clicking here moves the scroll bar towards the click by one page.

    .. note::

        This widget only accepts translation transformation.

    .. warning::

        Arrows are not yet implemented.

    :param length: Length of the page control
    :param values_range: Min and max values
    :param scrollbar_id: Bar identifier
    :param orientation: Bar orientation (horizontal or vertical). See :py:mod:`pygame_menu.locals`
    :param slider_pad: Space between slider and page control
    :param slider_color: Color of the slider
    :param page_ctrl_thick: Page control thickness
    :param page_ctrl_color: Page control color
    :param onchange: Callback when pressing and moving the scroll
    """
    _last_mouse_pos: Tuple2IntType
    _mouseover: bool
    _orientation: Literal[0, 1]
    _page_ctrl_color: ColorType
    _page_ctrl_length: NumberType
    _page_ctrl_thick: int
    _page_step: NumberType
    _shadow: bool
    _shadow_color: ColorType
    _shadow_offset: NumberType
    _shadow_position: str
    _shadow_tuple: Tuple2IntType
    _single_step: NumberType
    _slider_color: ColorType
    _slider_pad: int
    _slider_position: int
    _slider_rect: Optional['pygame.Rect']
    _values_range: List[NumberType]
    scrolling: bool

    def __init__(
            self,
            length: NumberType,
            values_range: VectorIntType,
            scrollbar_id: str = '',
            orientation: str = _locals.ORIENTATION_HORIZONTAL,
            slider_pad: NumberType = 0,
            slider_color: ColorInputType = (200, 200, 200),
            page_ctrl_thick: int = 20,
            page_ctrl_color: ColorInputType = (235, 235, 235),
            onchange: CallbackType = None,
            *args,
            **kwargs
    ) -> None:
        assert isinstance(length, NumberInstance)
        assert isinstance(values_range, (tuple, list))
        assert values_range[1] > values_range[0], 'minimum value first is expected'
        assert isinstance(slider_pad, NumberInstance)
        assert isinstance(page_ctrl_thick, int)
        assert page_ctrl_thick - 2 * slider_pad >= 2, 'slider shall be visible'

        slider_color = assert_color(slider_color)
        page_ctrl_color = assert_color(page_ctrl_color)

        super(ScrollBar, self).__init__(
            widget_id=scrollbar_id,
            onchange=onchange,
            args=args,
            kwargs=kwargs
        )

        self._last_mouse_pos = (-1, -1)
        self._mouseover = False
        self._orientation = 0  # 0: horizontal, 1: vertical
        self._values_range = list(values_range)

        self._page_ctrl_length = length
        self._page_ctrl_thick = page_ctrl_thick
        self._page_ctrl_color = page_ctrl_color

        self._slider_rect = None
        self._slider_pad = slider_pad
        self._slider_color = slider_color
        self._slider_position = 0

        # Shadow
        self._shadow = False
        self._shadow_color = (0, 0, 0)
        self._shadow_offset = 2.0
        self._shadow_position = _locals.POSITION_NORTHWEST
        self._shadow_tuple = (0, 0)  # (x px offset, y px offset)

        self._single_step = 20
        self._page_step = 0

        if values_range[1] - values_range[0] > length:
            self.set_page_step(length)
        else:
            self.set_page_step((values_range[1] - values_range[0]) / 5.0)  # Arbitrary

        self.set_orientation(orientation)

        # Configure publics
        self.is_scrollable = True
        self.is_selectable = False
        self.scrolling = False

    def scroll_to_widget(self, *args, **kwargs) -> 'ScrollBar':
        pass

    def _apply_font(self) -> None:
        pass

    def set_padding(self, *args, **kwargs) -> 'ScrollBar':
        return self

    def scale(self, *args, **kwargs) -> 'ScrollBar':
        return self

    def resize(self, *args, **kwargs) -> 'ScrollBar':
        return self

    def set_max_width(self, *args, **kwargs) -> 'ScrollBar':
        return self

    def set_max_height(self, *args, **kwargs) -> 'ScrollBar':
        return self

    def rotate(self, *args, **kwargs) -> 'ScrollBar':
        return self

    def flip(self, *args, **kwargs) -> 'ScrollBar':
        return self

    def _apply_size_changes(self) -> None:
        """
        Apply scrollbar changes.

        :return: None
        """
        opp_orientation = 1 if self._orientation == 0 else 0  # Opposite of orientation
        dims = ('width', 'height')
        setattr(self._rect, dims[self._orientation], self._page_ctrl_length)
        setattr(self._rect, dims[opp_orientation], self._page_ctrl_thick)
        self._slider_rect = pygame.Rect(0, 0, int(self._rect.width), int(self._rect.height))
        setattr(self._slider_rect, dims[self._orientation], self._page_step)
        setattr(self._slider_rect, dims[opp_orientation], self._page_ctrl_thick)

        # Update slider position according to the current one
        pos = ('x', 'y')
        setattr(self._slider_rect, pos[self._orientation], self._slider_position)
        self._slider_rect = self._slider_rect.inflate(-2 * self._slider_pad, -2 * self._slider_pad)

    def set_shadow(
            self,
            enabled: bool = True,
            color: Optional[ColorInputType] = None,
            position: Optional[str] = None,
            offset: int = 2
    ) -> 'ScrollBar':
        """
        Set the scrollbars shadow.

        .. note::

            See :py:mod:`pygame_menu.locals` for valid ``position`` values.

        :param enabled: Shadow is enabled or not
        :param color: Shadow color
        :param position: Shadow position
        :param offset: Shadow offset
        :return: Self reference
        """
        super(ScrollBar, self).set_font_shadow(enabled, color, position, offset)

        # Store shadow from font
        self._shadow = self._font_shadow
        self._shadow_color = self._font_shadow_color
        self._shadow_offset = self._font_shadow_offset
        self._shadow_position = self._font_shadow_position
        self._shadow_tuple = self._font_shadow_tuple

        # Disable font
        self._font_shadow = False
        return self

    def _draw(self, surface: 'pygame.Surface') -> None:
        surface.blit(self._surface, self._rect.topleft)

    def get_minimum(self) -> int:
        """
        Return the smallest acceptable value.

        :return: Smallest acceptable value
        """
        return int(self._values_range[0])

    def get_maximum(self) -> int:
        """
        Return the greatest acceptable value.

        :return: Greatest acceptable value
        """
        return int(self._values_range[1])

    def get_minmax(self) -> Tuple2IntType:
        """
        Return the min and max acceptabla tuple values.

        :return: Min, Max tuple
        """
        return self.get_minimum(), self.get_maximum()

    def get_orientation(self) -> str:
        """
        Return the scrollbar orientation (pygame-menu locals).

        :return: Scrollbar orientation
        """
        if self._orientation == 0:
            return _locals.ORIENTATION_HORIZONTAL
        else:
            return _locals.ORIENTATION_VERTICAL

    def get_page_step(self) -> int:
        """
        Return amount that the value changes by when the user
        click on the page control surface.

        :return: Page step
        """
        pstep = self._page_step * (self._values_range[1] - self._values_range[0]) / self._page_ctrl_length
        return int(pstep)

    def get_value_percentual(self) -> float:
        """
        Return the value but in percentage between ``0`` (minimum value) and ``1`` (maximum value).

        :return: Value as percentage
        """
        vmin, vmax = self.get_minmax()
        value = self.get_value()
        return round((value - vmin) / (vmax - vmin), 3)

    def get_value(self) -> int:
        """
        Return the value according to the slider position.

        :return: Position in pixels (px)
        """
        value = self._values_range[0] + self._slider_position * \
                (self._values_range[1] - self._values_range[0]) / (self._page_ctrl_length - self._page_step)

        # Correction due to value scaling
        value = max(self._values_range[0], value)
        value = min(self._values_range[1], value)
        return int(value)

    def _render(self) -> Optional[bool]:
        width, height = self._rect.width + self._rect_size_delta[0], self._rect.height + self._rect_size_delta[1]

        if not self._render_hash_changed(width, height, self._slider_rect.x, self._slider_rect.y,
                                         self._slider_rect.width, self._slider_rect.height, self._visible):
            return True

        self._surface = make_surface(width, height)
        self._surface.fill(self._page_ctrl_color)

        # Render slider
        if self._shadow:
            lit_rect = pygame.Rect(self._slider_rect)
            slider_rect = lit_rect.inflate(-self._shadow_offset * 2, -self._shadow_offset * 2)
            shadow_rect = lit_rect.inflate(-self._shadow_offset, -self._shadow_offset)
            shadow_rect = shadow_rect.move(self._shadow_tuple[0] / 2, self._shadow_tuple[1] / 2)

            pygame.draw.rect(self._surface, self._font_selected_color, lit_rect)
            pygame.draw.rect(self._surface, self._shadow_color, shadow_rect)
            pygame.draw.rect(self._surface, self._slider_color, slider_rect)
        else:
            pygame.draw.rect(self._surface, self._slider_color, self._slider_rect)

    def _scroll(self, rect: 'pygame.Rect', pixels: NumberType) -> bool:
        """
        Moves the slider based on mouse events relative to change along axis.
        The slider travel is limited to page control length.

        :param rect: Precomputed rect
        :param pixels: Number of pixels to scroll
        :return: ``True`` is scroll position has changed
        """
        assert isinstance(pixels, NumberInstance)
        if not pixels:
            return False

        axis = self._orientation
        space_before = rect.topleft[axis] - \
                       self._slider_rect.move(*rect.topleft).topleft[axis] + self._slider_pad
        move = max(round(pixels), space_before)
        space_after = rect.bottomright[axis] - \
                      self._slider_rect.move(*rect.topleft).bottomright[axis] - self._slider_pad
        move = min(move, space_after)

        if not move:
            return False

        move_pos = [0, 0]
        move_pos[axis] = move
        self._slider_rect.move_ip(*move_pos)
        self._slider_position += move
        return True

    def set_length(self, value: NumberType) -> None:
        """
        Set the length of the page control area.

        :param value: Length of the area
        :return: None
        """
        assert isinstance(value, NumberInstance)
        assert 0 < value
        self._page_ctrl_length = value
        self._slider_position = min(self._slider_position, self._page_ctrl_length - self._page_step)
        self._apply_size_changes()

    def get_thickness(self) -> int:
        """
        Return the thickness of the bar.

        :return: Thickness (px)
        """
        return self._page_ctrl_thick

    def set_maximum(self, value: NumberType) -> None:
        """
        Set the greatest acceptable value.

        :param value: Maximum value
        :return: None
        """
        assert isinstance(value, NumberInstance)
        assert value > self._values_range[0], 'maximum value shall greater than {}'.format(self._values_range[0])
        self._values_range[1] = value

    def set_minimum(self, value: NumberType) -> None:
        """
        Set the smallest acceptable value.

        :param value: Minimum value
        :return: None
        """
        assert isinstance(value, NumberInstance)
        assert 0 <= value < self._values_range[1], 'minimum value shall lower than {}'.format(self._values_range[1])
        self._values_range[0] = value

    def set_orientation(self, orientation: str) -> None:
        """
        Set the scroll bar orientation to vertical or horizontal.

        .. note::

            See :py:mod:`pygame_menu.locals` for valid ``orientation`` values.

        :param orientation: Widget orientation
        :return: None
        """
        assert_orientation(orientation)
        if orientation == _locals.ORIENTATION_HORIZONTAL:
            self._orientation = 0
        elif orientation == _locals.ORIENTATION_VERTICAL:
            self._orientation = 1
        self._apply_size_changes()

    def set_page_step(self, value: NumberType) -> None:
        """
        Set the amount that the value changes by when the user click on the
        page control surface.

        .. note::

            The length of the slider is related to this value, and typically
            represents the proportion of the document area shown in a scrolling view.

        :param value: Page step
        :return: None
        """
        assert isinstance(value, NumberInstance)
        assert 0 < value, 'page step shall be > 0'

        # Slider length shall represent the same ratio
        self._page_step = self._page_ctrl_length * value / (self._values_range[1] - self._values_range[0])

        if self._single_step >= self._page_step:
            self._single_step = self._page_step // 2  # Arbitrary to be lower than page step

        self._apply_size_changes()

    def set_value(self, position_value: NumberType) -> None:
        """
        Set the position of the scrollbar.

        :param position_value: Position
        :return: None
        """
        assert isinstance(position_value, NumberInstance)
        assert self._values_range[0] <= position_value <= self._values_range[1], \
            '{} < {} < {}'.format(self._values_range[0], position_value, self._values_range[1])

        pixels = (position_value - self._values_range[0]) * (self._page_ctrl_length - self._page_step)
        pixels /= (self._values_range[1] - self._values_range[0])

        # Correction due to value scaling
        pixels = max(0, pixels)
        pixels = min(self._page_ctrl_length - self._page_step, pixels)

        self._scroll(self.get_rect(), pixels - self._slider_position)

    def get_slider_rect(self) -> 'pygame.Rect':
        """
        Get slider rect.

        :return: Slider rect
        """
        return self._slider_rect.move(*self.get_rect(to_absolute_position=True).topleft)

    def update(self, events: EventVectorType) -> bool:
        if self.readonly or not self._visible:
            return False
        updated = False
        rect = self.get_rect(to_absolute_position=True)

        for event in events:

            if event.type == pygame.KEYDOWN:

                if self._keyboard_enabled and self._orientation == 1 and \
                        event.key in (pygame.K_PAGEUP, pygame.K_PAGEDOWN):
                    direction = 1 if event.key == pygame.K_PAGEDOWN else -1
                    keys_pressed = pygame.key.get_pressed()
                    step = self._page_step
                    if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
                        step *= 0.35
                    pixels = direction * step
                    if self._scroll(rect, pixels):
                        self.change()
                        updated = True

            elif self._mouse_enabled and event.type == pygame.MOUSEMOTION and hasattr(event, 'rel'):
                # If mouse outside region and scroll is on limits, ignore
                mx, my = pygame.mouse.get_pos()
                if self.scrolling and self.get_value_percentual() in (0, 1) and \
                        self.get_scrollarea() is not None and self.get_scrollarea().get_parent() is not None:
                    if self._orientation == 1:  # Vertical
                        h = self._slider_rect.height / 2
                        if my > (rect.bottom - h) or my < (rect.top + h):
                            continue
                    elif self._orientation == 0:  # Horizontal
                        w = self._slider_rect.width / 2
                        if mx > (rect.right - w) or mx < (rect.left + w):
                            continue

                # Check scrolling
                if self.scrolling and self._scroll(rect, event.rel[self._orientation]):
                    self.change()
                    updated = True

                # Check mouse over
                if rect.collidepoint(*event.pos):
                    if not self._mouseover:
                        self._mouseover = True
                        self.mouseover(event)
                else:
                    if self._mouseover:
                        self._mouseover = False
                        self.mouseleave(event)

            # Mouse enters or leaves the window
            elif event.type == pygame.ACTIVEEVENT:
                mx, my = pygame.mouse.get_pos()
                if event.gain != 1:  # Leave
                    self._last_mouse_pos = (mx, my)
                else:
                    lmx, lmy = self._last_mouse_pos
                    self._last_mouse_pos = (-1, -1)
                    if lmx == -1 or lmy == -1:
                        continue
                    if self.scrolling:
                        if self._orientation == 0:  # Horizontal
                            self._scroll(rect, mx - lmx)
                        else:
                            self._scroll(rect, my - lmy)

            elif self._mouse_enabled and event.type == pygame.MOUSEBUTTONDOWN:

                # Vertical bar: scroll down (4) or up (5). Mouse must be placed over the area to enable this feature
                if event.button in (4, 5) and self._orientation == 1 and \
                        (self._scrollarea is not None and self._scrollarea.mouse_is_over() or self._scrollarea is None):
                    direction = -1 if event.button == 4 else 1
                    if self._scroll(rect, direction * self._single_step):
                        self.change()
                        updated = True

                # Click button (left, middle, right)
                elif event.button in (1, 2, 3):
                    # The _slider_rect origin is related to the widget surface
                    if self.get_slider_rect().collidepoint(*event.pos):
                        # Initialize scrolling
                        self.scrolling = True

                    elif rect.collidepoint(*event.pos):
                        # Moves towards the click by one "page" (= slider length without pad)
                        srect = self.get_slider_rect()
                        pos = (srect.x, srect.y)
                        direction = 1 if event.pos[self._orientation] > pos[self._orientation] else -1
                        if self._scroll(rect, direction * self._page_step):
                            self.change()
                            updated = True

            # Releases mouse button
            elif self._mouse_enabled and event.type == pygame.MOUSEBUTTONUP:
                if self.scrolling:
                    self.scrolling = False
                    updated = True

        if updated:
            self.apply_update_callbacks()

        return updated
