import os
import sys
import pathlib
import importlib

from cube_sat_comm.drawing import curses_print

_COMMANDS_PATH = "commands/"


class DuplicateCommandException(Exception):
    pass


class CommandsState:
    def __init__(self):
        cmds_path = pathlib.Path(_COMMANDS_PATH)
        _mk_cmd_dir_if_not_exists(cmds_path)

        self.names_to_command_files = _load_in_commands(cmds_path)


_commands_state: CommandsState = None


def init_commands():
    global _commands_state
    _commands_state = CommandsState()


def execute_command(name, args):
    if name not in _commands_state.names_to_command_files:
        curses_print("The command \"{}\" does not exist.".format(name))
        return

    mod = _commands_state.names_to_command_files[name]
    mod.run(args)


def _mk_cmd_dir_if_not_exists(cmds_path):
    cmds_path.mkdir(parents=True, exist_ok=True)  # Does nothing if it already exists


def _load_in_commands(root_dir):
    cmd_names_to_mods = {}
    root_mod_path = os.path.dirname(sys.modules['__main__'].__file__)

    for curr_dir_name, _, file_paths in os.walk(root_dir):
        full_file_paths = map(lambda f_name: (f_name, os.path.join(curr_dir_name, f_name)), file_paths)
        command_files = filter(lambda f: _is_command_file(f), full_file_paths)

        for (name, cmd_file_path) in command_files:
            if name in cmd_names_to_mods:
                raise DuplicateCommandException("""More than one command file named {} found."
                                                ({} and {}))""".format(name, cmd_names_to_mods[name], cmd_file_path))

            module = _import_module(cmd_file_path, root_mod_path)
            cmd_names_to_mods[name] = module
    return cmd_names_to_mods


def _import_module(full_cmd_path, root_mod_path):
    rel_path = full_cmd_path.relative_path(root_mod_path)
    return importlib.import_module(rel_path)


def _is_command_file(name_and_full_path):
    name, full_path = name_and_full_path
    if name.suffix is not "py":
        return False

    # TODO: Probably add more checks once we know more about how command files are going to work...

    return True
