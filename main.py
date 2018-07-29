import handle_user_input
import drawing

def main():
    drawing_handle = drawing.init_drawing_thread()
    handle_user_input.handle_input_loop() # Main thread handles user input

    drawing.stop_drawing_thread()
    drawing_handle.join()

main()