import threading
import random
import time

from result import Ok, Err

from cube_sat_comm.drawing import curses_print
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
        MenuItem('exit', 'Exit the program', lambda: _exit(exit_state))
    ]

    _print_menu(menu_items)

    while not exit_state.get_state():
        res = _handle_given_user_input(menu_items)
        if res.is_err():
            curses_print("Error: {}".format(res.err()))


def _print_menu(menu_items):
    curses_print("---------- Menu ----------")
    for item in menu_items:
        curses_print("{} --> {}".format(item.get_input_str(), item.get_desc()))
    return Ok()


def _handle_given_user_input(menu_items):
    _input_state.last_input = prompt_for_input().lower()
    menu_item_name = _input_state.last_input.split(' ')[0]
    for item in menu_items:
        if menu_item_name == item.get_input_str():
            res = item.get_menu_func()()
            return res
    return Err("\"{}\" is not a valid option.".format(menu_item_name))


def _execute_command():
    menu_option_args = _input_state.last_input.split(' ')[1:]
    if len(menu_option_args) == 0:
        return Err("No command name given.")

    name = menu_option_args[0]
    args = menu_option_args[1:]
    execute_command(name, args)
    return Ok()


def _start_fake_task():
    time_to_run = random.random() * MAX_TASK_TIME_SECS
    thread = threading.Thread(target=_fake_task, args=(time_to_run,))
    thread.start()
    return Ok()


def _fake_task(time_to_run):
    time.sleep(time_to_run)
    curses_print("Task finished!")


def _exit(exit_state):
    exit_state.exit()
    return Ok()
