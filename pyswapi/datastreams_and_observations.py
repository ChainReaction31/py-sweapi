import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

import requests
from oshdatacore.component_implementations import DataRecordComponent, TimeComponent, QuantityComponent, CountComponent, \
    CategoryComponent, TextComponent, BooleanComponent
from oshdatacore.encoding import AbstractEncoding
from paho.mqtt import publish

from pyswapi.constants import APITerms
from pyswapi.endpoints import datastreams
from pyswapi.system import System


def build_ds_from_node(node_url, node_port, node_endpoint, parent_system: System):
    """
    Builds a list of Datastreams from a SensorHub node. May lose some resolution compared to creating a datastream
    directly, but the API does not currently provide things like definition or encoding in some cases.

    :param node_url: base URL of the node
    :param node_port: port the node is running on (often 8181 or 8282)
    :param node_endpoint: endpoint of the node, typically 'sensorhub' or APITerms.SENSORHUB.type
    :param parent_system: the System object that this datastream belongs to
    :return: a list of datastream objects
    """
    response = datastreams.get_datastream_from_system(node_api_endpoint=f'{node_url}:{node_port}/{node_endpoint}/api',
                                                      system_id=parent_system.get_sys_id())
    ds_list = []
    for ds in response.json()['items']:
        print(ds)
        new_ds = Datastream(
            name=ds['name'],
            output_name=ds['outputName'],
            encoding=AbstractEncoding(),
            parent_system=parent_system,
            obs_format=None
        )

        schema_resp = datastreams.get_datastream_schema(node_api_endpoint=f'{node_url}:{node_port}/{node_endpoint}/api',
                                                        datastream_id=ds['id'])
        r_json = schema_resp.json()
        ds_root = DataRecordComponent(description=r_json['resultSchema']['description'],
                                      label=r_json['resultSchema']['label'],
                                      name=r_json['resultSchema']['label'],
                                      definition='')

        for field in schema_resp.json()['resultSchema']['fields']:
            ds_root.add_field(__ds_builder(field))

        ds_list.append(new_ds)

    return ds_list


def __ds_builder(field_dict):
    match field_dict['type']:
        case 'Time':
            return TimeComponent(name=field_dict['name'], label=field_dict['label'],
                                 description='', definition='')
        case 'Boolean':
            return BooleanComponent(name=field_dict['name'], label=field_dict['label'],
                                    description='', definition='')
        case 'Text':
            return TextComponent(name=field_dict['name'], label=field_dict['label'],
                                 description='', definition='')
        case 'Category':
            return CategoryComponent(name=field_dict['name'], label=field_dict['label'],
                                     description='', definition='')
        case 'Count':
            return CountComponent(name=field_dict['name'], label=field_dict['label'],
                                  description='', definition='')
        case 'Quantity':
            return QuantityComponent(name=field_dict['name'], label=field_dict['label'],
                                     description='', definition='',
                                     uom=field_dict['uom']['href'])
        case 'DataRecord':
            return DataRecordComponent(name=field_dict['name'], label=field_dict['label'],
                                       description='', definition='',
                                       fields=list(map(__ds_builder, field_dict['fields'])))


class Datastream:

    def __init__(self, name, description, output_name, encoding, obs_format, parent_system,
                 root_component: DataRecordComponent = None):
        """
        Datastreams define the structure of data sent to an OSH Node. They provide a means of defining what and how
        data must be packaged.

        :param name: Human-readable name for the datastream
        :param description: A brief description of the datastream
        :param output_name: The machine name of the datastream, often lowercase and hyphenated (e.g. 'your-output')
        :param encoding: One of the supported encodings
        :param root_component: The DataRecordComponent that is the root of the datastream
        :param obs_format: The observation format of the datastream (e.g. 'application/om+json')
        :param parent_system: The parent system of the datastream
        """
        self.name = name
        self.output_name = output_name
        self.description = description
        self.encoding = encoding
        self.obs_format = obs_format
        self.parent_system = parent_system
        self.root_component = root_component
        self.schema = None
        self.__ds_id: str = None
        self.__topic = f'{APITerms.API.value}/{APITerms.DATASTREAMS.value}/{self.__ds_id}/{APITerms.OBSERVATIONS.value}'
        self.__field_map = {}
        self.__observations: list = []

    def create_datastream_schema(self):
        """
        create the schema for the datastream or return the existing schema

        :return: the datastream's schema
        """
        if self.schema is None:
            schema = dict([
                ('obsFormat', self.obs_format),
                ('resultSchema', self.root_component.datastructure_to_dict()),
                ('resultEncoding', vars(self.encoding))
            ])
            self.schema = schema
            return schema
        else:
            return self.schema

    # TODO: Test this method thoroughly
    def insert_datastream(self):
        """
        Insert the datastream into the parent system. Throws an error if the parent system is not set.
        """

        if self.parent_system is not None:
            datastream_dict = dict([
                ('outputName', self.output_name),
                ('name', self.name),
                ('description', self.description),
                ('schema', self.create_datastream_schema()),
            ])

            r = datastreams.post_datastream(self.parent_system.get_node_api_url(), self.parent_system.get_sys_id(),
                                            datastream_dict)
            location = r.headers.get('Location')
            self.__ds_id = location.removeprefix('/datastreams/')
            self.set_topic()
            return self.__ds_id
        else:
            raise ParentSystemNotFound()

    def get_datastream_url(self):
        """
        Get the URL of this datastream

        :return:
        """
        if self.__ds_id is None:
            raise DatastreamNotInserted()
        return f'{self.parent_system.get_system_url()}/{APITerms.DATASTREAMS.value}/{self.__ds_id}'

    def get_ds_insert_url(self):
        """
        Get the parent system's URL for datastreams

        :return:
        """
        return f'{self.parent_system.get_system_url()}/{self.parent_system.get_sys_id()}/{APITerms.DATASTREAMS.value}'

    def get_observation_url(self):
        """
        Get the URL for observations of this datastream

        :return:
        """
        return f'{self.parent_system.get_full_node_url()}/{APITerms.API.value}/{APITerms.DATASTREAMS.value}/' \
               f'{self.get_ds_id()}/{APITerms.OBSERVATIONS.value}'

    def add_root_component(self, component: DataRecordComponent):
        """
        Add a root component to the datastream. Use this method only if the datastream does not already have a root, or
        a change needs to be made to the root component. If the datastreams already has observations, this method will
        remove them as they are no longer valid.

        :param component:
        :return:
        """
        if self.root_component is not None:
            self.__observations = []
        self.root_component = component
        self.set_field_map()

    def get_ds_id(self):
        """
        Get the ID of the datastream

        :return:
        """
        return self.__ds_id

    def add_field(self, field):
        """
        Adds a field to the root component of the datastream.

        :param field:
        :return:
        """
        self.root_component.add_field(field)
        # TODO: it is not performant to rebuild the field map every time a field is added,
        #  change this in a future version
        self.set_field_map()

    def add_value_by_uuid(self, uuid, value):
        """
        Adds a value to the datastream by UUID. This method doesn't work in all cases and will be removed in a future
        version.

        .. deprecated:: 0.0.1-alpha.3
            Will be removed in 0.0.1.
            Prefer using the set_values method instead.

        :param uuid:
        :param value:
        :return:
        """
        if self.__field_map is None:
            self.set_field_map()
        self.__field_map[uuid].value = value

    def get_field_map(self):
        """
        Get the field map of the datastream. The field map is a dictionary of UUIDs to fields.
        It can be used to set values.

        .. deprecated:: 0.0.1-alpha.3
            Will be removed in 0.0.1

        :return:
        """
        self.set_field_map()
        return self.__field_map

    def set_field_map(self):
        """
        Sets the field map of the datastream. This is generated from the root component.

        :return:
        """
        field_map = self.root_component.flat_id_to_field_map()
        self.__field_map = field_map.copy()

    def create_observation_from_current(self):
        """
        Creates a new observation from the current values of the datastream and adds it to the list of observations.
        This prepares the datastream to send observations to the node.

        :return:
        """
        new_obs = Observation(parent_datastream=self)
        self.__observations.append(new_obs)

    def set_values(self, values):
        """
        Sets the values of the datastream from a dictionary. The format required is dependent on the composition of the
        components. Top level is most often a dictionary representing a DataRecordComponent.

        :param values:
        :return:
        """
        self.root_component.set_value(values)

    def send_earliest_observation(self):
        """
        Sends the first observation in the list of observations. These should be in chronological order, though setting
        manual times for can break this. To prevent issues it is recommended that observations be sent as they are created
        or created in chronological order.

        :return: True if the observation was sent successfully, False otherwise.
        """
        url = self.get_observation_url()
        if self.__observations is not None and len(self.__observations) > 0:
            obs = self.__observations[0]
            json_obs = obs.get_observation_dict()
            # TODO: we'll need to handle this differently when dealing with a binary datastream
            r = requests.post(url, json=json_obs, headers={'Content-Type': 'application/json'})
            if r.status_code == 201:
                self.__observations.pop(0)
                return True
            else:
                return False

    def send_observation_batch(self, batch_size: int):
        """
        Attempts to send a batch of observations to the OSH Node. Actual number of observations will be the least of
        the batch size and the number of observations in the list.
        """
        url = self.get_observation_url()
        batch = self.__observations[:batch_size]
        # TODO: as in send_earliest_observation, we'll need to handle this differently when dealing with a
        #  binary datastream
        r = requests.post(url, json=batch, headers={'Content-Type': 'application/json'})
        if r.status_code == 201:
            # Remove the observations that were sent
            self.__observations = self.__observations[batch_size:]
            return True
        else:
            return False

    def insert_obs_values_and_send(self, values):
        """
        Creates observations from the provided values and sends them to the OSH Node in one go.
        This is the preferred method for sending observations but set_values and create_observation_from_current can be
        called separately if required.

        :param values: dictionary uuid-value pairs where the uuid is for a field in the datastream
        :return:
        """
        self.set_values(values)
        self.create_observation_from_current()
        return self.send_earliest_observation()

    def get_obs_list(self):
        """
        Returns the list of queued observations.

        :return:
        """
        return self.__observations

    def publish_earliest_observation(self, hostname, port, tls=None, username=None, password=None,
                                     transport='websockets'):
        """
        Publishes the earliest observation to the MQTT broker but doesn't require any long-term client object.

        :param port: the port to connect to the broker on
        :param tls: a dict containing TLS configuration parameters for the client:
                    dict = {'ca_certs':"<ca_certs>", 'certfile':"<certfile>", 'keyfile':"<keyfile>",
                    'tls_version':"<tls_version>", 'ciphers':"<ciphers">}
                    ca_certs is required, all other parameters are optional and will default to None if not provided,
                    which results in the client using the default behaviour - see the paho.mqtt.client documentation.
                    Defaults to None, which indicates that TLS should not be used.
        :param username: optional, use when auth is required
        :param password: optional, use when auth is required
        :param transport: the transport to use, defaults to websockets, other option is tcp
        :param hostname: the hostname of the broker
        :return:
        """
        if self.__observations is not None and len(self.__observations) > 0:
            obs = self.__observations[0]
            json_obs = obs.get_observation_dict()
            hn = hostname if transport == 'tcp' else f'{hostname}/mqtt'
            if username is None:
                msg = publish.single(topic=self.__topic, payload=json.dumps(json_obs),
                                     hostname=hn, port=port, tls=tls,
                                     transport=transport)
                print(msg)
            else:
                publish.single(topic=self.__topic, payload=json.dumps(json_obs),
                               hostname=hn, port=port, tls=tls, auth={'username': username, 'password': password},
                               transport=transport)

    def publish_earliest_observation_client(self, client):
        """
        Publishes the earliest observation to the MQTT broker using a provided MQTT client.

        :param client: the client to use to publish the observation
        :return:
        """
        if self.__observations is not None and len(self.__observations) > 0:
            obs = self.__observations[0]
            json_obs = obs.get_observation_dict()
            client.publish(f'/api/datastreams/{self.__ds_id}/observations', msg=json.dumps(json_obs))

    def set_topic(self, topic=None):
        """
        Sets the topic for the datastream. If no topic is provided, the default topic is used.

        :param topic: MQTT topic the datastream will publish observations to
        :return: the topic set by the method
        """
        if topic is None:
            self.__topic = f'/api/datastreams/{self.__ds_id}/observations'
        else:
            self.__topic = topic
        return self.__topic


@dataclass
class Observation:
    """
    An observation is a single data point for a datastream. They are intended to be created by the parent datastream,
    but can be created manually. Doing so may result in unexpected behavior.

    Attributes:
        parent_datastream: The datastream that this observation belongs to
        id: The UUID of the observation
        timestamp: The timestamp of the observation
        __name_value_map: A dictionary of the field names and their respective values
        __observation_dict: A dictionary representation of the observation for conversion to JSON
    """

    def __init__(self, parent_datastream: Datastream, timestamp: datetime = None):
        """
        Creates a new observation for the given datastream. If no timestamp is provided, the current time will be used.

        :param parent_datastream:
        :param timestamp:
        """
        self.parent_datastream = parent_datastream
        self.id = uuid.uuid4()
        self.timestamp = None
        self.__name_value_map = None
        self.__observation_dict = None
        self.create_name_value_map()

        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)
        else:
            self.timestamp = timestamp
        self.create_observation_dict_with_time(self.timestamp)

    def create_name_value_map(self):
        self.parent_datastream.set_field_map()
        self.__name_value_map = dict([])
        for field in self.parent_datastream.get_field_map().values():
            self.__name_value_map[field.name] = field.value
        return self.__name_value_map

    def create_observation_dict(self):
        self.__observation_dict = dict([
            ('phenomenonTime', datetime.now(timezone.utc).isoformat()),
            ('result', self.parent_datastream.root_component.get_value())
        ])
        return self.__observation_dict

    def create_observation_dict_with_time(self, obs_time: datetime):
        self.__observation_dict = dict([
            ('phenomenonTime', obs_time.isoformat()),
            ('result', self.create_name_value_map())
        ])
        return self.__observation_dict

    def get_observation_dict(self):
        return self.__observation_dict

    def get_observation_json(self):
        # for key, record in self.__observation_dict['result'].items():
        #     if isinstance(record, datetime):
        #         self.__observation_dict['result'][record] = record.isoformat()

        return json.dumps(self.__observation_dict, indent=4, default=str)


class ParentSystemNotFound(Exception):

    def __init__(self, message="Cannot insert datastream without a parent system"):
        self.message = message
        super().__init__(self.message)


class InvalidDatastream(Exception):
    def __init__(self, message=f'The Datastream cannot be built. Please check that all required fields are set'):
        self.message = message
        super().__init__(self.message)


class DatastreamNotInserted(Exception):
    def __init__(self, message=f'The Datastream has not been inserted into the OSH Node. '
                               f'Please insert the datastream before attempting to insert observations'):
        self.message = message
        super().__init__(self.message)
