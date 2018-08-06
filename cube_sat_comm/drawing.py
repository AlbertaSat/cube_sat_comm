from queue import Queue
from threading import Thread, Event

from cube_sat_comm.curses_state import curses_print

_MAX_QUEUE_WAIT = 1.0

_queued_tasks = Queue()
_should_exit = Event()
_new_tasks_event = Event()


def init_drawing_thread():
    handle = Thread(target=_draw_thread_loop)
    handle.start()
    return handle


def queue_message(mess):
    _queued_tasks.put(lambda: _print_to_output(mess), True, _MAX_QUEUE_WAIT)
    _new_tasks_event.set()


def queue_task(task):
    _queued_tasks.put(task, True, _MAX_QUEUE_WAIT)
    _new_tasks_event.set()


def stop_drawing_thread():
    _should_exit.set()
    _new_tasks_event.set()  # To get the thread to exit nicely


def _draw_thread_loop():
    while not _should_exit.is_set():
        while not _queued_tasks.empty():
            _queued_tasks.get()()

        _new_tasks_event.wait()
        _new_tasks_event.clear()


def _print_to_output(mess):
    curses_print(mess)
