import json
from django.test import TestCase, Client
from django.db import connection
from adventures.models import *
from adventures.fields import *

class AdventureTestCase(TestCase):

    def test_Adventure_str(self):
        """Adventure str returns the name"""
        adventure = Adventure(name="LMoP")
        self.assertEqual(adventure.__str__(), "LMoP")

class AuthorTestCase(TestCase):

    def test_Author_str(self):
        """Author str returns the name"""
        author = Author(name="WotC")
        self.assertEqual(author.__str__(), "WotC")

class URLListFieldTestCase(TestCase):

    def setUp(self):
        Adventure.objects.create(name="LMoP", links=["www.google.com", "another.website.io"])
        Adventure.objects.create(name="HotDQ")

    def test_URLListField_db_type(self):
        """Make sure that URLListField has a proper type"""
        links = URLListField()
        self.assertEqual(links.db_parameters(connection)['type'], 'text')

    def test_URLListField_from_db_value_none(self):
        """Test URLListField's from_db_value none"""
        url_list = URLListField()
        self.assertEqual(url_list.from_db_value(None, None, None, None), None)

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


class AdventureByIdTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.test_adv = Adventure.objects.create(name="LMoP", links=["www.google.com", "another.website.io"])

    def test_adventure_by_id_get_success(self):
        lmop = self.client.get('/adventures/adventure/{}'.format(self.test_adv.id))
        actual_data = json.loads(lmop.content.decode('utf-8'))
        correct_data = {'name': 'LMoP',
                        'id': 1,
                        'links': ["www.google.com", "another.website.io"],
                        'authors': [],
                        'description': ''
                        }
        self.assertEqual(actual_data, correct_data)

    def test_adventure_by_id_get_404(self):
        notfound = self.client.get('/adventures/adventure/15')
        self.assertEqual(notfound.status_code, 404)

    def test_adventure_by_id_get_400(self):
        invalid = self.client.get('/adventures/adventure/notaninteger')
        self.assertEqual(invalid.status_code, 400)

    def test_adventure_by_id_get_put(self):
        put = self.client.put('/adventures/adventure/1')
        self.assertEqual(put.status_code, 405)
