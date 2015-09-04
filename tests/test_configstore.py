import copy
import mock
import os
import yaml

from juju import configstore
from juju.exceptions import EnvironmentNotBootstrapped

from . import environment, testcase


class TestConfigStore(testcase.TestCase):

    @mock.patch.dict(os.environ, JUJU_HOME='/test/juju/home')
    def test_configstore_default_uses_juju_home(self):
        store = configstore.ConfigStore()
        expected = os.path.join(os.environ['JUJU_HOME'], 'environments')
        self.assertEqual(store.directory, expected)

    @mock.patch.dict(os.environ, HOME='/test/home', clear=True)
    def test_get_juju_home_through_home(self):
        store = configstore.ConfigStore()
        expected = os.path.join(os.environ['HOME'], '.juju', 'environments')
        self.assertEqual(store.directory, expected)

    def test_configstore_directory_set(self):
        store = configstore.ConfigStore('/use/this/dir')
        self.assertEqual(store.directory, '/use/this/dir')

    def test_parse_env_missing(self):
        temp_juju_home = self.mkdir()
        with mock.patch.dict('os.environ', {'JUJU_HOME': temp_juju_home}):
            store = configstore.ConfigStore()
            self.assertRaises(
                EnvironmentNotBootstrapped,
                store.connection_info,
                'missing')

    def test_parse_env_jenv(self):
        temp_juju_home = self.mkdir()
        environment.write_jenv(temp_juju_home, 'test-env')
        with mock.patch.dict('os.environ', {'JUJU_HOME': temp_juju_home}):
            store = configstore.ConfigStore()
            env = store.connection_info('test-env')
            self.assertEqual(env, environment.SAMPLE_CONFIG)

    def test_parse_cache_file(self):
        temp_juju_home = self.mkdir()
        environment.write_cache_file(temp_juju_home, 'test-env')
        with mock.patch.dict('os.environ', {'JUJU_HOME': temp_juju_home}):
            store = configstore.ConfigStore()
            env = store.connection_info('test-env')
            self.assertEqual(env, environment.SAMPLE_CONFIG)

    def test_parse_cache_file_missing_env(self):
        """Create a valid cache file, but look for an environment that isn't there.
        """
        temp_juju_home = self.mkdir()
        environment.write_cache_file(temp_juju_home, 'test-env')
        with mock.patch.dict('os.environ', {'JUJU_HOME': temp_juju_home}):
            store = configstore.ConfigStore()
            self.assertRaises(
                EnvironmentNotBootstrapped,
                store.connection_info,
                'missing')

    def test_parse_env_cache_file_first(self):
        """The cache file has priority over a jenv file."""
        temp_juju_home = self.mkdir()
        content = copy.deepcopy(environment.SAMPLE_CONFIG)
        environment.write_jenv(temp_juju_home, 'test-env', content)
        # Now change the password.
        content['password'] = 'new password'
        environment.write_cache_file(temp_juju_home, 'test-env', content)
        with mock.patch.dict('os.environ', {'JUJU_HOME': temp_juju_home}):
            store = configstore.ConfigStore()
            env = store.connection_info('test-env')
            self.assertEqual(env, content)
