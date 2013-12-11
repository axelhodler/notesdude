import os.path
import ConfigParser

CONFIG_FILE = 'user.cfg'

class TestConfigFile():
    def test_if_config_exists(self):
        assert os.path.isfile(CONFIG_FILE), "config file does not exist"

    def test_if_config_header_exists(self):
        config = ConfigParser.RawConfigParser()
        try:
            config.read(CONFIG_FILE)
            assert True
        except ConfigParser.MissingSectionHeaderError:
            assert False, "the config file does not use a header part"

    def test_if_config_values_exist(self):
        config = ConfigParser.RawConfigParser()
        config.read(CONFIG_FILE)
        header = config.sections()[0]
        assert config.get(header, 'username') != ''
        assert config.get(header, 'password') != ''
