import curses

from cube_sat_comm import handle_user_input
from cube_sat_comm import drawing
from cube_sat_comm import curses_state
from cube_sat_comm import commands

def main(main_window):
    curses_state.init_state(main_window)
    commands.init_commands()
    drawing_handle = drawing.init_drawing_thread()

    handle_user_input.handle_input_loop()  # Main thread handles user input

    drawing.stop_drawing_thread()
    drawing_handle.join()


curses.wrapper(main)
