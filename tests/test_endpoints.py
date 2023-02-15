import json

from pyconnectedservices.endpoints import system_ep, fois, datastreams, observations, tasking


def test_get_systems(t_full_url):
    response = system.get_systems(node_api_endpoint=t_full_url,
                                  params=None)
    print(response)
    assert response is not None


def test_get_system(t_full_url):
    response = system.get_system(node_api_endpoint=t_full_url,
                                 params=None,
                                 system_id='7eg2t8tntjlte')
    print(response)
    assert response is not None


def test_get_system_details(t_full_url):
    response = system.get_system_details(node_api_endpoint=t_full_url,
                                         params=None,
                                         system_id='7eg2t8tntjlte')
    print(response)
    assert response is not None


def test_get_system_datastreams(t_full_url):
    response = system.get_system_datastreams(node_api_endpoint=t_full_url,
                                             params=None,
                                             system_id='7eg2t8tntjlte')
    print(response)
    assert response is not None


def test_get_system_controls(t_full_url):
    response = system.get_system_controls(node_api_endpoint=t_full_url,
                                          params=None,
                                          system_id='7eg2t8tntjlte')
    print(response)
    assert response is not None


def test_get_system_fois(t_full_url):
    response = system.get_system_fois(node_api_endpoint=t_full_url,
                                      params=None,
                                      system_id='7eg2t8tntjlte')
    print(response)
    assert response is not None


def test_get_system_history(t_full_url):
    response = system.get_system_history(node_api_endpoint=t_full_url,
                                         params=None,
                                         system_id='7eg2t8tntjlte')
    print(response)
    assert response is not None


def test_post_system(t_full_url):
    test_system_json = {
        'type': 'Feature',
        'properties': {
            'name': 'Test System Endpoint',
            'featureType': 'https://geojson.org/schema/Feature.json',
            'uid': 'urn:osh:test:system:abc123',
        }
    }
    print(json.dumps(test_system_json, indent=4))

    response = system.post_system(node_api_endpoint=t_full_url,
                                  system=test_system_json)

    print(response.headers)
    assert response is not None


def test_post_system_contact(t_full_url):
    response = system.post_system_contact(node_api_endpoint=t_full_url,
                                          system_id='7eg2t8tntjlte',
                                          contact=None)
    print(response)
    assert response is not None


def test_post_system_events(t_full_url):
    response = system.post_system_events(node_api_endpoint=t_full_url,
                                         system_id='7eg2t8tntjlte',
                                         events=None)
    print(response)
    assert response is not None


def test_post_system_members(t_full_url):
    response = system.post_system_member(node_api_endpoint=t_full_url,
                                         system_id='7eg2t8tntjlte',
                                         member=None)
    print(response)
    assert response is not None


def test_post_system_datastream(t_full_url):
    response = system.post_system_datastream(node_api_endpoint=t_full_url,
                                             system_id='7eg2t8tntjlte',
                                             datastream=None)
    print(response)
    assert response is not None


def test_post_system_controls(t_full_url):
    response = system.post_system_controls(node_api_endpoint=t_full_url,
                                           system_id='7eg2t8tntjlte',
                                           controls=None)
    print(response)
    assert response is not None


def test_post_system_foi(t_full_url):
    test_foi = {
        'type': 'Feature',
        'properties': {
            'name': 'Test FOI Endpoint',
            'featureType': 'https://geojson.org/schema/Feature.json',
            'uid': 'urn:osh:test:foi:abc123',
        },
        # 'geometry': {
        #     'type': None
        # }
    }
    response = system.post_system_foi(node_api_endpoint=t_full_url,
                                      system_id='7eg2t8tntjlte',
                                      foi=test_foi)
    print(response)
    assert response is not None


def test_post_system_history(t_full_url):
    response = system.post_system_history(node_api_endpoint=t_full_url,
                                          system_id='7eg2t8tntjlte',
                                          history=None)
    print(response)
    assert response is not None


def test_put_system(t_full_url):
    response = system.put_system(node_api_endpoint=t_full_url,
                                 system_id='7eg2t8tntjlte',
                                 system=None)
    print(response)
    assert response is not None


def test_put_system_details(t_full_url):
    response = system.put_system_details(node_api_endpoint=t_full_url,
                                         system_id='7eg2t8tntjlte',
                                         details=None)
    print(response)
    assert response is not None


def test_put_system_history_version(t_full_url):
    response = system.put_system_history_version(node_api_endpoint=t_full_url,
                                                 system_id='7eg2t8tntjlte',
                                                 version='7eg2t8tntjlte',
                                                 history=None)
    print(response)
    assert response is not None


# Test FOI Endpoint Methods
def test_get_foi(t_full_url):
    response = fois.get_foi(node_api_endpoint=t_full_url,
                            params=None,
                            foi_id=None)
    print(response)
    assert response is not None


# Test Datastream Endpoint Methods
def test_post_datastream(t_full_url):
    test_datastream_json = {
        'outputName': 'test-datastream-endpoint',
        'name': 'Test Datastream Endpoint',
        'schema': {
            'obsFormat': "application/om+json",
            'resultSchema': {
                "name": "root",
                "type": "DataRecord",
                "label": "Root",
                "definition": "www.test.org/test/root",
                "description": "Root Component",
                "fields": [
                    {
                        "name": "test-time",
                        "type": "Time",
                        "label": "Test Time",
                        "definition": "http://www.opengis.net/def/property/OGC/0/SamplingTime",
                        "description": "Test Description",
                        "uom": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
                    },
                    {
                        "name": "test-bool",
                        "type": "Boolean",
                        "label": "Test Bool",
                        "definition": "www.test.org/test/bool",
                        "description": ""

                    },
                    {
                        "name": "test-text",
                        "type": "Text",
                        "label": "Test Text",
                        "definition": "www.test.org/test/text",
                        "description": ""
                    },
                    {
                        "name": "test-count",
                        "type": "Count",
                        "label": "Test Count",
                        "definition": "www.test.org/test/count",
                        "description": ""
                    },
                    {
                        "name": "test-category",
                        "type": "Category",
                        "label": "Test Category",
                        "definition": "www.test.org/test/category",
                        "description": ""

                    },
                    {
                        "name": "test-quantity",
                        "type": "Quantity",
                        "label": "Test Quantity",
                        "definition": "www.test.org/test/quantity",
                        "description": ""
                    }
                ]
            },
        },
        "resultEncoding": {
            "token_sep": ",",
            "block_sep": "\n",
            "decimal_sep": ".",
            "collapse_white_spaces": False
        }
    }
    response = datastreams.post_datastream(node_api_endpoint=t_full_url,
                                           system_id='7eg2t8tntjlte',
                                           datastream=test_datastream_json)
    print(response)
    assert response is not None


# Test Observation Endpoint Methods
def test_post_observation(t_full_url):
    test_obs_json = {
        "phenomenonTime": "2023-02-01T01:16:13.594295+00:00",
        "result": {
            "test-time": 1675214173594.295,
            "test-bool": True,
            "test-text": "Test Text",
            "test-count": 1,
            "test-category": "Test Category",
            "test-quantity": 1.0
        }
    }

    response = observations.post_datastream_observations(node_api_endpoint=t_full_url,
                                                         datastream_id='svrtgio9mp6iq',
                                                         observations=test_obs_json)
    print(response)
    assert response is not None


# Test Control Endpoint Methods
def test_post_control_interface(t_full_url):
    test_control = {
        "name": "Name of control output000",
        "inputName": "output000",
        "schema": {
            "commandSchema": {
                "type": "DataRecord",
                "fields": [
                    {
                        "name": "time",
                        "type": "Time",
                        "definition": "http://www.opengis.net/def/property/OGC/0/SamplingTime",
                        "referenceFrame": "http://www.opengis.net/def/trs/BIPM/0/UTC",
                        "label": "Sampling Time",
                        "uom": {
                            "href": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
                        }
                    },
                    {
                        "name": "f1",
                        "type": "Quantity",
                        "label": "Component 1",
                        "uom": {
                            "code": "Cel"
                        }
                    },
                    {
                        "name": "f2",
                        "type": "Text",
                        "label": "Component 2",
                        "constraint": {
                            "type": "AllowedTokens",
                            "pattern": "[0-9]{5-10}"
                        }
                    }
                ]
            }
        }
    }

    print(f'\n{json.dumps(test_control, indent=4)}')

    response = system.post_system_controls(node_api_endpoint=t_full_url,
                                           system_id='7eg2t8tntjlte',
                                           controls=test_control)
    print(response)


def test_post_command(t_full_url):
    test_command = {
        'executionTime': 'now',
        'params': {
            "f1": 1.0,
            "f2": "Test Text"
        }
    }
    response = tasking.post_command(node_api_endpoint=t_full_url,
                                    system_id='7eg2t8tntjlte',
                                    tasking_id='pb0qfoc8fo6nu',
                                    command=test_command)
    print(response)
