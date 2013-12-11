import os.path

CONFIG_FILE = 'user.cfg'

class TestConfigFile():
    def test_if_config_exists(self):
        assert os.path.isfile(CONFIG_FILE), "config file does not exist"
