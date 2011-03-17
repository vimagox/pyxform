"""
Testing simple cases for Xls2Json
"""
import sys, os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.test import TestCase, Client
from pyxform.xls2json import ExcelReader

class BasicXls2JsonApiTests(TestCase):

    def test_simple_yes_or_no_question(self):
        x = ExcelReader("pyxform/tests/yes_or_no_question.xls")
        x_results = x.to_dict()
        
        expected_dict = [
            {
                u'label': {u'english': u'have you had a good day today?'},
                u'type': u'select one',
                u'name': u'good_day',
                u'choices': [
                    {
                        u'label': {u'english': u'yes'},
                        u'value': u'yes'
                        },
                    {
                        u'label': {u'english': u'no'},
                        u'value': u'no'
                        }
                    ]
                }
            ]
        self.assertEqual(x_results[u"children"], expected_dict)


    def test_gps(self):
        x = ExcelReader("pyxform/tests/gps.xls")

        expected_dict = [{u'type': u'gps', u'name': u'location'}]

        self.assertEqual(x.to_dict()[u"children"], expected_dict)

    
    def test_string_and_integer(self):
        x = ExcelReader("pyxform/tests/string_and_integer.xls")

        expected_dict = [{u'text': {u'english': u'What is your name?'}, u'type': u'string', u'name': u'your_name'}, {u'text': {u'english': u'How many years old are you?'}, u'type': u'integer', u'name': u'your_age'}]

        self.assertEqual(x.to_dict()[u"children"], expected_dict)

    def test_table(self):
        x = ExcelReader("pyxform/tests/simple_loop.xls")

        expected_dict = {
            u'type': u'survey',
            u'name': 'simple_loop',
            u'children': [
                {
                    u'children': [
                        {
                            u'type': u'integer',
                            u'name': u'count',
                            u'label': {u'English': u'How many are there in this group?'}
                            }
                        ],
                    u'type': u'loop',
                    u'name': u'my_table',
                    u'columns': [
                        {
                            u'name': u'col1',
                            u'label': {u'English': u'Column 1'}
                            },
                        {
                            u'name': u'col2',
                            u'label': {u'English': u'Column 2'}
                            }
                        ],
                    u'label': {u'English': u'My Table'}
                    }]}

        self.assertEqual(x.to_dict(), expected_dict)