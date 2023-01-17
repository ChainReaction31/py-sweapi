"""Outputs are a collection of datamodel types"""
import requests
from oshdatacore.component_implementations import DataRecordComponent
from oshdatacore.encoding import AbstractEncoding

from pyconnectedservices.constants import APITerms, ObservationFormat
from pyconnectedservices.system import System


class Datastream:
    """
    The base output is simply a DataRecord with a timestamp component.
    """

    def __init__(self):
        """
        Datastreams are intended to be build using DatastreamBuilder
        """

        self.name: str
        self.description: str
        self.output_name: str
        self.encoding: AbstractEncoding
        self.root_component: DataRecordComponent
        self.obs_format: ObservationFormat
        self.schema: dict = None
        self.parent_system: System
        self.__ds_id = None
        self.root_component : DataRecordComponent = None

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
            self.ds_id = location.removeprefix('/datastreams/')
            return self.ds_id
        else:
            raise ParentSystemNotFound()

    def get_datastream_url(self):
        return f'{self.parent_system.get_system_url()}{APITerms.DATASTREAMS.value}/{self.ds_id}'


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


class ParentSystemNotFound(Exception):

    def __init__(self, message="Cannot insert datastream without a parent system"):
        self.message = message
        super().__init__(self.message)
