"""
The utilities module contains various useful functions that are used around the library
"""
from oshdatacore.component_implementations import TimeComponent, BooleanComponent, TextComponent, CategoryComponent, \
    CountComponent, QuantityComponent, DataRecordComponent


def datarecord_from_json(json_data: dict) -> DataRecordComponent:
    """
    Creates a DataRecord object from a json dictionary

    :param json_data: The json dictionary (converted from JSON)
    :return: The DataRecord object
    """
    ds_root = DataRecordComponent(description=json_data['description'],
                                  label=json_data['label'],
                                  name=json_data['label'],
                                  definition='',
                                  fields=list(map(datarecord_field_builder, json_data['fields'])))
    return ds_root


def datarecord_field_builder(field_dict: dict):
    """
    Builds the fields in a DataRecordComponent from a dictionary (usually retrieved via an API call)
    :param field_dict: usually some variant of `json_data['resultSchema']['fields']`
    :return:
    """
    match field_dict['type']:
        case 'Time':
            return TimeComponent(name=field_dict['name'], label=field_dict['label'],
                                 description='', definition='')
        case 'Boolean':
            return BooleanComponent(name=field_dict['name'], label=field_dict['label'],
                                    description='', definition='')
        case 'Text':
            return TextComponent(name=field_dict['name'], label=field_dict['label'],
                                 description='', definition='')
        case 'Category':
            return CategoryComponent(name=field_dict['name'], label=field_dict['label'],
                                     description='', definition='')
        case 'Count':
            return CountComponent(name=field_dict['name'], label=field_dict['label'],
                                  description='', definition='')
        case 'Quantity':
            return QuantityComponent(name=field_dict['name'], label=field_dict['label'],
                                     description='', definition='',
                                     uom=field_dict['uom']['href'])
        case 'DataRecord':
            return DataRecordComponent(name=field_dict['name'], label=field_dict['label'],
                                       description='', definition='',
                                       fields=list(map(datarecord_field_builder, field_dict['fields'])))
