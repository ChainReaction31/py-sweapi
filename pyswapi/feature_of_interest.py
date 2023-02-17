from dataclasses import dataclass


@dataclass(kw_only=True)
class FeatureOfInterest:
    type: str
    featureType: str
    uid: str
    name: str
    description: str

