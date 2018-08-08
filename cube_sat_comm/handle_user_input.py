import threading
import random
import time

from result import Ok, Err

from cube_sat_comm.drawing import queue_message
from cube_sat_comm.curses_state import prompt_for_input
from cube_sat_comm.commands import execute_command

MAX_TASK_TIME_SECS = 10


class InputState:
    def __init__(self):
        self.last_input = None


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


_input_state = InputState()


def handle_input_loop():
    exit_state = ExitState()

    menu_items = [
        MenuItem('help', 'Display availaible commands', lambda: _print_menu(menu_items)),
        MenuItem('test', 'Run a fake task on another thread', _start_fake_task),
        MenuItem('cmd', "Run a command", _execute_command),
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
    _input_state.last_input = prompt_for_input().lower()
    menu_item_name = _input_state.last_input.split(' ')[0]
    queue_message("")
    for item in menu_items:
        if menu_item_name == item.get_input_str():
            item.get_menu_func()()
            return
    queue_message("\"{}\" is not a valid option.".format(_input_state.last_input))


def _execute_command(name):
    args = _input_state[1:]
    execute_command(name, args)


def _start_fake_task():
    time_to_run = random.random() * MAX_TASK_TIME_SECS
    thread = threading.Thread(target=_fake_task, args=(time_to_run,))
    thread.start()


def _fake_task(time_to_run):
    time.sleep(time_to_run)
    queue_message("Task finished!")


