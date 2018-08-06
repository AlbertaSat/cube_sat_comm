import os
import pathlib

_COMMANDS_PATH = "commands/"


class DuplicateCommandException(Exception):
    pass


class CommandsState:
    def __init__(self):
        cmds_path = pathlib.Path(_COMMANDS_PATH)
        _mk_cmd_dir_if_not_exists(cmds_path)

        self._names_to_command_files = _load_in_commands(cmds_path)


def _mk_cmd_dir_if_not_exists(cmds_path):
    cmds_path.mkdir(parents=True, exist_ok=True)  # Does nothing if it already exists


def _load_in_commands(root_dir):
    name_to_cmd_map = {}

    for curr_dir_name, _, file_paths in os.walk(root_dir):
        full_file_paths = map(lambda f_name: (f_name, os.path.join(curr_dir_name, f_name)), file_paths)
        command_files = filter(lambda f: _is_command_file(f), full_file_paths)

        for (name, c_file_path) in command_files:
            if name in name_to_cmd_map:
                raise DuplicateCommandException("""More than one command file named {} found."
                                                ({} and {}))""".format(name, name_to_cmd_map[name], c_file_path))

            name_to_cmd_map[name] = c_file_path
    return name_to_cmd_map


def _is_command_file(name_and_full_path):
    name, full_path = name_and_full_path
    if name.suffix is not "py":
        return False

    # TODO: Probably add more checks once we know more about how command files are going to work...

    return True
