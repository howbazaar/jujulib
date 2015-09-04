import mock
import os
import unittest

import juju

from . import environment, testcase


class TestEnvironment(testcase.TestCase):

    def test_environment_not_running(self):
        # If there is no connection info for the environment name,
        # the environment isn't running.
        env = juju.Environment("testing")

        temp_juju_home = self.mkdir()
        with mock.patch.dict('os.environ', {'JUJU_HOME': temp_juju_home}):
            self.assertFalse(env.running)

    def test_environment_running(self):
        env = juju.Environment("testing")

        temp_juju_home = self.mkdir()
        environment.write_jenv(temp_juju_home, 'testing')
        with mock.patch.dict('os.environ', {'JUJU_HOME': temp_juju_home}):
            self.assertTrue (env.running)

    def test_status(self):
        env = juju.Environment("testing")
        config = {'FullStatus.return_value': "status result"}
        with mock.patch.object(juju.Environment, 'client', **config):
            result = env.status()
            self.assertEqual(result, "status result")
