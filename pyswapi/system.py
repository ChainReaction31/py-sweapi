import json
from dataclasses import dataclass

import requests

from pyswapi.constants import SystemTypes, APITerms
from pyswapi.endpoints import system_ep as system_eps


def build_systems_from_node(node_url, node_port, node_endpoint):
    response = system_eps.get_systems(node_api_endpoint=f'{node_url}:{node_port}{node_endpoint}/{APITerms.API.value}')
    systems = []
    if response.ok:
        print(response.json())
        for sys in response.json()['items']:
            print(sys)
            new_system = System(
                name=sys['properties']['name'],
                uid=sys['properties']['uid'],
                node_url=node_url,
                node_port=node_port,
                node_endpoint=node_endpoint,
            )
            new_system.set_sys_id(sys['id'])
            if 'definition' in sys['properties']:
                new_system.definition = sys['properties']['definition']
                new_system.def_type = sys['properties']['type']
            if 'description' in sys['properties']:
                new_system.description = sys['properties']['description']

            systems.append(new_system)
        return systems


@dataclass
class System:
    """
    The System class is used to describe sets of datastreams via the Connected Systems API.

    Attributes:
        name: Human readable name for the system
        uid: A unique identifier for the system
        definition: A URL to the definition of the system
        def_type: The type of system, e.g. 'Feature'
        description: A human readable description of the system
        node_url: The URL of the OSH Node to which the system will be inserted
        node_port: The port through which to access the Node
        node_endpoint: The endpoint of the OSH Node to which the system will be inserted. Usually 'sensorhub'
        system_dict: A dictionary representation of the system
        __sys_id: The id of the system in the OSH Node
    """
    name: str = None
    uid: str = None
    definition: str = None
    def_type: str = None
    description: str = None
    node_url: str = None
    node_port: int = None
    node_endpoint: str = None
    system_dict: dict = None
    __sys_id: str = None

    def build_system_dict(self):
        properties = dict([

            ('name', self.name),
            ('uid', self.uid),
            ('definition', self.definition),
            ('description', self.description),
            ('type', self.def_type)
        ])

        self.system_dict = dict([
            ('type', SystemTypes.FEATURE.value),
            ('properties', properties)
        ])

    def generate_json(self) -> str:
        self.build_system_dict()
        return json.dumps(self.system_dict)

    def insert_system(self) -> str:
        """
                Naively tries to insert the specified system into the OSH Node specified by its url.
                :return: The id of the system
                See https://opensensorhub.github.io/sensorweb-api/swagger-ui

                :return:
                """

        temp_id = self.__sys_id
        if self.system_dict is None:
            self.build_system_dict()

        if temp_id is None or temp_id == '':
            r = requests.post(self.get_system_url(), json=self.system_dict,
                              headers={'Content-Type': 'application/json'})

            # This is what we hope to get, but cases arise where the sensor is already inserted
            if r.status_code == 201:
                temp_id = r.headers.get('Location').removeprefix('/systems/')

            # This means the result told us we already had a matching sensor inserted
            elif r.status_code == 400:
                # Additional parameters are possible, but not needed at this time
                r = requests.get(self.get_system_url(), params={'validTime': '../..'})
                decoded_content = r.json()['items'][0]
                temp_id = decoded_content['id']

            else:
                # TODO: add error handling
                print('Error inserting system')
                return None

            self.__sys_id = temp_id
            return self.__sys_id
        return temp_id

    def get_full_node_url(self) -> str:
        """
        Returns the full url of the node, including the port (if specified) and endpoint
        :return: the full url of the node as a string
        """
        if self.node_port is None:
            return f"{self.node_url}/{self.node_endpoint}"
        else:
            return f"{self.node_url}:{str(self.node_port)}/{self.node_endpoint}"

    def get_system_url(self):
        return f"{self.get_full_node_url()}/{APITerms.API.value}/{APITerms.SYSTEMS.value}"

    # TODO: add this method to datastream
    def get_observation_url(self, datastream_id):
        url = f"{self.get_full_node_url()}/{APITerms.API.value}/{APITerms.DATASTREAMS.value}/{datastream_id}/{APITerms.OBSERVATIONS.value}"
        return url

    def add_datastream(self, datastream):
        self.datastreams.append(datastream)

    def get_sys_id(self):
        return self.__sys_id

    def set_sys_id(self, sys_id):
        self.__sys_id = sys_id


class SystemBuilder:

    def __init__(self):
        self.system = System()

    def with_name(self, name):
        self.system.name = name
        return self

    def with_uid(self, uid):
        self.system.uid = uid
        return self

    def with_definition(self, definition):
        self.system.definition = definition
        self.system.def_type = definition
        return self

    def with_description(self, description):
        self.system.description = description
        return self

    def with_node(self, node_url, node_port, node_endpoint):
        self.system.node_url = node_url
        self.system.node_port = node_port
        self.system.node_endpoint = node_endpoint
        return self

    def build(self):
        return self.system
