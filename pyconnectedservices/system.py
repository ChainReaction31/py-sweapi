import json
import requests

from constants import SystemTypes, APITerms


class System:
    name: str
    uid: str
    definition: str
    def_type: str
    description: str
    node_url: str
    system_dict: dict
    __sys_id: str
    """Should only be assigned by the OSH Node, changing this value manually will break things"""

    def __init__(self, name, uid, definition, description, node_url):
        """

        :param name: Human-readable name of the system
        :param uid: a URN (Uniform Resource Name) that is unique to the system with respect to the node
        :param definition: URI/URL to an ontological definition of the system
        :param description: a description of the system. Brevity is preferred, but the field can be of any length.
        :param node_url: The root url of the node
        """
        self.node_port = None
        self.node_endpoint = None
        self.name = name
        self.uid = uid
        self.definition = definition
        self.def_type = definition
        self.description = description
        self.node_url = node_url

    def build_system_dict(self):
        properties = dict([
            ('definition', self.definition),
            ('name', self.name),
            ('uid', self.uid),
            ('type', self.def_type),
            ('description', self.description)
        ])

        self.system_dict = dict([
            ('type', SystemTypes.FEATURE.value),
            ('properties', properties)
        ])

    def generate_json(self) -> str:
        return json.dumps(self.build_system_dict())

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

        if temp_id is None or temp_id == '':
            r = requests.post(self.url, json=self.system_dict, headers={'Content-Type': 'application/json'})

            # This is what we hope to get, but cases arise where the sensor is already inserted
            if r.status_code == 201:
                temp_id = r.headers.get('Location').removeprefix('/systems/')
                print(r.headers.get('Location'))

            # This means the result told us we already had a matching sensor inserted
            elif r.status_code == 400:
                r = requests.get(self.url, params={'validTime': '../..', 'q': 'ply'})
                decoded_content = r.json()['items'][0]
                temp_id = decoded_content['id']

            else:
                # TODO: add error handling
                print('Error inserting system')

            return temp_id
        return temp_id

    def get_node_url(self):
        return f"{self.node_url}:{str(self.node_port)}{self.node_endpoint}"

    def get_system_url(self):
        return f"{self.get_node_url()}{APITerms.API.value}{APITerms.SYSTEMS.value}"

    # TODO: add this method to datastream
    def get_observation_url(self, datastream_id):
        url = f"{self.get_node_url()}{APITerms.API.value}{APITerms.DATASTREAMS.value}/{datastream_id}{APITerms.OBSERVATIONS.value}"
        return url
