import requests
from oshdatacore.component_implementations import DataRecordComponent
from oshdatacore.encoding import AbstractEncoding

from pyconnectedservices.constants import APITerms, ObservationFormat
from pyconnectedservices.system import System


class Datastream:
    """
    Datastreams define the structure of data sent to an OSH Node. They provide a means of defining what and how
    data must be packaged.

    A builder is provided to make the creation of datastreams less complex
    """

    def __init__(self):
        """
        Datastreams are intended to be build using DatastreamBuilder
        """

        self.name: str = None
        """Human readable name for the datastream"""
        self.description: str = None
        """A brief description of the datastream"""
        self.output_name: str = None
        """The machine name of the datastream, often lowercase and hyphenated (e.g. 'your-output')"""
        self.encoding: AbstractEncoding = None
        """One of the supported encodings"""
        self.root_component: DataRecordComponent = None
        """The DataRecordComponent that is the root of the datastream"""
        self.obs_format: ObservationFormat = None
        """The observation format of the datastream (e.g. 'application/om+json')"""
        self.schema: dict = None
        """The JSON schema of the datastream. Generated by create_datastream_schema()"""
        self.parent_system: System = None
        """The parent system of the datastream"""
        self.__ds_id: str = None
        """The internal id of the datastream"""

    def get_fields(self):
        return self.root_component.get_fields()

    def create_datastream_schema(self):
        """
        create the schema for the datastream, returns the schema if it already exists
        :return:
        """
        if self.schema is None:
            schema = dict([
                ('obsFormat', self.obs_format),
                ('resultSchema', self.root_component.datastructure_to_dict()),
                ('resultEncoding', self.encoding)
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

            full_url = f'{self.parent_system.get_system_url()}/{APITerms.DATASTREAMS.value}'
            r = requests.post(full_url, json=datastream_dict, headers={'Content-Type': 'application/json'})
            location = r.headers.get('Location')
            self.__ds_id = location.removeprefix('/datastreams/')
            return self.__ds_id
        else:
            raise ParentSystemNotFound()

    def get_datastream_url(self):
        return f'{self.parent_system.get_system_url()}/{APITerms.DATASTREAMS.value}/{self.__ds_id}'

    def add_root_component(self, component: DataRecordComponent):
        self.root_component = component


class DatastreamBuilder:
    def __init__(self):
        self.datastream = Datastream()

    def with_name(self, name):
        self.datastream.name = name

    def with_description(self, description):
        self.datastream.description = description

    def with_encoding(self, encoding: AbstractEncoding):
        self.datastream.encoding = encoding

    def with_observation_format(self, obs_format: ObservationFormat):
        self.datastream.obs_format = obs_format

    def with_root_component(self, component: DataRecordComponent):
        self.datastream.root_component = component

    def with_parent_system(self, system: System):
        self.datastream.parent_system = system

    def build(self):
        for (k, v) in self.__dict__.items():
            if v is None:
                raise InvalidDatastream(f'The Datastream cannot be built because {k} is not set')
        return self.datastream


class ParentSystemNotFound(Exception):

    def __init__(self, message="Cannot insert datastream without a parent system"):
        self.message = message
        super().__init__(self.message)


class InvalidDatastream(Exception):
    def __init__(self, message=f'The Datastream cannot be built. Please check that all required fields are set'):
        self.message = message
        super().__init__(self.message)
