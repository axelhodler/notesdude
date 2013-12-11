import os.path
import ConfigParser

CONFIG_FILE = 'user.cfg'

class TestConfigFile():
    def test_if_config_exists(self):
        assert os.path.isfile(CONFIG_FILE), "config file does not exist"

    def test_if_config_section_exists(self):
        config = ConfigParser.RawConfigParser()
        try:
            config.read(CONFIG_FILE)
            assert True
        except ConfigParser.MissingSectionHeaderError:
            assert False, "the config file does not use a section part"

    def test_if_config_values_exist(self):
        config = ConfigParser.RawConfigParser()
        config.read(CONFIG_FILE)
        main_section = config.sections()[0]
        assert config.get(main_section, 'username') != ''
        assert config.get(main_section, 'password') != ''
