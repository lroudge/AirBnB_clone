#!/usr/bin/python3
"""Module for TestHBNBCommand class."""

from console import HBNBCommand
import unittest
from unittest.mock import patch
import sys
from io import StringIO
import re
import json
import os


class TestHBNBCommand(unittest.TestCase):
    """Tests HBNBCommand console."""

    def setUp(self):
        """Sets up test cases."""
        if os.path.isfile("file.json"):
            os.remove("file.json")

    def test_help(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help"))
        s = """
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

"""
        self.assertEqual(s, f.getvalue())

    def test_help_EOF(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
        s = "Handles End Of File character.\n"
        self.assertEqual(s, f.getvalue())

    def test_emptyline(self):
        """Tests emptyline functionality."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("\n"))
        s = ""
        self.assertEqual(s, f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("                  \n"))
        s = ""
        self.assertEqual(s, f.getvalue())

if __name__ == "__main__":
    unittest.main()
