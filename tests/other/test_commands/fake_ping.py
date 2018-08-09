from result import Ok, Err


def run(success_callback):
    success_callback()
    return Ok()