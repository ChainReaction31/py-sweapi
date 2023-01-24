import pytest

from pyconnectedservices.system import SystemBuilder


@pytest.fixture
def t_sys_name():
    return 'Test System'


@pytest.fixture
def t_sys_uid():
    return 'urn:test:testsystem'


@pytest.fixture
def t_sys_definition():
    return 'www.test.org/test/testsystem'


@pytest.fixture
def t_sys_description():
    return 'A Test System'


@pytest.fixture
def t_sys_node_url():
    return 'http://192.168.56.101'
    # return 'http://127.0.0.1'


@pytest.fixture
def t_sys_node_port():
    return 8181
    # return 8282


@pytest.fixture
def t_sys_node_endpoint():
    return 'sensorhub'


@pytest.fixture
def t_sys_system(t_sys_name, t_sys_uid, t_sys_definition, t_sys_description, t_sys_node_url, t_sys_node_port,
                 t_sys_node_endpoint):
    sys_builder = SystemBuilder()
    system = sys_builder \
        .with_name(t_sys_name) \
        .with_uid(t_sys_uid) \
        .with_definition(t_sys_definition) \
        .with_description(t_sys_description) \
        .with_node(t_sys_node_url, t_sys_node_port, t_sys_node_endpoint) \
        .build()

    return system
