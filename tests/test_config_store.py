import unittest
import tempfile

from configstore.config_store import ConfigStore


class TestConfStore(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.conf_store = ConfigStore(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_print_repo_details(self):
        try:
            print(self.conf_store)
        except Exception:
            self.fail("__str__() raised Exception unexpectedly!")

    def test_print_changes_log(self):
        self.conf_store.store_conf("user_a", "device_1337", "configuration")
        try:
            self.conf_store.print_changes_log(4)
        except Exception:
            self.fail("print_commits(1) raised Exception unexpectedly!")

    def test_store_conf_do_not_allow_empty_device_name(self):
        self.assertRaises(
            TypeError,
            lambda: self.conf_store.store_conf("UserEmpty", "", "conf content")
        )

    def test_store_conf_saves_latest(self):
        self.conf_store.store_conf("user_a", "device_1", "<a x=\"1\">\n</a>\n")
        conf_b = "<a x=\"1\">\n<b y=\"2\"></b>\n</a>\n"
        self.conf_store.store_conf("user_b", "device_1", conf_b)
        conf = self.conf_store.get_conf("device_1")
        self.assertEqual(conf, conf_b)


if __name__ == "__main__":
    unittest.main()
