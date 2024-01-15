from os.path import join

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
        self.__repo = self.load_or_init_repo(repo_dir)

        if (self.__repo.__class__ is Repo and not self.__repo.bare):
            print("Repo at {} successfully loaded.".format(repo_dir))
        else:
            print("Could not load nor init repository at {}".format(repo_dir))
            raise InitError("Failed to load or initialize repository at {}."
                            .format(repo_dir))

    def load_or_init_repo(self, repo_dir):
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
        TODO: print diffs between commits as this is of interest

        Print information from git commits.
        """
        commits = list(self.__repo.iter_commits("main"))[:count]
        for commit in commits:
            print("----")
            print(str(commit.authored_datetime))
            print("\"{}\"".format(commit.summary))
            print(str("count: {} and size: {}".format(commit.count(),
                                                      commit.size)))

    def print_repo_details(self):
        print("Description: {}".format(self.__repo.description))
        print("Active branch: {}".format(self.__repo.active_branch))
        print("Path: {}".format(self.__repo.working_tree_dir))
        print("Last commit: {}.".format(str(self.__repo.head.commit.hexsha)))
        print("Last commit time: {}.".format(
            str(self.__repo.head.commit.authored_datetime)))

    def store_conf(self, user, device_name):
        """
        Assume flat structure under repository where device names will be saved
        as files.

        :param user:
        :param device_name:
            Device name changes apply to will be used as file name to commit.
        """

        absolute_file_name = join(self.__repo_dir, device_name)

        #  TODO: proper file management
        open(absolute_file_name, "wb").close()  # write binary TODO delete

        self.__repo.index.add([absolute_file_name])
        self.__repo.index.commit("{} updates {}".format(user, device_name))
