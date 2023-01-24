from enum import Enum


class APITerms(Enum):
    API = 'api'
    SYSTEMS = 'systems'
    DATASTREAMS = 'datastreams'
    OBSERVATIONS = 'observations'


class SystemTypes(Enum):
    FEATURE = "Feature"


class ObservationFormat(Enum):
    JSON = "application/om+json"
    XML = "application/om+xml"
    SWE_XML = "application/swe+xml"
    SWE_JSON = "application/swe+json"
    SWE_CSV = "application/swe+csv"
    SWE_BINARY = "application/swe+binary"
