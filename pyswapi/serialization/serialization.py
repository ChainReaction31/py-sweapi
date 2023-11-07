from abc import ABC, abstractmethod


class Serializer(ABC):
    @abstractmethod
    def serialize(self, some_object):
class JSONSerializer:
    """
    For the serialization and deserialization of API objects
    """

class GeoJSONSerializer:
    """
    For the serialization of GeoJSON formatted objects
    """
