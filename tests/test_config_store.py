import unittest

from configstore.config_store import ConfigStore


class TestAuditLogger(unittest.TestCase):
    def setUp(self):
        self.conf_store = ConfigStore()

    def tearDown(self):
        pass

    def test_print_repo_details(self):
        try:
            self.conf_store.print_repo_details()
        except Exception:  # TODO: Exception type
            self.fail("print_repo() raised ExceptionType unexpectedly!")

    def test_print_changes_log(self):
        try:
            self.conf_store.print_changes_log(2)
        except Exception:  # TODO: Exception type
            self.fail("print_commits(1) raised ExceptionType unexpectedly!")


if __name__ == "__main__":
    unittest.main()
