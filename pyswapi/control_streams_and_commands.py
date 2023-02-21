from dataclasses import dataclass
from datetime import datetime
from enum import Enum


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


@dataclass(kw_only=True)
class CommandStatus:
    command_id: str
    report_time: datetime
    status: CommandStatusCode.value
