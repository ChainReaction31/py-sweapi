import json
from dataclasses import dataclass
from enum import Enum

from oshdatacore.component_implementations import DataRecordComponent

from pyswapi.comm.comm_mqtt import MQTTComm
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
    __csi_id: str = None
    __mqtt_client: MQTTComm = None

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

    def set_client(self, client: MQTTComm):
        """
        Sets the MQTT client
        :param client:
        """
        self.__mqtt_client = client

    def publish_control_stream_interface(self, system: System):
        """
        Publishes the control stream to topic /api/systems/{system_id}/controls using the MQTT client set by the
        set_client method
        :param system: The system to which the control stream will be published
        """
        if self.__mqtt_client is None:
            raise Exception('MQTT client not set')

        topic = f'{system.get_node_api_url()}/api/systems/{system.get_sys_id()}/controls'
        self.__mqtt_client.publish(topic, self.__get_control_stream_dict())
        self.__mqtt_client.subscribe(f'/api/controls/{self.__csi_id}/commands')

    def publish_command(self, system: System, command: Command):
        """
        Publishes a command to the control interface. OSH rejects commands if there is no subscriber to the command
        interface's topic
        :param system: The system to which the command will be published
        :param client:
        :param command: The command to be published
        """
        topic = f'/api/systems/{system.get_sys_id()}/controls/{self.name}/commands'
        self.__mqtt_client.publish(topic, command.__dict__)

    def subscribe_to_commands(self, callback=None):
        """
        Subscribes to the command interface's topic
        :param callback: handler for dealing with the received commands, by default the handler just accepts
        the command with a status of ACCEPTED and does no further processing
        """
        self.__mqtt_client.subscribe(f'/api/controls/{self.__csi_id}/commands')
        if callback is not None:
            self.__mqtt_client.on_message = callback
        else:
            def on_msg(client, userdata, msg):
                json_msg = json.loads(msg.payload.decode("utf-8"))
                resp = {
                    'id': json_msg.id,
                    'commad@id': json_msg.commandId,
                    'status': CommandStatusCode.ACCEPTED.value
                }
                self.__mqtt_client.publish(f'/api/controls/{self.__csi_id}/commands/status', resp)

            self.__mqtt_client.on_message = on_msg

    
