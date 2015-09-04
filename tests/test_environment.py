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
