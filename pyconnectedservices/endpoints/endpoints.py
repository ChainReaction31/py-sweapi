from enum import Enum

import requests

from pyconnectedservices.constants import APITerms


class SystemQueryParams(Enum):
    Keywords = 'q'
    """
    A comma-separated list of keywords to search for in the system name, description, and definition.
    """
    BBOX = 'bbox'
    """
    BBOX to fileter resources based on their location
    """
    LOCATION = 'location'
    """
    WKT geometry to filter resources based on their location or geometry
    """
    VALID_TIME = 'validTime'
    """
    ISO 8601 time interval to filter resources based on their valid time. When omitted, the implicit time is "now"
    except for "history" collection where no filtering is applied.
    """
    PARENT = 'parent'
    """
    Comma-separated list of parent system IDs or "*" to included nested resources at any level
    """
    SELECT = 'select'
    """
    Comma-separated list of properties to include or exclude from results (use "!" prefix to exclude)
    """
    FORMAT = 'format'
    """
    Mime type of the response format.
    """
    LIMIT = 'limit'
    """
    Maximum number of resources to return per page (max 1000)
    """
    OFFSET = 'offset'
    """
    Token specifying the page to return (usually the token provided in the previous call)
    """

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

















