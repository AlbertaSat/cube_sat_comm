import traceback
import curses

from cube_sat_comm import handle_user_input
from cube_sat_comm import drawing
from cube_sat_comm import curses_state
from cube_sat_comm import commands

_COMMANDS_PATH = "commands/"


def main():
    drawing_handle = None
    try:
        drawing_handle = drawing.init_drawing_thread()
        commands.init_commands(_COMMANDS_PATH)

        curses.wrapper(_run)

    except Exception as ex:
        print("The following exception has occurred: {}".format(ex))
        print("Stacktrace: {}".format(traceback.format_exc()))

    drawing.stop_drawing_thread()
    drawing_handle.join()


def _run(main_window):
    curses_state.init_state(main_window)
    handle_user_input.handle_input_loop()  # Main thread handles user input


main()

