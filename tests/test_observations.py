from datetime import datetime


def test_insert_time_value(t_ds_datastream, t_sys_system, t_root_component, t_comp_time):
    ds = t_ds_datastream
    the_time = datetime.now()
    ds.add_value_by_uuid(t_comp_time.get_uuid(), the_time)
    assert t_comp_time.value == the_time


def test_insert_bool_value(t_ds_datastream, t_sys_system, t_root_component, t_comp_bool):
    ds = t_ds_datastream
    ds.add_value_by_uuid(t_comp_bool.get_uuid(), True)
    assert t_comp_bool.value == True


def test_insert_text_value(t_ds_datastream, t_sys_system, t_root_component, t_comp_text):
    ds = t_ds_datastream
    ds.add_value_by_uuid(t_comp_text.get_uuid(), 'Test Text')
    assert t_comp_text.value == 'Test Text'


def test_insert_count_value(t_ds_datastream, t_sys_system, t_root_component, t_comp_count):
    ds = t_ds_datastream
    ds.add_value_by_uuid(t_comp_count.get_uuid(), 1)
    assert t_comp_count.value == 1


def test_insert_category_value(t_ds_datastream, t_sys_system, t_root_component, t_comp_category):
    ds = t_ds_datastream
    ds.add_value_by_uuid(t_comp_category.get_uuid(), 'Test Category')
    assert t_comp_category.value == 'Test Category'


def test_insert_quantity_value(t_ds_datastream, t_sys_system, t_root_component, t_comp_quantity):
    ds = t_ds_datastream
    ds.add_value_by_uuid(t_comp_quantity.get_uuid(), 1.0)
    assert t_comp_quantity.value == 1.0


def test_insert_multiple_values(t_ds_datastream, t_sys_system, t_root_component, t_comp_time, t_comp_bool, t_comp_text,
                                t_comp_count, t_comp_category, t_comp_quantity):
    ds = t_ds_datastream
    the_time = datetime.now()
    ds.add_value_by_uuid(t_comp_time.get_uuid(), the_time)
    ds.add_value_by_uuid(t_comp_bool.get_uuid(), True)
    ds.add_value_by_uuid(t_comp_text.get_uuid(), 'Test Text')
    ds.add_value_by_uuid(t_comp_count.get_uuid(), 1)
    ds.add_value_by_uuid(t_comp_category.get_uuid(), 'Test Category')
    ds.add_value_by_uuid(t_comp_quantity.get_uuid(), 1.0)
    assert t_comp_time.value == the_time
    assert t_comp_bool.value is True
    assert t_comp_text.value == 'Test Text'
    assert t_comp_count.value == 1
    assert t_comp_category.value == 'Test Category'
    assert t_comp_quantity.value == 1.0


def test_create_observation(t_ds_datastream, t_sys_system, t_root_component, t_comp_time, t_comp_bool, t_comp_text,
                            t_comp_count, t_comp_category, t_comp_quantity):
    ds = t_ds_datastream
    the_time = datetime.now()
    ds.add_value_by_uuid(t_comp_time.get_uuid(), the_time)
    ds.add_value_by_uuid(t_comp_bool.get_uuid(), True)
    ds.add_value_by_uuid(t_comp_text.get_uuid(), 'Test Text')
    ds.add_value_by_uuid(t_comp_count.get_uuid(), 1)
    ds.add_value_by_uuid(t_comp_category.get_uuid(), 'Test Category')
    ds.add_value_by_uuid(t_comp_quantity.get_uuid(), 1.0)
    ds.create_observation_from_current()
    assert len(ds.get_obs_list()) == 1


def test_insert_earliest_observation(t_ds_datastream, t_sys_system, t_root_component, t_comp_time, t_comp_bool,
                                     t_comp_text, t_comp_count, t_comp_category, t_comp_quantity):
    ds = t_ds_datastream
    the_time = datetime.now().timestamp() * 1000
    ds.add_value_by_uuid(t_comp_time.get_uuid(), the_time)
    ds.add_value_by_uuid(t_comp_bool.get_uuid(), True)
    ds.add_value_by_uuid(t_comp_text.get_uuid(), 'Test Text')
    ds.add_value_by_uuid(t_comp_count.get_uuid(), 1)
    ds.add_value_by_uuid(t_comp_category.get_uuid(), 'Test Category')
    ds.add_value_by_uuid(t_comp_quantity.get_uuid(), 1.0)

    ds.create_observation_from_current()
    ds.parent_system.insert_system()
    ds.insert_datastream()
    ds.send_earliest_observation()


def test_insert_via_dict_and_send(t_ds_datastream, t_sys_system, t_root_component, t_comp_time, t_comp_bool,
                                  t_comp_text, t_comp_count, t_comp_category, t_comp_quantity):
    ds = t_ds_datastream
    the_time = datetime.now().timestamp() * 1000
    ds.parent_system.insert_system()
    ds.insert_datastream()

    values = {
        t_comp_time.get_uuid(): the_time,
        t_comp_bool.get_uuid(): True,
        t_comp_text.get_uuid(): 'Test Text',
        t_comp_count.get_uuid(): 1,
        t_comp_category.get_uuid(): 'Test Category',
        t_comp_quantity.get_uuid(): 1.0
    }
    ds.insert_obs_values_and_send(values)
