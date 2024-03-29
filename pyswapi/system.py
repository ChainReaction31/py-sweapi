import json
from dataclasses import dataclass

from pyswapi.constants import SystemTypes, APITerms
from pyswapi.endpoints import system_ep as system_eps


def build_systems_from_node(node_url, node_port, node_endpoint):
    """
    Builds a list of System objects from a given OSH Node. The API requires multiple calls to retrieve all provided
    metadata and even then can lose some resolution. As such, it is recommended to manually create a representation of
    the system, but this method does enable a fast way to get a list of systems and perform quick operations on them.

    :param node_url: base URL of the node
    :param node_port: port the node is running on (often 8181 or 8282)
    :param node_endpoint: endpoint of the node, typically 'sensorhub' or APITerms.SENSORHUB.type

    :return: a list of System objects
    """
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
        description: A human-readable description of the system
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
        """
        Builds a dictionary representation of the system. This is necessary as the API requires a JSON representation.

        :return:
        """
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
        Naively tries to insert the system into the OSH Node specified by its url.

        :return: The id of the system
        """

        temp_id = self.__sys_id
        if self.system_dict is None:
            self.build_system_dict()

        # Check for existing system
        check_sys = system_eps.get_systems(node_api_endpoint=self.get_node_api_url(), params={'uid': self.uid})
        if check_sys.ok and len(check_sys.json()['items']) > 0:
            temp_id = check_sys.json()['items'][0]['id']
            self.__sys_id = temp_id

        if temp_id is None or temp_id == '':
            r = system_eps.post_system(node_api_endpoint=self.get_node_api_url(), system=self.system_dict)

            # This is what we hope to get, but cases arise where the sensor is already inserted
            if r.status_code == 201:
                temp_id = r.headers.get('Location').removeprefix('/systems/')
            else:
                # TODO: add specific Exception
                raise Exception(f"Error inserting system: {r.text}")

            self.__sys_id = temp_id
            return self.__sys_id
        return temp_id

    def get_full_node_url(self) -> str:
        """
        Returns the full URL of the node, including the port (if specified) and endpoint

        :return: the full URL of the node as a string
        """
        if self.node_port is None:
            return f"{self.node_url}/{self.node_endpoint}"
        else:
            return f"{self.node_url}:{str(self.node_port)}/{self.node_endpoint}"

    def get_node_api_url(self):
        """
        returns the node's API URL

        :return:
        """
        return f"{self.get_full_node_url()}/{APITerms.API.value}"

    def get_system_url(self):
        """
        Returns the node's system URL for the API

        :return:
        """
        return f"{self.get_full_node_url()}/{APITerms.API.value}/{APITerms.SYSTEMS.value}"

    # TODO: add this method to datastream
    def get_observation_url(self, datastream_id):
        """
        Returns the URL for the observations of a given datastream

        :param datastream_id:

        :return:
        """
        url = f"{self.get_full_node_url()}/{APITerms.API.value}/{APITerms.DATASTREAMS.value}/{datastream_id}/{APITerms.OBSERVATIONS.value}"
        return url

    def add_datastream(self, datastream):
        """
        Adds a datastream to the system

        :param datastream:

        :return:
        """
        self.datastreams.append(datastream)

    def get_sys_id(self):
        """
        Returns the id of the system in the OSH Node

        :return:
        """
        return self.__sys_id

    def set_sys_id(self, sys_id):
        """
        Sets the id of the system in the OSH Node. This should only need to be called when the system is inserted

        :param sys_id:

        :return:
        """
        self.__sys_id = sys_id


class SystemBuilder:

    def __init__(self):
        """
        The SystemBuilder class is used to build a System object. It can be used instead of the System class's
        constructor.
        """
        self.system = System()

    def with_name(self, name):
        """
        Sets the name of the system

        :param name:

        :return:
        """
        self.system.name = name
        return self

    def with_uid(self, uid):
        """
        Sets the uid of the system

        :param uid:

        :return:
        """
        self.system.uid = uid
        return self

    def with_definition(self, definition):
        """
        Sets the definition of the system

        :param definition:

        :return:
        """
        self.system.definition = definition
        self.system.def_type = definition
        return self

    def with_description(self, description):
        """
        Sets the description of the system

        :param description:

        :return:
        """
        self.system.description = description
        return self

    def with_node(self, node_url, node_port, node_endpoint):
        """
        Sets the node url, port, and endpoint

        :param node_url:
        :param node_port:
        :param node_endpoint:

        :return:
        """
        self.system.node_url = node_url
        self.system.node_port = node_port
        self.system.node_endpoint = node_endpoint
        return self

    def build(self):
        """
        Builds the system and returns it.

        :return:
        """
        return self.system
