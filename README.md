# OSH Connected Systems API For Python
Serves as a bridge between datasources created in Python and an OSH Node with the SWEAPI enabled

This package depends on the osh_data_core package as well 

## Using the package

---

### Required information
To use this package, you must know a few things about the hub that you are intending connect to:
1. The hub's IP address
2. The hub's port
3. The hub's API endpoint

---

## Creating a System
1. Create a system object   
```python 
# A system requires a name, a UID, a definition, and a description.
sys_builder = SystemBuilder()
sys_builder.with_name("My System")
sys_builder.with_uid("urn:my_project:my_system_uid")
sys_builder.with_definition("http://my_system_definition")
sys_builder.with_description("My system description")
sys_builder.with_node("http://my_node_url", 8282, "api_endpoint")

system = sys_builder.build()
```

2. Add Datastream to System
```python
datastream = Datastream(
    name=t_ds_name, 
    description=t_ds_description, 
    encoding=t_ds_encoding,                        
    obs_format=t_ds_observation_format, 
    parent_system=t_ds_result_parent,
    root_component=t_root_component, 
    output_name='test-output')
```

3. Add Root Component to Datastream
```python
root_component =DataRecordComponent(
    name='root', 
    label='Root', 
    definition='www.test.org/test/root',
    description='Root Component')
datastream.set_root_component(root_component)
```

4. Add Components to Root Component
```python
# Create a component
comp = BooleanComponent(name='test-bool', label='Test Bool', definition='www.test.org/test/bool')
root_component.add_component(comp)
```