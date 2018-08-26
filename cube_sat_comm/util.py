import subprocess


def mk_dir_if_not_exists(path):
    path.mkdir(parents=True, exist_ok=True)  # Does nothing if it already exists


def str_arr_to_str(str_arr):
    full_str = ""
    for string in str_arr:
        full_str += string
        full_str += " "
    return full_str


def clean_check_output_subprocess(*args, **kwargs):
    return subprocess.check_output(*args, **kwargs).decode("utf-8").replace("\n", "")
