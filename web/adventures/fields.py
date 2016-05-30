from django.db import models

def parse_URL_list_field(url_list, separator):
    """Takes a string of urls and coverts them into a list."""
    if url_list == "":
        return []
    return url_list.split(",")

class URLListField(models.URLField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list of URLs"

    def __init__(self, *args, **kwargs):
        self.separator = ","
        super(URLListField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(URLListField, self).deconstruct()
        return name, path, args, kwargs

    def db_type(self, connection):
        return 'text'

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return parse_URL_list_field(value, self.separator)

    def to_python(self, value):
        if value is None:
            return value
        return parse_URL_list_field(value, self.separator)

    def get_prep_value(self, value):
        return self.separator.join(value)
