#!/usr/bin/python3
"""Module for TestHBNBCommand class."""

from console import HBNBCommand
from unittest.mock import create_autospec
import unittest
import sys
import io
from contextlib import redirect_stdout
from models import storage

class TestHBNBCommand(unittest.TestCase):
    """Tests HBNBCommand console."""

    def setUp(self):
        """Sets up test cases."""
        self.mock_stdin = create_autospec(sys.stdin)
        self.mock_stdout = create_autospec(sys.stdout)

    def create(self):
        """Creates new instance of console."""
        return HBNBCommand(stdin=self.mock_stdin, stdout=self.mock_stdout)

    def key(self, obj):
        """Returns dict key of this obj."""
        return "{}.{}".format(type(obj).__name__, obj.id)

    def last_write(self, lines=None):
        """Returns that last <lines> of written to stdout."""
        if not lines:
            return self.mock_stdout.write.call_args[0][0]
        return "".join([c[0][0] for c in self.mock_stdout.write.call_args_list[-lines:]])

    def test_help(self):
        """Tests the help command."""
        cli = self.create()
        self.assertFalse(cli.onecmd("help"))
        self.mock_stdout.flush()
        self.assertTrue(self.mock_stdout.flush.called)
        s = """\
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

"""
        self.assertEqual(s, self.last_write(4))

    def test_help_EOF(self):
        """Tests the help command."""
        cli = self.create()
        self.assertFalse(cli.onecmd("help EOF"))
        self.mock_stdout.flush()
        self.assertTrue(self.mock_stdout.flush.called)
        s = "*** No help on EOF\n"
        self.assertNotEqual(s, self.last_write(1))

    def test_emptyline(self):
        """Tests emptyline functionality."""
        cli = self.create()
        self.assertFalse(cli.onecmd("\n"))
        self.mock_stdout.flush()
        self.assertTrue(self.mock_stdout.flush.called)
        s = ""
        self.assertEqual(s, self.last_write(1))

        self.assertFalse(cli.onecmd("                  \n"))
        self.mock_stdout.flush()
        self.assertTrue(self.mock_stdout.flush.called)
        s = ""
        self.assertEqual(s, self.last_write(1))

    def test_do_create_user(self):
        """Tests create commmand."""
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("create User"))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)
        key = "User." + uid
        self.assertTrue(key in storage.all())

    def test_do_create_noclass(self):
        """Tests create command without class argument."""
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("create"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

    def test_do_create_wrong_class(self):
        """Tests create command with nonexisting class."""
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("create garbage"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")
