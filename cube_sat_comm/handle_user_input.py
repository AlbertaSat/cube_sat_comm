import threading
import random
import time

from cube_sat_comm.drawing import queue_message
from cube_sat_comm.curses_state import prompt_for_input

MAX_TASK_TIME_SECS = 10


class ExitState:
    def __init__(self):
        self._exit = False

    def get_state(self):
        return self._exit

    def exit(self):
        self._exit = True


class MenuItem:
    def __init__(self, input_str, desc, menu_func):
        self._input_str = input_str
        self._desc = desc
        self._menu_func = menu_func

    def get_input_str(self):
        return self._input_str

    def get_desc(self):
        return self._desc

    def get_menu_func(self):
        return self._menu_func


def handle_input_loop():
    exit_state = ExitState()
    menu_items = [
        MenuItem('help', 'Display availaible commands', lambda: _print_menu(menu_items)),
        MenuItem('test', 'Run a fake task on another thread', _start_fake_task),
        MenuItem('exit', 'Exit the program', exit_state.exit)
    ]

    _print_menu(menu_items)

    while not exit_state.get_state():
        _handle_given_user_input(menu_items)


def _print_menu(menu_items):
    queue_message("---------- Menu ----------")
    for item in menu_items:
        queue_message("{} --> {}".format(item.get_input_str(), item.get_desc()))


def _handle_given_user_input(menu_items):
    user_input = prompt_for_input().lower()
    queue_message("")
    for item in menu_items:
        if user_input == item.get_input_str():
            item.get_menu_func()()
            return
    queue_message("\"{}\" is not a valid option.".format(user_input))


def _start_fake_task():
    time_to_run = random.random() * MAX_TASK_TIME_SECS
    thread = threading.Thread(target=_fake_task, args=(time_to_run,))
    thread.start()


def _fake_task(time_to_run):
    time.sleep(time_to_run)
    queue_message("Task finished!")