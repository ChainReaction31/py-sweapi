from pyconnectedservices.endpoints import system, fois, datastreams, observations, tasking


def test_get_systems(t_full_url):
    response_json = system.get_systems(node_api_endpoint=t_full_url,
                                       params=None)
    print(response_json)
    assert response_json is not None


def test_get_system(t_full_url):
    response_json = system.get_system(node_api_endpoint=t_full_url,
                                      params=None,
                                      system_id='7eg2t8tntjlte')
    print(response_json)
    assert response_json is not None


def test_get_system_details(t_full_url):
    response_json = system.get_system_details(node_api_endpoint=t_full_url,
                                              params=None,
                                              system_id='7eg2t8tntjlte')
    print(response_json)
    assert response_json is not None


def test_get_system_datastreams(t_full_url):
    response_json = system.get_system_datastreams(node_api_endpoint=t_full_url,
                                                  params=None,
                                                  system_id='7eg2t8tntjlte')
    print(response_json)
    assert response_json is not None


def test_get_system_controls(t_full_url):
    response_json = system.get_system_controls(node_api_endpoint=t_full_url,
                                               params=None,
                                               system_id='7eg2t8tntjlte')
    print(response_json)
    assert response_json is not None


def test_get_system_fois(t_full_url):
    response_json = system.get_system_fois(node_api_endpoint=t_full_url,
                                           params=None,
                                           system_id='7eg2t8tntjlte')
    print(response_json)
    assert response_json is not None


def test_get_system_history(t_full_url):
    response_json = system.get_system_history(node_api_endpoint=t_full_url,
                                              params=None,
                                              system_id='7eg2t8tntjlte')
    print(response_json)
    assert response_json is not None


def test_post_system(t_full_url):
    response_json = system.post_system(node_api_endpoint=t_full_url,
                                       system=None)
    print(response_json)
    assert response_json is not None


def test_post_system_contact(t_full_url):
    response_json = system.post_system_contact(node_api_endpoint=t_full_url,
                                               system_id='7eg2t8tntjlte',
                                               contact=None)
    print(response_json)
    assert response_json is not None


def test_post_system_events(t_full_url):
    response_json = system.post_system_events(node_api_endpoint=t_full_url,
                                              system_id='7eg2t8tntjlte',
                                              events=None)
    print(response_json)
    assert response_json is not None


def test_post_system_members(t_full_url):
    response_json = system.post_system_member(node_api_endpoint=t_full_url,
                                              system_id='7eg2t8tntjlte',
                                              member=None)
    print(response_json)
    assert response_json is not None


def test_post_system_datastream(t_full_url):
    response_json = system.post_system_datastream(node_api_endpoint=t_full_url,
                                                  system_id='7eg2t8tntjlte',
                                                  datastream=None)
    print(response_json)
    assert response_json is not None


def test_post_system_controls(t_full_url):
    response_json = system.post_system_controls(node_api_endpoint=t_full_url,
                                                system_id='7eg2t8tntjlte',
                                                controls=None)
    print(response_json)
    assert response_json is not None


def test_post_system_foi(t_full_url):
    response_json = system.post_system_foi(node_api_endpoint=t_full_url,
                                           system_id='7eg2t8tntjlte',
                                           foi=None)
    print(response_json)
    assert response_json is not None


def test_post_system_history(t_full_url):
    response_json = system.post_system_history(node_api_endpoint=t_full_url,
                                               system_id='7eg2t8tntjlte',
                                               history=None)
    print(response_json)
    assert response_json is not None


def test_put_system(t_full_url):
    response_json = system.put_system(node_api_endpoint=t_full_url,
                                      system_id='7eg2t8tntjlte',
                                      system=None)
    print(response_json)
    assert response_json is not None


def test_put_system_details(t_full_url):
    response_json = system.put_system_details(node_api_endpoint=t_full_url,
                                              system_id='7eg2t8tntjlte',
                                              details=None)
    print(response_json)
    assert response_json is not None


def test_put_system_history_version(t_full_url):
    response_json = system.put_system_history_version(node_api_endpoint=t_full_url,
                                                      system_id='7eg2t8tntjlte',
                                                      version='7eg2t8tntjlte',
                                                      history=None)
    print(response_json)
    assert response_json is not None


# Test FOI Endpoint Methods
def test_get_foi(t_full_url):
    response_json = fois.get_foi(node_api_endpoint=t_full_url,
                                 params=None,
                                 foi_id=None)
    print(response_json)
    assert response_json is not None
