from .apiclient import open_environment
from .configstore import ConfigStore
from .exceptions import EnvironmentNotBootstrapped


class Environment(object):
    """Represents an environment in a Juju System.

    The environment may be the initial environment of the system itself.
    """

    def __init__(self, name):
        self.name = name

    @property
    def running(self):
        # If there are cached values saved for the environment then it is, by
        # our definition, running.
        try:
            self.connection_info()
            return True
        except EnvironmentNotBootstrapped:
            return False

    def connection_info(self):
        store = ConfigStore()
        return store.connection_info(self.name)

    @property
    def _connection(self):
        """Returns an open API connection.

        All access to the API server goes through this method with the intent
        that we may in the future cache an open connection for a length of
        time.

        """
        return open_environment(self.name)

    @property
    def client(self):
        "Client API facade for the API connection for this environment."
        api = self._connection
        return api.get_facade("Client")

    def status(self):
        return self.client.FullStatus()

    def config(self, *keys):
        "Return the environment config."
        result = self.client.EnvironmentGet()
        cfg = result['Config']
        if len(keys) == 0:
            return cfg
        if len(keys) == 1:
            return cfg[keys[0]]
        return dict([(key, cfg[key]) for key in keys])

    def service(self, name):
        return Service(self, name)



class Service(object):
    def __init__(self, environment, name):
        self.environment = environment
        self.name = name

    def config(self, *keys):
        "Return the environment config."
        client = self.environment.client
        result = client.ServiceGet({'ServiceName': self.name})
        cfg = result['Config']
        if len(keys) == 0:
            return cfg
        if len(keys) == 1:
            return cfg[keys[0]]
        return dict([(key, cfg[key]) for key in keys])
