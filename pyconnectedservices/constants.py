from enum import Enum


class APITerms(Enum):
    API = '/api'
    SYSTEMS = '/systems'
    DATASTREAMS = '/datastreams'
    OBSERVATIONS = '/observations'


class SystemTypes(Enum):
    FEATURE = "Feature"
