from os.path import join
from difflib import unified_diff

from typing import Optional
from git import Repo, InvalidGitRepositoryError, NoSuchPathError

from configstore.exceptions import InitError
from configstore.log import get_logger

default_repo_dir = "/var/local/clixon-log"


class ConfigStore():
    def __init__(self, repo_dir: Optional[str] = default_repo_dir):
        """Create a ConfigStore object."""
        self.__repo_dir = repo_dir
        self.__log = get_logger()
        self.__repo = self._load_or_init_repo(repo_dir)

        if (self.__repo.__class__ is Repo and not self.__repo.bare):
            self.__log.info(
                "Repo successfully attached at {}.".format(repo_dir))
        else:
            self.__log.error(
                "Could not load nor init repository at {}".format(repo_dir))
            raise InitError("Failed to load or initialize repository at {}."
                            .format(repo_dir))

    def _load_or_init_repo(self, repo_dir):
        """Tries to load repo object from repo_dir. Tries to initialize repo if
        loading fails.
        """
        try:
            return Repo(repo_dir)
        except (InvalidGitRepositoryError, NoSuchPathError):
            self.__log.info(
                "Failed to load repo at {}. Trying to initialize new repo"
                .format(repo_dir))
            r = Repo.init(join(repo_dir))
            r.description = "Configuration store log repository"
            r.index.commit("Init Configuration store")
            return r

    def __str__(self):
        return ("{{\n"
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

    def print_changes_log(self, count):
        """Print diff information between subsequent commits."""
        commits_count = self.__repo.tree().size
        if count > commits_count:
            count = commits_count

        commits = list(self.__repo.iter_commits("main", max_count=count))
        for commit in commits:
            print("\n--{}--".format(str(commit.authored_datetime)))
            print("\"{}\"".format(commit.summary))
            print("\"SHA {}\"".format(commit.hexsha))
            modified, added, deleted = self._get_diff(commit, commit.parents)
            for file, diff in modified:
                print("modified_files: {}\n{}".format(file, "\n".join(diff)))
            for file in added:
                print("added files: {}".format(added))
            for file in deleted:
                print("deleted files: {}".format(deleted))
            print()

    def _get_diff(self, commit, commit_parent):
        """Output diff on modified files only.

        :return:
            Tuple of lists with modified_files, added_files, deleted_files.
            note that modified_files is a list of tuples like (file name, diff)
        """
        if len(commit_parent) == 0:
            return [], [], []
        diff_index = commit_parent[0].diff(commit)

        added_files = []
        deleted_files = []
        modified_files = []

        for idx in diff_index:
            match idx.change_type:
                case "A":
                    # added paths
                    added_files.append(idx.a_path)
                case "M":
                    # paths with modified data
                    a_blob = idx.a_blob.data_stream.read().decode("utf-8")
                    b_blob = idx.b_blob.data_stream.read().decode("utf-8")
                    diff = unified_diff(
                        a_blob.splitlines(),
                        b_blob.splitlines())
                    modified_files.append((idx.a_path, diff))
                case "D":
                    # deleted paths
                    deleted_files.append(idx.a_path)
                case "_":
                    print("TODO: support change_type == {}"
                          .format(idx.change_type))

        return modified_files, added_files, deleted_files

    def store_conf(self, user, conf_per_device):
        """Store as content of file names device_name to disk.

        :param user:
        :param conf_per_device:
            list of 2-tuples with (device_name and conf)
            device_name will be used as file name and conf will be content of
            file.
        """
        for (device_name, conf) in conf_per_device:
            if len(device_name) == 0:
                raise TypeError("device_name must not be empty")

            absolute_file_name = self._get_file_path(device_name)
            with open(absolute_file_name, "w") as device_file:
                device_file.write(conf)

            self.__repo.index.add([absolute_file_name])
            self.__repo.index.commit(
                "{{\"user\": \"{}\", \"device\": \"{}\"}}"
                .format(user, device_name))

    def get_current_conf(self):
        """
        Get current conf as a list of 2-tuples containing (device_name, config)

        Note that device_name is the same as path since we assume a flat
        file structure in the repo.
        """
        latest_tree = self.__repo.head.commit.tree
        return [(blobs.path, blobs.data_stream.read().decode())
                for blobs in latest_tree]

    def get_current_conf_for(self, device_name):
        """Get device's current conf."""
        latest_blob = self.__repo.head.commit.tree[device_name]
        return latest_blob.data_stream.read().decode()

    def get_conf_history(self, device_name):
        """Get history of full config file for :device_name:"""
        commits_for_file = self.__repo.iter_commits(
            all=True, paths=device_name)
        confs = []
        for commit in commits_for_file:
            confs.append(commit.tree[device_name].data_stream.read().decode())
        return confs

    def _get_file_path(self, device_name):
        return join(self.__repo_dir, device_name)
