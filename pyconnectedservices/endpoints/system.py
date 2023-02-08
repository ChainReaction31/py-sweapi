import requests

from pyconnectedservices.constants import APITerms


def get_systems(node_api_endpoint=None, params: dict = None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}'

    r = requests.get(base_url, params=params)

    if r.status_code == 200:
        return r.json().items
    elif not r.ok:
        raise ValueError(f'Error getting systems: {r.status_code}')


def get_system(node_api_endpoint=None, params=None, system_id=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}'

    r = requests.get(base_url, params=params)

    if r.status_code == 200:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error getting system: {r.status_code}')


def get_system_details(node_api_endpoint=None, params=None, system_id=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/details'

    r = requests.get(base_url, params=params)

    if r.status_code == 200:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error getting system details: {r.status_code}')


def get_system_datastreams(node_api_endpoint=None, params=None, system_id=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/datastreams'

    r = requests.get(base_url, params=params)

    if r.status_code == 200:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error getting system datastreams: {r.status_code}')


def get_system_controls(node_api_endpoint=None, params=None, system_id=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/controls'

    r = requests.get(base_url, params=params)

    if r.status_code == 200:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error getting system controls: {r.status_code}')


def get_system_fois(node_api_endpoint=None, params=None, system_id=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/featuresOfInterest'

    r = requests.get(base_url, params=params)

    if r.status_code == 200:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error getting system features: {r.status_code}')


def get_system_history(node_api_endpoint=None, params=None, system_id=None, version=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/history'

    if version is not None:
        base_url = f'{base_url}/{version}'

    r = requests.get(base_url, params=params)

    if r.status_code == 200:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error getting system history: {r.status_code}')


def post_system(node_api_endpoint=None, system=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}'

    r = requests.post(base_url, json=system)

    if r.status_code == 201:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error posting system: {r.status_code}')


def post_system_contact(node_api_endpoint=None, system_id=None, contact=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/contacts'

    r = requests.post(base_url, json=contact)

    if r.status_code == 201:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error posting system contacts: {r.status_code}')


def post_system_events(node_api_endpoint=None, system_id=None, events=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/events'

    r = requests.post(base_url, json=events)

    if r.status_code == 201:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error posting system events: {r.status_code}')


def post_system_member(node_api_endpoint=None, system_id=None, member=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/members'

    r = requests.post(base_url, json=member)

    if r.status_code == 201:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error posting system members: {r.status_code}')


def post_system_datastream(node_api_endpoint=None, system_id=None, datastream=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/datastreams'

    r = requests.post(base_url, json=datastream)

    if r.status_code == 201:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error posting system datastream: {r.status_code}')


def post_system_controls(node_api_endpoint=None, system_id=None, controls=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/controls'

    r = requests.post(base_url, json=controls)

    if r.status_code == 201:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error posting system controls: {r.status_code}')


def post_system_foi(node_api_endpoint=None, system_id=None, foi=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/featuresOfInterest'

    r = requests.post(base_url, json=foi)

    if r.status_code == 201:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error posting system features: {r.status_code}')


def post_system_history(node_api_endpoint=None, system_id=None, history=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/history'

    r = requests.post(base_url, json=history)

    if r.status_code == 201:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error posting system history: {r.status_code}')


def put_system(node_api_endpoint=None, system_id=None, system=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}'

    r = requests.put(base_url, json=system)

    if r.status_code == 200:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error putting system: {r.status_code}')


def put_system_details(node_api_endpoint=None, system_id=None, details=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/details'

    r = requests.put(base_url, json=details)

    if r.status_code == 200:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error putting system details: {r.status_code}')


def put_system_history_version(node_api_endpoint=None, system_id=None, version=None,
                               history=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/history/{version}'

    r = requests.put(base_url, json=history)

    if r.status_code == 200:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error putting system history: {r.status_code}')
