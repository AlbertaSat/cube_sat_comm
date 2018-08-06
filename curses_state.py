import os
import curses
from curses.textpad import Textbox

import drawing

_INPUT_TEXT_NUM_LINES = 1


class CursesState:
    def __init__(self, main_window):
        self.main_win = main_window

        screen_y, screen_x = self.main_win.getmaxyx()
        output_win_num_lines = screen_y - _INPUT_TEXT_NUM_LINES
        input_win_begin_y = output_win_num_lines

        self.output_win = curses.newwin(output_win_num_lines, screen_x, 0, 0)
        self.input_win = curses.newwin(_INPUT_TEXT_NUM_LINES, screen_x, input_win_begin_y, 0)
        self.input_win_tb = Textbox(self.input_win)
        self.input_win_tb.stripspaces = True  # Seems to be broken...

        self.output_win.scrollok(True)


_state = None


def init_state(main_window):
    global _state
    _state = CursesState(main_window)


def prompt_for_input(prompt=None):
    if prompt is not None:
        _state.input_win.addstr(prompt)
    _state.input_win_tb.edit()
    user_input = _state.input_win_tb.gather().strip()
    _queue_clear_input_tb()
    return user_input


def _queue_curses_print(mess):
    drawing.queue_task(lambda: curses_print(mess))


def _queue_clear_input_tb():
    drawing.queue_task(lambda: _state.input_win.clear())


def curses_print(mess):
    _state.output_win.addstr(mess + os.linesep)
    _set_cursor_back_to_input()
    _state.output_win.refresh()


def _set_cursor_back_to_input():
    y_cur, x_cur = _state.input_win.getbegyx()
    curses.setsyx(y_cur, x_cur)
    _state.input_win.refresh()
