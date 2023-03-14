import pyswapi.comm.comm_mqtt as mqtt
import paho.mqtt.client as mqtt_ph


def test_mqtt_client():
    tclient = mqtt_ph.Client()
    # tclient.username_pw_set('uxs-team', 'WR6zlso9h#')
    tclient.on_message = mqtt.on_message
    tclient.on_connect = mqtt.on_connect
    tclient.on_publish = mqtt.on_publish
    tclient.on_subscribe = mqtt.on_subscribe
    tclient.connect('192.168.56.101', port=8181)
    # tclient.connect('api.georobotix.io/ogc/t18', port=443)
    # tclient.subscribe('/api/datastreams/lqvvhsmeo0h0e/observations', 1)
    # tclient.subscribe('api/datastreams/rbnag2hrc04mm/observations', 1)
    tclient.subscribe('#', 0)
    while True:
        tclient.loop(1)


def test_publish_obs_mqtt():
    tclient = mqtt_ph.Client()
    tclient.on_message = mqtt.on_message
    tclient.on_connect = mqtt.on_connect
    tclient.on_publish = mqtt.on_publish
    tclient.on_subscribe = mqtt.on_subscribe

    # TODO: Add Method to Datastream to take an MQTT Client and publish an Observation
    # Datastream -> MQTTClient
    # Datastream -> Publish Earliest Observation
