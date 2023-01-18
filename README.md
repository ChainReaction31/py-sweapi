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
ds_builder = DatastreamBuilder()
my_datastream = ds_builder \
    .with_name("My Datastream") \
    .with_uid("urn:my_project:my_datastream_uid") \
    .with_description("My datastream description") \
    # Create a text encoding either inline or beforehand
    .with_encoding(txt_encoding) \
    # Choose from ObservationFormat enum in constants.py
    .with_observation_format(ObservationFormat.JSON) \
    .with_parent_system(system) \
    .build()
```

3. Add Root Component to Datastream
```python
root_component = DataRecordComponent("my_record", "My Record", "http://my_record_definition", "My record description")
my_datastream.set_root_component(root_component)
```

4. Add Components to Root Component
```python
# Create a component

```