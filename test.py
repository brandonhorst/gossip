#!/usr/bin/env python3

import gossip
import json
import unittest

class TestGossip(unittest.TestCase):

    def test_simple_cycle(self):
        simple_cycle = [{
            "talker": "a",
            "listener": "b",
            "time": 1
        }, {
            "talker": "b",
            "listener": "c",
            "time": 2
        }, {
            "talker": "c",
            "listener": "a",
            "time": 4
        }]
        school = gossip.School(simple_cycle)

        self.assertEqual(school.search("a", "a"), 0)
        self.assertEqual(school.search("a", "b"), 1)
        self.assertEqual(school.search("a", "c"), 3)
        self.assertEqual(school.search("c", "b"), 5)

        with self.assertRaises(ValueError):
            school.search("a", "d")
        with self.assertRaises(ValueError):
            school.search("d", "a")

    def test_broken_graph(self):
        broken_graph = [{
            "talker": "a",
            "listener": "b",
            "time": 1
        }, {
            "talker": "b",
            "listener": "a",
            "time": 2
        }, {
            "talker": "c",
            "listener": "d",
            "time": 4
        }, {
            "talker": "d",
            "listener": "c",
            "time": 8
        }]

        school = gossip.School(broken_graph)

        self.assertEqual(school.search("a", "b"), 1)
        self.assertEqual(school.search("c", "d"), 4)

        with self.assertRaises(RuntimeError):
            school.search("a", "c")
        with self.assertRaises(RuntimeError):
            school.search("d", "b")

if __name__ == '__main__':
    unittest.main()