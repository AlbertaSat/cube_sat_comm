import os
import sys
import pathlib
import importlib

from result import Err

from cube_sat_comm import util


class DuplicateCommandException(Exception):
    pass


class CommandsState:
    def __init__(self, cmds_path):
        cmds_path = pathlib.Path(cmds_path)
        util.mk_dir_if_not_exists(cmds_path)

        self.names_to_command_files = _load_in_commands(cmds_path)


_commands_state: CommandsState = None


def init_commands(cmds_path):
    global _commands_state
    _commands_state = CommandsState(cmds_path)


def execute_command(name, args):
    if name not in _commands_state.names_to_command_files:
        return Err("The command \"{}\" does not exist.".format(name))

    mod = _commands_state.names_to_command_files[name]
    res = mod.run(args)
    return res


def _load_in_commands(root_dir):
    cmd_names_to_mods = {}
    root_mod_path = os.path.dirname(sys.modules['__main__'].__file__)

    for curr_dir_name, _, file_names in os.walk(root_dir):
        full_file_paths = map(lambda f_name: pathlib.PurePath(curr_dir_name).joinpath(f_name), file_names)
        cmd_file_paths = filter(lambda f_path: _is_command_file(f_path), full_file_paths)

        for cmd_file_path in cmd_file_paths:
            name = cmd_file_path.stem
            if name in cmd_names_to_mods:
                raise DuplicateCommandException("""More than one command file named {} found."
                                                ({} and {}))""".format(name, cmd_names_to_mods[name], cmd_file_path))

            module = _import_module(cmd_file_path)
            cmd_names_to_mods[name] = module
    return cmd_names_to_mods


def _import_module(mod_path):
    mod_path = str(mod_path).replace(".py", "").replace("/", ".")
    return importlib.import_module(mod_path)


def _is_command_file(cmd_path):
    if cmd_path.suffix != ".py":
        return False

    if cmd_path.stem == "__init__":
        return False

    # TODO: Probably add more checks once we know more about how command files are going to work...
    return True
