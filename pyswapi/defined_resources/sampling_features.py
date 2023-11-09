from pyswapi.defined_resources.features import Feature
from pyswapi.defined_resources.properties import Property
from pyswapi.system import System


class SamplingFeature:
    unique_id = None
    name = None
    description = None
    feature_type = None
    valid_time = None
    parent_system: System = None
    feature_of_interest: Feature = None
    observed_properties: list[Property] = None
    controlled_properties: list[Property] = None
    spatial_sampling_feature: SpatialSamplingFeature = None