import json
import requests

from osh_connected_services.constants import SystemTypes


def build_system_dict(name, uid, definition, def_type, description) -> dict:
    properties = dict([
        ('definition', definition),
        ('name', name),
        ('uid', uid),
        ('type', def_type),
        ('description', description)
    ])

    return dict([
        ('type', SystemTypes.FEATURE.value),
        ('properties', properties)
    ])


def generate_json(system_dict) -> str:
    return json.dumps(system_dict)


def insert_system(url, system_dict: dict, sys_id=None) -> str:
    """
            Naively tries to insert the specified system into Hub at the URL provided.
            If it is found to be present, then the id will be set
            :param url: URL of the Hub to insert system into
            :param system_dict: dictionary with the type and properties needed to create a valid SWEAPI System.
            :param sys_id: optional, if a system id is provided, this method only returns that value
            See https://opensensorhub.github.io/sensorweb-api/swagger-ui

            :return:
            """

    temp_id = sys_id

    if temp_id is None or temp_id == '':
        r = requests.post(url, json=system_dict, headers={'Content-Type': 'application/json'})

        # This is what we hope to get, but cases arise where the sensor is already inserted
        if r.status_code == 201:
            temp_id = r.headers.get('Location').removeprefix('/systems/')
            print(r.headers.get('Location'))

        # This means the result told us we already had a matching sensor inserted
        elif r.status_code == 400:
            r = requests.get(url, params={'validTime': '../..', 'q': 'ply'})
            decoded_content = r.json()['items'][0]
            temp_id = decoded_content['id']

        else:
            # TODO: add error handling
            print('Error inserting system')

        return temp_id
    return temp_id
