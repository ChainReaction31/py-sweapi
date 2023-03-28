from dataclasses import dataclass
from enum import Enum

from oshdatacore.component_implementations import DataRecordComponent

from pyswapi.endpoints.system_ep import post_system_controls
from pyswapi.system import System


@dataclass(kw_only=True)
class ControlledProperty:
    definition: str
    label: str


@dataclass(kw_only=True)
class ControlStream:
    name: str
    issue_time: tuple
    execution_time: tuple
    controlled_properties: list[ControlledProperty]
    formats: list


@dataclass(kw_only=True)
class Command:
    control_stream_id: str
    user_id: str
    issue_time: tuple
    execution_time: tuple
    current_status: str
    params: dict


class CommandStatusCode(Enum):
    """
    Defines accepted command status codes
    """
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    SCHEDULED = 'SCHEDULED'
    UPDATED = 'UPDATED'
    CANCELLED = 'CANCELLED'
    EXECUTING = 'EXECUTING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


@dataclass(kw_only=True)
class ControlInterface:
    """
    Control interfaces define the commands that can be issued to a system.
    :param name: The machine name of the control interface
    :param input_name: The human-readable name of the control interface
    :param __command_schema: The schema of the commands that can be issued to the system, often a reflection of the
    system's data model
    """
    name: str
    input_name: str
    __command_schema: DataRecordComponent = None

    def add_schema(self, component: DataRecordComponent):
        """
        Adds a schema to the control interface
        :param component: The DataRecordComponent that defines the names and types of the commands that can be issued to
        the system
        """
        self.__command_schema = component

    def insert_control_stream(self, system: System):
        """
        Inserts the control stream into the system
        :param system: The system to which the control stream will be added
        """
        post_system_controls(system.get_node_api_url(), system.get_sys_id(), self.__get_control_stream_dict())

    def __get_control_stream_dict(self):
        return {
            'name': self.name,
            'inputName': self.input_name,
            'schema': {
                'commandSchema': self.__command_schema.datastructure_to_dict()
            }
        }
