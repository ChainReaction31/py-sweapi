"""Outputs are a collection of datamodel types"""
from oshdatacore.component_implementations import TimeComponent, DataRecordComponent


class Output:
    """
    The base output is simply a DataRecord with a timestamp component.
    """
    root_component: DataRecordComponent

    def __init__(self, name, label, definition, description=None):
        self.root_component = DataRecordComponent(name, label, definition, description)

    def get_fields(self):
        return self.root_component.get_fields()

