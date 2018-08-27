import subprocess
from pathlib import Path

from cube_sat_comm import util

top = "."
out = "build"

_repo_dir_path = "/build/repos"

class _RepoDep:
    def __init__(self, url, commit_hash):
        self.url = url
        self.commit_hash = commit_hash


_repo_deps = [
    _RepoDep("https://github.com/libcsp/libcsp.git", "cd44a62")
]


def configure(ctx):
    _check_if_dependencies_are_installed(ctx)
    _clone_needed_repo_deps()


def _check_if_dependencies_are_installed(ctx):
    ctx.find_program("python2")
    ctx.find_program("git")
    ctx.find_program("gcc")


def _clone_needed_repo_deps():
    try:
        for repo_dep in _repo_deps:
            repo_url_path = Path(repo_dep.repo_url)
            repo_name = repo_url_path.stem
            repo_local_path = _repo_dir_path.joinpath(repo_name)
            util.mk_dir_if_not_exists(repo_local_path)

            _setup_repo_if_needed(repo_local_path, repo_dep)

    except subprocess.CalledProcessError as ex:
        pass

def build():
    pass


def _setup_repo_if_needed(repo_local_path, repo_dep):
    if not repo_exists(repo_local_path):
        print("Cloning \"{}\" into \"{}\"...".format(repo_dep.url_path, repo_local_path))
        subprocess.call(["git", "clone", repo_dep.repo_url, str(repo_local_path)])

    if not repo_head_is_on_commit(repo_dep.commit_hash, repo_local_path):
        print("Checking out the correct commit... ({})".format(repo_dep.commit_hash))
        subprocess.call(["git", "checkout", repo_dep.commit_hash], cwd=str(repo_local_path))


def repo_exists(repo_local_path):
    git_internals_folder_path = repo_local_path.joinpath(".git")
    return git_internals_folder_path.is_dir()


def repo_head_is_on_commit(commit_hash, repo_local_path):
    curr_head_commit_hash = util.clean_check_output_subprocess(["git", "rev-parse", "HEAD"], cwd=str(repo_local_path))
    return curr_head_commit_hash[:len(commit_hash)] == commit_hash
