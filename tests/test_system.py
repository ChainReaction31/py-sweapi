import pytest

from pyconnectedservices.constants import SystemTypes
from pyconnectedservices.system import SystemBuilder


def test_system_builder_empty():
    sys_builder = SystemBuilder()
    system = sys_builder.build()

    assert system.name is None
    assert system.uid is None
    assert system.definition is None
    assert system.description is None
    assert system.node_url is None
    assert system.node_port is None
    assert system.node_endpoint is None


def test_sys_builder_with_name(t_sys_name):
    sys_builder = SystemBuilder()
    system = sys_builder.with_name(t_sys_name).build()

    assert system.name == t_sys_name
    assert system.uid is None
    assert system.definition is None
    assert system.description is None
    assert system.node_url is None
    assert system.node_port is None
    assert system.node_endpoint is None


def test_sys_builder_with_uid(t_sys_uid):
    sys_builder = SystemBuilder()
    system = sys_builder.with_uid(t_sys_uid).build()

    assert system.name is None
    assert system.uid == t_sys_uid
    assert system.definition is None
    assert system.description is None
    assert system.node_url is None
    assert system.node_port is None
    assert system.node_endpoint is None


def test_sys_builder_with_definition(t_sys_definition):
    sys_builder = SystemBuilder()
    system = sys_builder.with_definition(t_sys_definition).build()

    assert system.name is None
    assert system.uid is None
    assert system.definition == t_sys_definition
    assert system.description is None
    assert system.node_url is None
    assert system.node_port is None
    assert system.node_endpoint is None


def test_sys_builder_with_description(t_sys_description):
    sys_builder = SystemBuilder()
    system = sys_builder.with_description(t_sys_description).build()

    assert system.name is None
    assert system.uid is None
    assert system.definition is None
    assert system.description == t_sys_description
    assert system.node_url is None
    assert system.node_port is None
    assert system.node_endpoint is None


def test_sys_builder_with_node(t_sys_node_url, t_sys_node_port, t_sys_node_endpoint):
    sys_builder = SystemBuilder()
    system = sys_builder.with_node(t_sys_node_url, t_sys_node_port, t_sys_node_endpoint).build()

    assert system.name is None
    assert system.uid is None
    assert system.definition is None
    assert system.description is None
    assert system.node_url == t_sys_node_url
    assert system.node_port == t_sys_node_port
    assert system.node_endpoint == t_sys_node_endpoint


def test_sys_builder_all(t_sys_name, t_sys_uid, t_sys_definition, t_sys_description, t_sys_node_url, t_sys_node_port,
                         t_sys_node_endpoint):
    sys_builder = SystemBuilder()
    system = sys_builder \
        .with_name(t_sys_name) \
        .with_uid(t_sys_uid) \
        .with_definition(t_sys_definition) \
        .with_description(t_sys_description) \
        .with_node(t_sys_node_url, t_sys_node_port, t_sys_node_endpoint) \
        .build()

    assert system.name == t_sys_name
    assert system.uid == t_sys_uid
    assert system.definition == t_sys_definition
    assert system.description == t_sys_description
    assert system.node_url == t_sys_node_url
    assert system.node_port == t_sys_node_port
    assert system.node_endpoint == t_sys_node_endpoint


def test_build_system_dict(t_sys_system):
    t_sys_system.build_system_dict()
    system_dict = t_sys_system.system_dict

    assert system_dict['type'] == SystemTypes.FEATURE.value
    assert system_dict['properties'] == dict([
        ('name', t_sys_system.name),
        ('uid', t_sys_system.uid),
        ('definition', t_sys_system.definition),
        ('description', t_sys_system.description),
        ('type', t_sys_system.definition),
    ])


def test_generate_json(t_sys_system):
    json = t_sys_system.generate_json()
    print(json)
    assert json == '{"type": "Feature", "properties": {"name": "Test System", "uid": "urn:test:testsystem", ' \
                   '"definition": "www.test.org/test/testsystem", "description": "A Test System", ' \
                   '"type": "www.test.org/test/testsystem"}}'
