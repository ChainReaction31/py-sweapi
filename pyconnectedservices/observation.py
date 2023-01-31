import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

import requests
from oshdatacore.component_implementations import DataRecordComponent
from oshdatacore.datamodels_core import DataComponentImpl

from pyconnectedservices.datastream import Datastream


def create_result_dict(root_output: DataRecordComponent):
    result_dict = dict([])

    for field in root_output.fields:
        if isinstance(field, DataRecordComponent):
            # create a dictionary of name->value for each field
            result_dict[field.name] = map_record_fields_to_dict(field)
            pass
        elif isinstance(field, DataComponentImpl):
            result_dict[field.name] = field.value

    observation = dict([
        ('phenomenonTime', datetime.now(timezone.utc).isoformat()),
        ('result', result_dict)
    ])
    return observation


def map_record_fields_to_dict(data_record: DataRecordComponent):
    result_dict = dict([])

    for field in data_record.fields:
        if isinstance(field, DataRecordComponent):
            result_dict[field.name] = map_record_fields_to_dict(field)
        elif isinstance(field, DataComponentImpl):
            result_dict[field.name] = field.value

    return result_dict


def send_result(url, root_record):
    result_json = create_result_dict(root_record)
    r = requests.post(url, json=result_json, headers={'Content-Type': 'application/json'})


def send_result_batch(url, result_list):
    r = requests.post(url, json=result_list, headers={'Content-Type': 'application/json'})


@dataclass
class Observation:
    id: UUID = uuid.uuid4()
    parent_datastream: Datastream = None
    __name_value_map: dict = None
    __observation_dict: dict = None

    def create_name_value_map(self):
        self.parent_datastream.set_field_map()
        self.__name_value_map = dict([])
        for field in self.parent_datastream.get_field_map().values():
            self.__name_value_map[field.name] = field.value
        return self.__name_value_map

    def create_observation_dict(self):
        self.__observation_dict = dict([
            ('phenomenonTime', datetime.now(timezone.utc).isoformat()),
            ('result', self.create_name_value_map())
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
        return json.dumps(self.__observation_dict, indent=4)
