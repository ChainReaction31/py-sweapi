import json
import requests

from pyconnectedservices.constants import SystemTypes, APITerms


class System:
    """Should only be assigned by the OSH Node, changing this value manually will break things"""

    def __init__(self):
        """
        Systems are intended to be built using the SystemBuilder
        """
        self.name: str = None
        self.uid: str = None
        self.definition: str = None
        self.def_type: str = None
        self.description: str = None
        self.node_url: str = None
        self.node_port: int = None
        self.node_endpoint: str = None
        self.system_dict: dict = None
        self.__sys_id: str = None

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
                Naively tries to insert the specified system into Hub at the URL provided.
                If it is found to be present, then the id will be set
                :param url: URL of the Hub to insert system into
                :param system_dict: dictionary with the type and properties needed to create a valid SWEAPI System.
                :param sys_id: optional, if a system id is provided, this method only returns that value
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

    def get_full_node_url(self):
        return f"{self.node_url}:{str(self.node_port)}/{self.node_endpoint}"

    def get_system_url(self):
        return f"{self.get_full_node_url()}/{APITerms.API.value}/{APITerms.SYSTEMS.value}"

    # TODO: add this method to datastream
    def get_observation_url(self, datastream_id):
        url = f"{self.get_full_node_url()}/{APITerms.API.value}/{APITerms.DATASTREAMS.value}/{datastream_id}/{APITerms.OBSERVATIONS.value}"
        return url

    def add_datastream(self, datastream):
        self.datastreams.append(datastream)


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
