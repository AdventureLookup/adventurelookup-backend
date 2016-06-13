import json

from django.core.urlresolvers import reverse
from django.db import connection
from django.test import Client, TestCase

from .fields import *
from .models import *


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
        Adventure.objects.create(
            name="LMoP",
            links=["www.google.com", "another.website.io"])
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
        self.assertEqual(adventure.links,
                         ["www.google.com", "another.website.io"])

    def test_URLListField_to_python_none(self):
        """Test URLListField's to_python with none"""
        url_list = URLListField()
        self.assertEqual(url_list.to_python(None), None)

    def test_URLListField_to_python_with_links(self):
        """Test URLListField's to_python with links"""
        url_list = URLListField()
        self.assertEqual(
            url_list.to_python("www.google.com,another.website.io"),
            ["www.google.com", "another.website.io"])

    def test_URLListField_get_prep_value(self):
        """Test URLListField's to_python with none"""
        url_list = URLListField()
        self.assertEqual(
            url_list.get_prep_value(["www.google.com", "another.website.io"]),
            "www.google.com,another.website.io")


class AdventureByIdTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.test_data = {'name': 'LMoP',
                         'links': ["www.google.com", "another.website.io"]}
        cls.test_adv = Adventure.objects.create(**cls.test_data)
        cls.put_test_data = {'name': 'Rage of Demons', 'description': 'test'}

    def test_adventure_by_id_get_success(self):
        lmop = self.client.get(reverse('adventures:adventure-by-id',
                                       args=(self.test_adv.id, )))
        actual_data = json.loads(lmop.content.decode('utf-8'))
        self.assertEqual(actual_data['name'], self.test_adv.name)
        self.assertEqual(actual_data['id'], self.test_adv.id)
        self.assertEqual(actual_data['links'], self.test_adv.links)
        self.assertEqual(actual_data['authors'], [])
        self.assertEqual(actual_data['description'], self.test_adv.description)

    def test_adventure_by_id_get_404(self):
        notfound = self.client.get(reverse('adventures:adventure-by-id',
                                           args=(100, )))
        self.assertEqual(notfound.status_code, 404)

    def test_adventure_by_id_put_success(self):
        self.client.put(reverse('adventures:adventure-by-id', args=(self.test_adv.id, )),
                        data=json.dumps(self.put_test_data), content_type='application/json')
        get = self.client.get(reverse('adventures:adventure-by-id', args=(self.test_adv.id, )))
        get_data = json.loads(get.content.decode('utf-8'))
        self.assertEqual(get_data['name'], self.put_test_data['name'])
        self.assertEqual(get_data['id'], self.test_adv.id)
        self.assertEqual(get_data['links'], self.test_adv.links)
        self.assertEqual(get_data['authors'], [])
        self.assertEqual(get_data['description'], self.put_test_data['description'])

    def test_adventure_by_id_put_404(self):
        put = self.client.put(reverse('adventures:adventure-by-id', args=(self.test_adv.id+1, )),
                              data=json.dumps(self.put_test_data), content_type='application/json')
        self.assertEqual(put.status_code, 404)

