import unittest

import boto
import yaml

from janitor import policy, actions, filters

from janitor.tests.common import BaseTest


class TestPolicy(BaseTest):

    def test_file_not_found(self):
        self.assertRaises(
            ValueError, policy.load, {}, "/asdf12")

    def test_filters(self):
        p = self.load_policy({'filters': [
            {'state': 'absent',
             'filter': 'tag:ASV'},
            {'filter': 'tag-key',
             'value': 'CMDBEnvironment'}
        ]})
        self.assertTrue(
            isinstance(p.filters[0], filters.EC2InstanceFilter))
        self.assertTrue(
            isinstance(p.filters[1], filters.EC2QueryFilter))        
        self.assertEqual(
            p.filters[0].data, {'filter': 'tag:ASV', 'state': 'absent'})

    def test_actions(self):
        # a simple action by string
        p = self.load_policy({'actions': ['mark']})
        self.assertEqual(len(p.actions), 1)
        self.assertTrue(isinstance(p.actions[0], actions.Mark))

        # a configured action with dict
        p = self.load_policy({'actions': [
            {'type': 'mark',
             'msg': 'Missing proper tags'}]})
        self.assertEqual(len(p.actions), 1)
        self.assertTrue(isinstance(p.actions[0], actions.Mark))
        self.assertEqual(p.actions[0].data,
                         {'msg': 'Missing proper tags', 'type': 'mark'})
        

