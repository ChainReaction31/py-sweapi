import requests

from pyconnectedservices.constants import APITerms


def get_observations(self, node_api_endpoint=None, params=None, observation_id=None):
    """
    List all observations or get a specific observation if an observation_id is provided
    :param self:
    :param node_api_endpoint:
    :param params:
    :param observation_id:
    :return:
    """

    base_url = f'{node_api_endpoint}/{APITerms.OBSERVATIONS.value}'

    if observation_id is not None:
        base_url += f'/{observation_id}'

    r = requests.get(base_url, params=params)

    if r.status_code == 200:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error getting observations: {r.status_code}')


def get_datastream_observations(node_api_endpoint=None, params=None, datastream_id=None):
    """
    List all observations for a specific datastream
    :param node_api_endpoint:
    :param params:
    :param datastream_id:
    :return:
    """
    base_url = f'{node_api_endpoint}/{APITerms.OBSERVATIONS.value}/{APITerms.DATASTREAMS.value}/{datastream_id}'

    r = requests.get(base_url, params=params)

    if r.status_code == 200:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error getting datastream observations: {r.status_code}')


def post_datastream_observations(node_api_endpoint=None, datastream_id=None, observations=None):
    """
    Post observations for a specific datastream. Can be either a single observation or an array of observations
    :param node_api_endpoint:
    :param datastream_id:
    :param observations:
    :return:
    """
    base_url = f'{node_api_endpoint}/{APITerms.OBSERVATIONS.value}/{APITerms.DATASTREAMS.value}/{datastream_id}'

    r = requests.post(base_url, json=observations)

    if r.status_code == 200:
        return r.json()
    elif not r.ok:
        raise ValueError(f'Error posting datastream observations: {r.status_code}')
