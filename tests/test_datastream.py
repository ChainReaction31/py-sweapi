def test_datastream(t_ds_datastream, t_sys_system, t_root_component):
    ds = t_ds_datastream
    print(ds)
    assert ds.name == 'Test Datastream'
    assert ds.description == 'A Test Datastream'
    assert ds.encoding == 'application/json'
    assert ds.parent_system == t_sys_system
    assert ds.root_component == t_root_component


def test_insert_datastream(t_ds_datastream, t_sys_system, t_root_component):
    sys_id = t_sys_system.insert_system()
    if sys_id is not None:
        ds = t_ds_datastream
        ds.parent_system = t_sys_system
        expected_id = ds.insert_datastream()
        assert ds.get_ds_id() == expected_id
    else:
        assert False
