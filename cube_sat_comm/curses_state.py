import os
import curses
from curses.textpad import Textbox

from cube_sat_comm import drawing

_INPUT_TEXT_NUM_LINES = 1
_TITLE_HEIGHT = 1
_DASH_TITLE_LENGTH_PERC = 0.50


class CursesState:
    def __init__(self, main_window):
        self.main_win = main_window

        screen_max_y, screen_max_x = self.main_win.getmaxyx()
        output_win_num_lines = screen_max_y - _INPUT_TEXT_NUM_LINES - _TITLE_HEIGHT * 2

        output_title_beg_y = 0
        output_win_beg_y = output_title_beg_y + _TITLE_HEIGHT
        input_title_beg_y = output_win_beg_y + output_win_num_lines
        input_win_beg_y = input_title_beg_y + _TITLE_HEIGHT

        self.output_win_title = curses.newwin(_TITLE_HEIGHT, screen_max_x, output_title_beg_y, 0)
        self.output_win = curses.newwin(output_win_num_lines, screen_max_x, output_win_beg_y, 0)
        self.input_win_title = curses.newwin(_TITLE_HEIGHT, screen_max_x, input_title_beg_y, 0)
        self.input_win = curses.newwin(_INPUT_TEXT_NUM_LINES, screen_max_x, input_win_beg_y, 0)

        self.input_win_tb = Textbox(self.input_win)
        self.input_win_tb.stripspaces = True  # Seems to be broken...

        self._init_title_texts()

        self.output_win.scrollok(True)

    def _init_title_texts(self):
        self._init_title_text(self.output_win_title, " OUTPUT ")
        self._init_title_text(self.input_win_title, " INPUT ")

    @staticmethod
    def _init_title_text(win, text):
        win_y, win_x = win.getmaxyx()
        half_text_len = (len(text) // 2)
        max_dashes_per_side = int(_DASH_TITLE_LENGTH_PERC * win_x / 2)
        num_dashes_per_side = max_dashes_per_side - half_text_len
        title_text = ("-" * num_dashes_per_side) + text + ("-" * num_dashes_per_side)
        start_x = (win_x // 2) - half_text_len - num_dashes_per_side

        win.addstr(0, start_x, title_text)
        win.refresh()


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
