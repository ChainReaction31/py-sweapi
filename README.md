# osh_connected_services_api_for_python
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
sys_builder.with_uid("my_system_uid")
sys_builder.with_definition("http://my_system_definition")
sys_builder.with_description("My system description")
sys_builder.with_node("http://my_node_url", 8080, "api_endpoint")

system = sys_builder.build()
```

2. Add Outputs to System
```python

```