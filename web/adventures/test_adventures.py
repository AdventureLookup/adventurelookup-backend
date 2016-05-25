from django.test import TestCase
from django.db import connection
from adventures.models import *

class URLListFieldTestCase(TestCase):

    def setUp(self):
        Adventure.objects.create(name="LMoP", links=["www.google.com", "another.website.io"])
        Adventure.objects.create(name="HotDQ")

    def test_URLListField_db_type(self):
        """Make sure that URLListField has a proper type"""
        links = URLListField()
        self.assertEqual(links.db_parameters(connection)['type'], 'text')

    def test_URLListField_from_db_value_empty_list(self):
        """Test URLListField's from_db_value with empty list"""
        adventure = Adventure.objects.get(name="HotDQ")
        self.assertEqual(adventure.links, [])

    def test_URLListField_from_db_value_with_links(self):
        """Test URLListField's from_db_value with links"""
        adventure = Adventure.objects.get(name="LMoP")
        self.assertEqual(adventure.links, ["www.google.com", "another.website.io"])

    def test_URLListField_to_python_none(self):
        """Test URLListField's to_python with none"""
        url_list = URLListField()
        self.assertEqual(url_list.to_python(None), None)

    def test_URLListField_to_python_with_links(self):
        """Test URLListField's to_python with links"""
        url_list = URLListField()
        self.assertEqual(url_list.to_python("www.google.com,another.website.io"), ["www.google.com", "another.website.io"])

    def test_URLListField_get_prep_value(self):
        """Test URLListField's to_python with none"""
        url_list = URLListField()
        self.assertEqual(url_list.get_prep_value(["www.google.com", "another.website.io"]), "www.google.com,another.website.io")
