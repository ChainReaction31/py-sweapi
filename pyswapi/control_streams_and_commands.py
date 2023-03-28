from dataclasses import dataclass
from datetime import datetime
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
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    SCHEDULED = 'SCHEDULED'
    UPDATED = 'UPDATED'
    CANCELLED = 'CANCELLED'
    EXECUTING = 'EXECUTING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


# @dataclass(kw_only=True)
# class CommandStatus:
#     command_id: str
#     report_time: datetime
#     status: CommandStatusCode.value


@dataclass(kw_only=True)
class ControlInterface:
    name: str
    input_name: str
    __command_schema: DataRecordComponent = None

    def add_schema(self, component: DataRecordComponent):
        self.__command_schema = component

    def insert_control_stream(self, system: System):
        post_system_controls(system.get_node_api_url(), system.get_sys_id(), self.__get_control_stream_dict())

    def __get_control_stream_dict(self):
        return {
            'name': self.name,
            'inputName': self.input_name,
            'schema': {
                'commandSchema': self.__command_schema.datastructure_to_dict()
            }
        }

    # def set):