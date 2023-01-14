import requests

from osh_connected_services.constants import APITerms


def create_datastream_schema(obs_format, result_schema, result_encoding):
    schema = dict([
        ('obsFormat', obs_format),
        ('resultSchema', result_schema),
        ('resultEncoding', result_encoding)
    ])
    return schema


def insert_datastream(systems_url, system_id, ds_output_name, ds_name, ds_description, result_schema, result_encoding):
    datastream_dict = dict([
        ('outputName', ds_output_name),
        ('name', ds_name),
        ('description', ds_description),
        ('schema', create_datastream_schema('application/om+json', result_schema, result_encoding)),
    ])

    full_url = systems_url + f'/{system_id}' + APITerms.DATASTREAMS.value
    r = requests.post(full_url, json=datastream_dict, headers={'Content-Type': 'application/json'})
    location = r.headers.get('Location')
    ds_id = location.removeprefix('/datastreams/')
    return ds_id


data_types_dict = dict([
    ('f4', 'float'),
    ('u1', 'uchar')
])
