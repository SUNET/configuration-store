from os.path import join
from difflib import unified_diff

from typing import Optional
from git import Repo, InvalidGitRepositoryError, NoSuchPathError

from configstore.exceptions import InitError

# default_repo_dir = "/var/local/clixon-log"
default_repo_dir = "/home/johannes/code/configuration-store/.log"


class ConfigStore():
    def __init__(self, repo_dir: Optional[str] = default_repo_dir):
        """
        Create a ConfigStore object
        """
        self.__repo_dir = repo_dir
        self.__repo = self._load_or_init_repo(repo_dir)

        if (self.__repo.__class__ is Repo and not self.__repo.bare):
            print("Repo at {} successfully loaded.".format(repo_dir))
        else:
            print("Could not load nor init repository at {}".format(repo_dir))
            raise InitError("Failed to load or initialize repository at {}."
                            .format(repo_dir))

    def _load_or_init_repo(self, repo_dir):
        """
        Creates repo object from repo_dir. Creates the git repository if it
        does not exist already.
        """
        try:
            return Repo(repo_dir)
        except (InvalidGitRepositoryError, NoSuchPathError):
            r = Repo.init(join(repo_dir))
            r.description = "Configuration store log repository"
            r.index.commit("Init Configuration store")
            return r

    def print_changes_log(self, count):
        """
        Print diff information between subsequent commits.
        """
        commits = list(self.__repo.iter_commits("main"))

        for commit in commits:
            print("--{}--".format(str(commit.authored_datetime)))
            print("\"{}\"".format(commit.summary))
            print("\"{}\"".format(commit.hexsha))
            modified, added, deleted = self._get_diff(commit, commit.parents)
            for file, diff in modified:
                print("modified_files: {}\n {}".format(file, "\n".join(diff)))
            for file in added:
                print("added files: {}".format(added))
            for file in deleted:
                print("deleted files: {}".format(deleted))
            print()

    def _get_diff(self, commit, commit_parent):
        """
        Output diff on modified files only.

        :return:
            Tuple of lists with modified_files, added_files, deleted_files.
            note that modified_files is a list of tuples like (file name, diff)
        """
        if len(commit_parent) == 0:
            return [], [], []

        diff_index = commit_parent[0].diff(commit)

        #  iter_change_type: "M" - paths with modified data
        modified_files = []
        for file in diff_index.iter_change_type("M"):
            a_blob = file.a_blob.data_stream.read().decode("utf-8")
            b_blob = file.b_blob.data_stream.read().decode("utf-8")
            modified_files.append(
                (
                    file.a_path,
                    unified_diff(a_blob.splitlines(), b_blob.splitlines())
                )
            )

        #  iter_change_type: "A" - added paths
        added_files = []
        for file in diff_index.iter_change_type("A"):
            added_files.append(file.a_path)

        #  iter_change_type: "D" - deleted paths
        deleted_files = []
        for file in diff_index.iter_change_type("D"):
            deleted_files.append(file.a_path)

        return modified_files, added_files, deleted_files

    def print_repo_details(self):
        print(
            "{\n" +
            "  \"description\": \"{}\"\n".format(self.__repo.description) +
            "  \"branch\": \"{}\"\n".format(self.__repo.active_branch) +
            "  \"path\": \"{}\"\n".format(self.__repo.working_tree_dir) +
            "  \"latest\": {\n" +
            "    \"sha\": \"{}\"\n".format(
                str(self.__repo.head.commit.hexsha)) +
            "    \"timestamp\": \"{}\"\n".format(
                str(self.__repo.head.commit.authored_datetime)) +
            "  }\n" +
            "}")

    def store_conf(self, user, device_name, conf):
        """
        Store :conf: as content of file names :device_name: to disk.

        :param user:
        :param device_name:
            Device name will be used as file name to commit changes to.
        :conf:
            Content string to write to file.
        """
        # TODO: should handle multiple device_names and correlating confs

        if len(device_name) == 0:
            raise TypeError("device_name must not be empty")

        absolute_file_name = self._get_file_path(device_name)
        with open(absolute_file_name, "w") as device_file:
            device_file.write(conf)

        self.__repo.index.add([absolute_file_name])
        self.__repo.index.commit(
            "{{\"user\": \"{}\", \"device\": \"{}\"}}"
            .format(user, device_name))

    def get_conf(self, device_name):
        absolute_file_name = self._get_file_path(device_name)
        with open(absolute_file_name, "r+") as device_file:
            conf = device_file.read()

        return conf

    def _get_file_path(self, device_name):
        return join(self.__repo_dir, device_name)
