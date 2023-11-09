from abc import ABC


class Feature(ABC):
    """
    A feature is defined as "an abstraction of real-world phenomena".
    """
    # TODO: Define basic feature here
    id: str
    unique_id:str = None
    feature_type:str = None
    geometry: geometry
    has_custom_geom_property
    valid_time = None
    has_custom_time_property
    properties = None

    def get_id(self):
        return self.id

    def get_unique_id(self):
        return self.unique_id

    def get_feature_type(self):
        return self.feature_type

    def get_geometry(self):
        return self.geometry

    def has_custom_geom_property(self):
        return self.has_custom_geom_property

    def get_valid_time(self):
        return self.valid_time

    def has_custom_time_property(self):
        return self.has_custom_time_property

    def get_properties(self):
        return self.properties