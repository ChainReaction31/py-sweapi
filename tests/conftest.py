import pytest
import json
import pathlib
from oshdatacore.component_implementations import BooleanComponent, TextComponent, CountComponent, CategoryComponent, \
    QuantityComponent, TimeComponent, DataRecordComponent, VectorComponent, DataArrayComponent
from oshdatacore.encoding import TextEncoding

from pyswapi.constants import ObservationFormat
from pyswapi.control_streams_and_commands import ControlInterface
from pyswapi.datastreams_and_observations import Datastream
from pyswapi.system import SystemBuilder


@pytest.fixture
def secret_json(request):
    file = pathlib.Path(request.node.fspath)
    secrets = file.with_name('secrets.json')
    with secrets.open() as cf:
        return json.load(cf)


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
def t_sys_node_url(secret_json):
    return secret_json['url']


@pytest.fixture
def t_sys_node_port(secret_json):
    return secret_json['port']


@pytest.fixture
def t_sys_node_endpoint(secret_json):
    return secret_json['endpoint']


@pytest.fixture
def t_full_url(t_sys_node_url, t_sys_node_port, t_sys_node_endpoint):
    return f'{t_sys_node_url}:{t_sys_node_port}/{t_sys_node_endpoint}/api'


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


# Datastream.py test fixtures
@pytest.fixture
def t_ds_name():
    return 'Test Datastream'


@pytest.fixture
def t_ds_description():
    return 'A Test Datastream'


@pytest.fixture
def t_ds_encoding():
    encoding = TextEncoding()
    return encoding


@pytest.fixture
def t_ds_observation_format():
    return ObservationFormat.JSON.value


@pytest.fixture
def t_ds_result_parent(t_sys_system):
    return t_sys_system


@pytest.fixture
def t_ds_datastream(t_ds_name, t_ds_description, t_ds_encoding, t_ds_observation_format, t_ds_result_parent,
                    t_root_component):
    datastream = Datastream(name=t_ds_name, description=t_ds_description, encoding=t_ds_encoding,
                            obs_format=t_ds_observation_format, parent_system=t_ds_result_parent,
                            root_component=t_root_component, output_name='test-output')

    return datastream


@pytest.fixture
def t_root_component(t_comp_time, t_comp_bool, t_comp_text, t_comp_count, t_comp_category, t_comp_quantity):
    comp = DataRecordComponent(name='root', label='Root', definition='www.test.org/test/root',
                               description='Root Component')
    comp.add_field(t_comp_time)
    comp.add_field(t_comp_bool)
    comp.add_field(t_comp_text)
    comp.add_field(t_comp_count)
    comp.add_field(t_comp_category)
    comp.add_field(t_comp_quantity)
    return comp


# Component Fixtures
@pytest.fixture
def t_comp_bool():
    comp = BooleanComponent(name='test-bool', label='Test Bool', definition='www.test.org/test/bool')
    return comp


@pytest.fixture
def t_comp_text():
    comp = TextComponent(name='test-text', label='Test Text', definition='www.test.org/test/text')
    return comp


@pytest.fixture
def t_comp_count():
    comp = CountComponent(name='test-count', label='Test Count', definition='www.test.org/test/count')
    return comp


@pytest.fixture
def t_comp_category():
    comp = CategoryComponent(name='test-category', label='Test Category', definition='www.test.org/test/category')
    return comp


@pytest.fixture
def t_comp_quantity():
    comp = QuantityComponent(name='test-quantity', label='Test Quantity', definition='www.test.org/test/quantity')
    return comp


@pytest.fixture
def t_comp_time():
    comp = TimeComponent(name='test-time', label='Test Time', description='Test Description')
    return comp


@pytest.fixture
def t_comp_vector():
    comp = VectorComponent(name='test-vector', label='Test Vector', definition='www.test.org/test/vector',
                           local_frame='#SENSOR_FRAME', reference_frame='http://www.opengis.net/def/crs/EPSG/0/9705')
    lat = QuantityComponent(name='lat', label='Latitude', definition='www.test.org/test/lat')
    lon = QuantityComponent(name='lon', label='Longitude', definition='www.test.org/test/lon')
    alt = QuantityComponent(name='alt', label='Altitude', definition='www.test.org/test/alt')
    comp.add_coord(lat)
    comp.add_coord(lon)
    comp.add_coord(alt)
    return comp


@pytest.fixture
def t_comp_data_array():
    count = CountComponent(name='count', label='Count', definition='www.test.org/test/count')
    count.value = 3
    e_type = QuantityComponent(name='e-type', label='Element Type', definition='www.test.org/test/e-type')
    comp = DataArrayComponent(name='test-data-array', label='Test Data Array',
                              definition='www.test.org/test/data-array',
                              element_count=count, element_type=e_type)
    return comp


@pytest.fixture
def t_command_interface():
    ci = ControlInterface(name='test-command-interface', input_name='Command Test')
    return ci
