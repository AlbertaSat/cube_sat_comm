from queue import Queue
from threading import Thread, Event

_MAX_QUEUE_MESSAGE_WAIT = 1.0

_queued_messages = Queue()
_should_exit = Event()
_new_messages_event = Event()


def init_drawing_thread():
    handle = Thread(target=_draw_thread_loop)
    handle.start()
    return handle


def queue_message(mess):
    _queued_messages.put(mess, True, _MAX_QUEUE_MESSAGE_WAIT)
    _new_messages_event.set()


def stop_drawing_thread():
    _should_exit.set()
    _new_messages_event.set()  # To get the thread to exit nicely


def _draw_thread_loop():
    while not _should_exit.is_set():
        while not _queued_messages.empty():
            message = _queued_messages.get()
            print(message)

        _new_messages_event.wait()
        _new_messages_event.clear()

