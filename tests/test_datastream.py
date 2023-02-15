from pyconnectedservices import datastreams_and_observations as ds
from pyconnectedservices import system


def test_datastream(t_ds_datastream, t_sys_system, t_root_component):
    ds = t_ds_datastream
    print(f'Datastream: {ds}')
    assert ds.name == 'Test Datastream'
    assert ds.description == 'A Test Datastream'
    assert ds.encoding == t_ds_datastream.encoding
    assert ds.parent_system == t_sys_system


def test_insert_datastream(t_ds_datastream, t_sys_system, t_root_component):
    sys_id = t_sys_system.insert_system()
    if sys_id is not None:
        ds = t_ds_datastream
        ds.parent_system = t_sys_system
        expected_id = ds.insert_datastream()
        assert ds.get_ds_id() == expected_id
    else:
        assert False


def test_build_ds_from_node():
    test_systems = system.build_systems_from_node('http://192.168.56.101', '8181', '/sensorhub')
    par_sys = test_systems[0]
    ds_list = ds.build_ds_from_node('http://192.168.56.101', 8181, 'sensorhub', par_sys)
