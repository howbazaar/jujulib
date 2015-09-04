import os
import yaml


SAMPLE_CONFIG = {
    'user': 'tester',
    'password': 'sekrit',
    'environ-uuid': 'some-uuid',
    'server-uuid': 'server-uuid',
    'state-servers': ['localhost:12345'],
    'ca-cert': 'test-cert',
}


def write_jenv(juju_home, env_name, content=None):
    if content is None:
        content = SAMPLE_CONFIG
    env_dir = os.path.join(juju_home, 'environments')
    if not os.path.exists(env_dir):
        os.mkdir(env_dir)
    jenv = os.path.join(env_dir, '{}.jenv'.format(env_name))
    with open(jenv, 'w') as f:
        yaml.dump(content, f, default_flow_style=False)


def write_cache_file(juju_home, env_name, content=None):
    if content is None:
        content = SAMPLE_CONFIG
    env_dir = os.path.join(juju_home, 'environments')
    if not os.path.exists(env_dir):
        os.mkdir(env_dir)
    filename = os.path.join(env_dir, 'cache.yaml')
    cache_content = {
        'environment': {
            env_name: {'env-uuid': content['environ-uuid'],
                       'server-uuid': content['server-uuid'],
                       'user': content['user']}},
        'server-data': {
            content['server-uuid']: {
                'api-endpoints': content['state-servers'],
                'ca-cert': content['ca-cert'],
                'identities': {content['user']: content['password']}}},
        # Explicitly don't care about 'server-user' here.
        }
    with open(filename, 'w') as f:
        yaml.dump(cache_content, f, default_flow_style=False)
