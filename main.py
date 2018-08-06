import curses

import handle_user_input
import drawing
import curses_state


def main(main_window):
    curses_state.init_state(main_window)
    drawing_handle = drawing.init_drawing_thread()
    handle_user_input.handle_input_loop()  # Main thread handles user input

    drawing.stop_drawing_thread()
    drawing_handle.join()


curses.wrapper(main)
