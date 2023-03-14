import time
from datetime import datetime

from pyswapi import datastreams_and_observations as ds
from pyswapi import system
import pyswapi.comm.comm_mqtt as mqtt
import paho.mqtt.client as mqtt_ph



def test_datastream(t_ds_datastream, t_sys_system, t_root_component):
    datastream = t_ds_datastream
    print(f'Datastream: {datastream}')
    assert datastream.name == 'Test Datastream'
    assert datastream.description == 'A Test Datastream'
    assert datastream.encoding == t_ds_datastream.encoding
    assert datastream.parent_system == t_sys_system


def test_insert_datastream(t_ds_datastream, t_sys_system, t_root_component):
    sys_id = t_sys_system.insert_system()
    if sys_id is not None:
        datastream = t_ds_datastream
        datastream.parent_system = t_sys_system
        expected_id = datastream.insert_datastream()
        assert datastream.get_ds_id() == expected_id
    else:
        assert False


def test_build_ds_from_node():
    test_systems = system.build_systems_from_node('http://192.168.56.101', '8181', '/sensorhub')
    par_sys = test_systems[0]
    ds_list = ds.build_ds_from_node('http://192.168.56.101', 8181, 'sensorhub', par_sys)


def test_publish_single(t_ds_datastream, t_sys_system, t_root_component, t_comp_time, t_comp_bool,
                        t_comp_text, t_comp_count, t_comp_category, t_comp_quantity, t_sys_node_url, t_sys_node_port):
    datastream = t_ds_datastream
    the_time = datetime.now().timestamp() * 1000
    datastream.parent_system.insert_system()
    datastream.insert_datastream()

    values = {
        t_comp_time.name: the_time,
        t_comp_bool.name: True,
        t_comp_text.name: 'Test Text',
        t_comp_count.name: 1,
        t_comp_category.name: 'Test Category',
        t_comp_quantity.name: 1.0
    }
    datastream.set_values(values)
    datastream.create_observation_from_current()
    datastream.publish_earliest_observation(node_url=f'digitalbridge.tech/sensorhub', port=t_sys_node_port)


def test_publish_client(t_ds_datastream, t_sys_system, t_root_component, t_comp_time, t_comp_bool,
                        t_comp_text, t_comp_count, t_comp_category, t_comp_quantity, t_sys_node_url, t_sys_node_port):
    datastream = t_ds_datastream
    the_time = datetime.now().timestamp() * 1000
    datastream.parent_system.insert_system()
    datastream.insert_datastream()

    values = {
        t_comp_time.name: the_time,
        t_comp_bool.name: True,
        t_comp_text.name: 'Test Text',
        t_comp_count.name: 1,
        t_comp_category.name: 'Test Category',
        t_comp_quantity.name: 1.0
    }
    datastream.set_values(values)
    datastream.create_observation_from_current()
    client = mqtt.MQTTComm('digitalbridge.tech', 1883)
    client.connect()
    # time.sleep(3)
    client.start()
    datastream.publish_earliest_observation_client(client)
