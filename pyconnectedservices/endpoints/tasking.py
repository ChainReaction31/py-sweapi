import requests

from pyconnectedservices.constants import APITerms


def get_tasking_interface(node_api_endpoint=None, params=None, system_id=None, tasking_id=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/{APITerms.TASKING.value}'

    if tasking_id is not None:
        base_url += f'/{tasking_id}'

    r = requests.get(base_url, params=params)

    if r.status_code == 200:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error getting tasking interface: {r.status_code}')


def get_tasking_inteface_schema(node_api_endpoint=None, params=None, system_id=None, tasking_id=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/{APITerms.TASKING.value}' \
               f'/{tasking_id}/schema'

    r = requests.get(base_url, params=params)

    if r.status_code == 200:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error getting tasking interface schema: {r.status_code}')


def get_tasking_interface_commands(node_api_endpoint=None, params=None, system_id=None, tasking_id=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/{APITerms.TASKING.value}/{tasking_id}/commands'

    r = requests.get(base_url, params=params)

    if r.status_code == 200:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error getting tasking interface commands: {r.status_code}')


def get_tasking_interface_status(node_api_endpoint=None, params=None, system_id=None, tasking_id=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/{APITerms.TASKING.value}/{tasking_id}/status'

    r = requests.get(base_url, params=params)

    if r.status_code == 200:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error getting tasking interface status: {r.status_code}')


def get_command_status(node_api_endpoint=None, params=None, system_id=None, tasking_id=None, command_id=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/{APITerms.TASKING.value}' \
               f'/{tasking_id}/commands/{command_id}/status'

    r = requests.get(base_url, params=params)

    if r.status_code == 200:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error getting command status: {r.status_code}')


def post_command(node_api_endpoint=None, system_id=None, tasking_id=None, command=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/{APITerms.TASKING.value}' \
               f'/{tasking_id}/commands'

    r = requests.post(base_url, json=command)

    if r.status_code == 201:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error posting command: {r.status_code}')


def post_command_status(node_api_endpoint=None, system_id=None, tasking_id=None, command_id=None,
                        status=None):
    base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/{APITerms.TASKING.value}' \
               f'/{tasking_id}/commands/{command_id}/status'

    r = requests.post(base_url, json=status)

    if r.status_code == 201:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error posting command status: {r.status_code}')
