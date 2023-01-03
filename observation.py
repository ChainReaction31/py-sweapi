import requests
from datetime import datetime, timezone
from osh_data_core.datamodels import DataRecordComponent, AbstractDataComponent


def create_result_dict(root_output: DataRecordComponent):
    result_dict = dict([])

    for field in root_output.fields:
        if isinstance(field, DataRecordComponent):
            # create a dictionary of name->value for each field
            result_dict[field.name] = map_record_fields_to_dict(field)
            pass
        elif isinstance(field, AbstractDataComponent):
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
        elif isinstance(field, AbstractDataComponent):
            result_dict[field.name] = field.value

    return result_dict


def send_result(url, root_record):
    result_json = create_result_dict(root_record)
    r = requests.post(url, json=result_json, headers={'Content-Type': 'application/json'})


def send_result_batch(url, result_list):
    r = requests.post(url, json=result_list, headers={'Content-Type': 'application/json'})
