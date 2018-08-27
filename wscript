#!/usr/bin/env python3

import platform
import subprocess
from pathlib import Path

from cube_sat_comm import util

top = "."
out = "build"

_repo_dir_path = "build/repos"
_libcsp_dir_path = "{}/libcsp".format(_repo_dir_path)
_libcsp_build_path = "{}/build".format(_libcsp_dir_path)


class _RepoDep:
    def __init__(self, url_path, commit_hash):
        self.url_path = url_path
        self.commit_hash = commit_hash


_repo_deps = [
    _RepoDep("https://github.com/libcsp/libcsp.git", "cd44a62")
]


def configure(ctx):
    _check_if_dependencies_are_installed(ctx)
    _clone_needed_repo_deps(ctx)


def _setup_dep_waf_config_args(bld):
    (os_arg, usart_arg) = _get_os_arg_for_libcsp(bld)
    return [str("".join(bld.env.PYTHON2)), "./waf", "configure", "--with-os={}".format(os_arg),
            "--with-driver-usart={}".format(usart_arg)]


def _check_if_dependencies_are_installed(ctx):
    ctx.find_program("python2", var="PYTHON2")


def _clone_needed_repo_deps(ctx):
    try:
        for repo_dep in _repo_deps:
            repo_url_path = Path(repo_dep.url_path)
            repo_name = repo_url_path.stem
            repo_local_path = Path(_repo_dir_path).joinpath(repo_name)
            util.mk_dir_if_not_exists(repo_local_path)

            _setup_repo_if_needed(repo_local_path, repo_dep)

    except subprocess.CalledProcessError as ex:
        ctx.fatal("Failed with error code {} and output the following: \"{}\".".format(ex.returncode, ex.output))


def build(bld):
    _configure_libcsp(bld)
    _build_python_bindings(bld)
    subprocess.call(["".join(bld.env.PYTHON2), "./waf", "build"], cwd=_libcsp_dir_path)


def _configure_libcsp(bld):
    args = _setup_dep_waf_config_args(bld)
    subprocess.call(args, cwd=_libcsp_dir_path)


def _setup_repo_if_needed(repo_local_path, repo_dep):
    if not repo_exists(repo_local_path):
        print("Cloning \"{}\" into \"{}\"...".format(repo_dep.url_path, repo_local_path))
        subprocess.call(["git", "clone", repo_dep.url_path, str(repo_local_path)])

    if not repo_head_is_on_commit(repo_dep.commit_hash, repo_local_path):
        print("Checking out the correct commit... ({})".format(repo_dep.commit_hash))
        subprocess.call(["git", "checkout", repo_dep.commit_hash], cwd=str(repo_local_path))


def repo_exists(repo_local_path):
    git_internals_folder_path = repo_local_path.joinpath(".git")
    return git_internals_folder_path.is_dir()


def repo_head_is_on_commit(commit_hash, repo_local_path):
    curr_head_commit_hash = util.clean_check_output_subprocess(["git", "rev-parse", "HEAD"], cwd=str(repo_local_path))
    return curr_head_commit_hash[:len(commit_hash)] == commit_hash


def _get_os_arg_for_libcsp(ctx):
    sys_name = platform.system()
    if sys_name == "Linux":
        return "posix", "linux"
    if sys_name == "Windows":
        return "windows", "windows"
    if sys_name == "Darwin":
        return "macosx", "none"

    ctx.fatal("Unknown OS type. (Found {})".format(sys_name))


def _build_python_bindings(bld):
    pass
