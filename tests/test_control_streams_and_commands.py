import json
import pathlib

from oshdatacore.component_implementations import DataRecordComponent, BooleanComponent, TimeComponent
from oshdatacore.encoding import TextEncoding

from conftest import t_sys_node_url, t_sys_node_port, t_sys_node_endpoint
from pyswapi.comm.comm_mqtt import MQTTComm
from pyswapi.constants import ObservationFormat
from pyswapi.control_streams_and_commands import ControlInterface
from pyswapi.datastreams_and_observations import Datastream
from pyswapi.system import SystemBuilder

with open('secrets.json') as secrets:
    secret_json = json.load(secrets)

test_system = SystemBuilder() \
    .with_name('Test System Control') \
    .with_uid('system_control_test') \
    .with_definition('http://test/org/test_system_control') \
    .with_description('System Control Test') \
    .with_node(secret_json['url'], secret_json['port'], secret_json['endpoint']) \
    .build()

test_system.insert_system()

# Use this blank ds to test the control stream
test_ds = Datastream(name='Controlled Datastream', description='A Controllable Datastream',
                     output_name='controlled-datastream', encoding=TextEncoding(),
                     obs_format=ObservationFormat.JSON.value, parent_system=test_system)

simple_root = DataRecordComponent(name='root', label='Root', description='Root Component',
                                  definition='www.test.org/test/root')
a_timestamp = TimeComponent(name='a_timestamp', label='A Timestamp', description='A Timestamp Component',
                            definition='www.test.org/test/a_timestamp')
a_bool = BooleanComponent(name='a_bool', label='A Boolean', description='A Boolean Component',
                          definition='www.test.org/test/a_bool')
simple_root.add_field(a_timestamp)
simple_root.add_field(a_bool)


# Resuable
ci_id = None

def test_add_schema(t_command_interface):
    ci = t_command_interface
    ci.add_schema(simple_root)

    assert ci._ControlInterface__command_schema == simple_root


def test_set_parent_system(t_command_interface):
    ci = t_command_interface
    ci.set_parent_system(test_system)
    assert ci._ControlInterface__parent_system == test_system


def test_insert_control_stream(t_command_interface):
    ci = t_command_interface
    ci.add_schema(simple_root)
    ci.set_parent_system(test_system)
    ci.insert_control_stream()
    assert ci._ControlInterface__csi_id is not None
    ci_id = ci._ControlInterface__csi_id


some_client = MQTTComm(url=secret_json['url'])


def test_set_client(t_command_interface):
    ci = t_command_interface
    ci.set_client(some_client)
    assert ci._ControlInterface__mqtt_client == some_client


def test_publish_control_stream_interface():
    """ TODO: This test cannot pass until an MQTT bug is fixed server-side"""
    assert False


def test_publish_command():
    """ TODO: This test cannot pass until an MQTT bug is fixed server-side"""
    assert False


def test_subscribe_to_commands():
    """ TODO: This test cannot pass until an MQTT bug is fixed server-side"""
    assert False


def test_insert_command():
    assert False


def test_get_commands():
    assert False


def test_retrieve_schema():
    assert False


def test_build_command_interfaces_from_system(t_sys_node_url, t_sys_node_port, t_sys_node_endpoint,
                                              t_command_interface):
    test_system.set_sys_id('j37bui6no3om2')
    new_ci = ControlInterface.build_command_interfaces_from_system(test_system)[0]

    assert new_ci._ControlInterface__parent_system == test_system
    assert new_ci._ControlInterface__command_schema is not None
