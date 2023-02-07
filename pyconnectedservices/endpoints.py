from enum import Enum

import requests

from pyconnectedservices.constants import APITerms


class SystemQueryParams(Enum):
    Keywords = 'q'
    """
    A comma-separated list of keywords to search for in the system name, description, and definition.
    """
    BBOX = 'bbox'
    """
    BBOX to fileter resources based on their location
    """
    LOCATION = 'location'
    """
    WKT geometry to filter resources based on their location or geometry
    """
    VALID_TIME = 'validTime'
    """
    ISO 8601 time interval to filter resources based on their valid time. When omitted, the implicit time is "now"
    except for "history" collection where no filtering is applied.
    """
    PARENT = 'parent'
    """
    Comma-separated list of parent system IDs or "*" to included nested resources at any level
    """
    SELECT = 'select'
    """
    Comma-separated list of properties to include or exclude from results (use "!" prefix to exclude)
    """
    FORMAT = 'format'
    """
    Mime type of the response format.
    """
    LIMIT = 'limit'
    """
    Maximum number of resources to return per page (max 1000)
    """
    OFFSET = 'offset'
    """
    Token specifying the page to return (usually the token provided in the previous call)
    """

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class SystemsEndpoints:
    params = {
        'q', 'bbox', 'location', 'validTime', 'parent', 'select', 'format', 'limit', 'offset'
    }

    def get_systems(self, node_api_endpoint=None, params: dict = None):
        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}'

        if params is not None and any(key in self.params for key in params):
            raise ValueError(f'Invalid query parameter. Valid parameters are {SystemQueryParams}')

        r = requests.get(base_url, params=params)

        if r.status_code == 200:
            return r.json().items
        elif not r.ok:
            raise ValueError(f'Error getting systems: {r.status_code}')

    def get_system(self, node_api_endpoint=None, params=None, system_id=None):

        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}'

        r = requests.get(base_url)

        if r.status_code == 200:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error getting system: {r.status_code}')

    def get_system_details(self, node_api_endpoint=None, params=None, system_id=None):

        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/details'

        r = requests.get(base_url)

        if r.status_code == 200:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error getting system details: {r.status_code}')

    def get_system_datastreams(self, node_api_endpoint=None, params=None, system_id=None):

        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/datastreams'

        r = requests.get(base_url)

        if r.status_code == 200:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error getting system datastreams: {r.status_code}')

    def get_system_controls(self, node_api_endpoint=None, params=None, system_id=None):

        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/controls'

        r = requests.get(base_url)

        if r.status_code == 200:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error getting system controls: {r.status_code}')

    def get_system_fois(self, node_api_endpoint=None, params=None, system_id=None):

        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/featuresOfInterest'

        r = requests.get(base_url)

        if r.status_code == 200:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error getting system features: {r.status_code}')

    def get_system_history(self, node_api_endpoint=None, params=None, system_id=None, version=None):

        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/history'

        if version is not None:
            base_url = f'{base_url}/{version}'

        r = requests.get(base_url)

        if r.status_code == 200:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error getting system history: {r.status_code}')

    def post_system(self, node_api_endpoint=None, params=None, system_id=None, system=None):

        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}'

        r = requests.post(base_url, json=system)

        if r.status_code == 201:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error posting system: {r.status_code}')

    def post_system_contacts(self, node_api_endpoint=None, params=None, system_id=None, contacts=None):

        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/contacts'

        r = requests.post(base_url, json=contacts)

        if r.status_code == 201:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error posting system contacts: {r.status_code}')

    def post_system_events(self, node_api_endpoint=None, params=None, system_id=None, events=None):

        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/events'

        r = requests.post(base_url, json=events)

        if r.status_code == 201:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error posting system events: {r.status_code}')

    def post_system_members(self, node_api_endpoint=None, params=None, system_id=None, members=None):

        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/members'

        r = requests.post(base_url, json=members)

        if r.status_code == 201:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error posting system members: {r.status_code}')

    def post_system_datastream(self, node_api_endpoint=None, params=None, system_id=None, datastream=None):

        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/datastreams'

        r = requests.post(base_url, json=datastream)

        if r.status_code == 201:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error posting system datastream: {r.status_code}')

    def post_system_controls(self, node_api_endpoint=None, params=None, system_id=None, controls=None):

        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/controls'

        r = requests.post(base_url, json=controls)

        if r.status_code == 201:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error posting system controls: {r.status_code}')

    def post_system_fois(self, node_api_endpoint=None, params=None, system_id=None, fois=None):

        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/featuresOfInterest'

        r = requests.post(base_url, json=fois)

        if r.status_code == 201:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error posting system features: {r.status_code}')

    def post_system_history(self, node_api_endpoint=None, params=None, system_id=None, history=None):

        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/history'

        r = requests.post(base_url, json=history)

        if r.status_code == 201:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error posting system history: {r.status_code}')

    def put_system(self, node_api_endpoint=None, params=None, system_id=None, system=None):

        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}'

        r = requests.put(base_url, json=system)

        if r.status_code == 200:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error putting system: {r.status_code}')

    def put_system_details(self, node_api_endpoint=None, params=None, system_id=None, details=None):

        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/details'

        r = requests.put(base_url, json=details)

        if r.status_code == 200:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error putting system details: {r.status_code}')

    def put_system_history_version(self, node_api_endpoint=None, params=None, system_id=None, version=None,
                                   history=None):

        base_url = f'{node_api_endpoint}/{APITerms.SYSTEMS.value}/{system_id}/history/{version}'

        r = requests.put(base_url, json=history)

        if r.status_code == 200:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error putting system history: {r.status_code}')


class FOIEndpoints:
    def get_foi(self, node_api_endpoint=None, params=None, foi_id=None):

        base_url = f'{node_api_endpoint}/{APITerms.FOIS.value}'

        if foi_id is not None:
            base_url += f'/{foi_id}'

        r = requests.get(base_url, params=params)

        if r.status_code == 200:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error getting FOI: {r.status_code}')

    def get_foi_history(self, node_api_endpoint=None, params=None, foi_id=None, version=None):

        base_url = f'{node_api_endpoint}/{APITerms.FOIS.value}/{foi_id}/history'

        if version is not None:
            base_url += f'/{version}'

        r = requests.get(base_url, params=params)

        if r.status_code == 200:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error getting FOI history: {r.status_code}')

    def get_foi_members(self, node_api_endpoint=None, params=None, foi_id=None):

        base_url = f'{node_api_endpoint}/{APITerms.FOIS.value}/{foi_id}/members'

        r = requests.get(base_url, params=params)

        if r.status_code == 200:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error getting FOI members: {r.status_code}')

    def post_foi(self, node_api_endpoint=None, params=None, foi=None):

        base_url = f'{node_api_endpoint}/{APITerms.FOIS.value}'

        r = requests.post(base_url, json=foi)

        if r.status_code == 201:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error posting FOI: {r.status_code}')

    def post_foi_history(self, node_api_endpoint=None, params=None, foi_id=None, history=None):

        base_url = f'{node_api_endpoint}/{APITerms.FOIS.value}/{foi_id}/history'

        r = requests.post(base_url, json=history)

        if r.status_code == 201:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error posting FOI history: {r.status_code}')

    def post_foi_members(self, node_api_endpoint=None, params=None, foi_id=None, member=None):

        base_url = f'{node_api_endpoint}/{APITerms.FOIS.value}/{foi_id}/members'

        r = requests.post(base_url, json=member)

        if r.status_code == 201:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error posting FOI members: {r.status_code}')

    def put_foi(self, node_api_endpoint=None, params=None, foi_id=None, foi=None):

        base_url = f'{node_api_endpoint}/{APITerms.FOIS.value}/{foi_id}'

        r = requests.put(base_url, json=foi)

        if r.status_code == 200:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error putting FOI: {r.status_code}')

    def put_foi_history_version(self, node_api_endpoint=None, params=None, foi_id=None, version=None,
                                history=None):

        base_url = f'{node_api_endpoint}/{APITerms.FOIS.value}/{foi_id}/history/{version}'

        r = requests.put(base_url, json=history)

        if r.status_code == 200:
            return r.json()
        elif not r.ok:
            raise ValueError(f'Error putting FOI history: {r.status_code}')


class DatastreamsEndpoints:
    pass
