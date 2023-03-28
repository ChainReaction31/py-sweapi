from oshdatacore.component_implementations import DataRecordComponent
from oshdatacore.encoding import TextEncoding

from pyswapi.constants import ObservationFormat
from pyswapi.control_streams_and_commands import ControlInterface
from pyswapi.datastreams_and_observations import Datastream
from pyswapi.system import SystemBuilder


def test_insert_control_stream(t_comp_time, t_comp_quantity):
    builder = SystemBuilder()
    system = builder.with_name('Test System Control') \
        .with_uid('test_system_control') \
        .with_definition('http://test/org/test_system_control') \
        .with_description('A Test System Control') \
        .with_node('http://digitalbridge.tech', 8181, 'sensorhub') \
        .build()

    datastream = Datastream(name='Controlled Datastream', description='A Controllable Datastream',
                            output_name='controlled-datastream', encoding=TextEncoding(),
                            obs_format=ObservationFormat.JSON.value, parent_system=system)

    root_component = DataRecordComponent(name='root', label='Root', description='Root Component',
                                         definition='www.test.org/test/root')
    root_component.add_field(t_comp_time)
    root_component.add_field(t_comp_quantity)
    datastream.add_root_component(root_component)

    system.insert_system()
    datastream.insert_datastream()

    control_stream = ControlInterface(name='Controlled Datastream', input_name='controlled-datastream')
    control_stream.add_schema(root_component)
    control_stream.insert_control_stream(system)


