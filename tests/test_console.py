#!/usr/bin/python3
"""Module for TestHBNBCommand class."""

from console import HBNBCommand
from unittest.mock import create_autospec
import unittest
import sys
import io
from contextlib import redirect_stdout
from models import storage
from models.base_model import BaseModel
from models.city import City
from models.user import User
from models.engine.file_storage import FileStorage
import re
import json
import os


class TestHBNBCommand(unittest.TestCase):
    """Tests HBNBCommand console."""

    attribute_values = {
        str: "foobar108",
        int: 1008,
        float: 1.08
        }

    test_random_attributes = {
        "strfoo": "barfoo",
        "intfoo": 248,
        "floatfoo": 9.8
        }

    def setUp(self):
        """Sets up test cases."""
        self.mock_stdin = create_autospec(sys.stdin)
        self.mock_stdout = create_autospec(sys.stdout)
        self.resetStorage()

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

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
        return "".join([c[0][0]
                        for c in self.mock_stdout.write.
                        call_args_list[-lines:]])

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

    def test_do_create_error(self):
        """Tests create command with errors."""
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("create"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("create garbage"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def help_test_dict(self, obj, rep):
        """Helper method to test dictionary equality."""
        rex = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        res = rex.match(rep)
        self.assertIsNotNone(res)
        self.assertEqual(res.group(1), type(obj).__name__)
        self.assertEqual(res.group(2), obj.id)
        s = res.group(3)
        s = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", s)
        d = json.loads(s.replace("'", '"'))
        d2 = obj.__dict__.copy()
        d2["created_at"] = repr(d2["created_at"])
        d2["updated_at"] = repr(d2["updated_at"])
        self.assertEqual(d, d2)

    def test_do_show(self):
        """Tests show command."""
        o = BaseModel()
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("show BaseModel " + o.id))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        self.help_test_dict(o, s)

    def test_do_show_error(self):
        """Tests show command with errors."""
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("show"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("show garbage"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("show BaseModel"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("show BaseModel 6524359"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def test_show_advanced(self):
        """Tests .show() command."""
        o = BaseModel()
        o.save()
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd("BaseModel.show(" + o.id + ")"))
        # Might work on our code but not on the one the checker uses -> put
        # onecmd back ?
        s = f.getvalue()
        self.assertTrue(len(s) > 0)
        self.help_test_dict(o, s)

    def test_do_destroy(self):
        """Tests destroy command."""
        o = BaseModel()
        key = self.key(o)
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("destroy BaseModel " + o.id))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) == 0)
        self.assertFalse(key in storage.all())

    def test_do_destroy_error(self):
        """Tests destroy command with errors."""
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("destroy"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("destroy garbage"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("destroy BaseModel"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("destroy BaseModel 6524359"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def test_destroy_advanced(self):
        """Tests .destroy() command."""
        o = BaseModel()
        o.save()
        key = self.key(o)
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd("BaseModel.destroy(" + o.id + ")"))
        # Might work on our code but not on the one the checker uses -> put
        # onecmd back ?
        s = f.getvalue()
        self.assertTrue(len(s) == 0)
        self.assertFalse(key in storage.all())

    def test_do_all(self):
        """Tests the all command."""
        o = BaseModel()
        c = City()
        u = User()
        o.save()
        c.save()
        u.save()
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("all"))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        l = json.loads(s)
        self.assertEqual(l, [str(v) for k, v in storage.all().items()])

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("all City"))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        l = json.loads(s)
        self.assertEqual(
            l, [str(v) for k, v in storage.all().items()
                if type(v).__name__ == "City"])

    def test_do_all_error(self):
        """Tests all command with errors."""
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("all garbage"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def test_all_advanced(self):
        """Tests .all() command."""
        o = BaseModel()
        c = City()
        o.save()
        c.save()
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd("City.all()"))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        l = json.loads(s)
        self.assertEqual(
            l, [str(v) for k, v in storage.all().items()
                if type(v).__name__ == "City"])

    def test_count_advanced(self):
        """Tests .count() command."""
        o = BaseModel()
        c = BaseModel()
        o.save()
        c.save()
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd("BaseModel.count()"))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        self.assertEqual(s, "2")

    def test_do_count_error(self):
        """Tests .count() command with errors."""
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd("garbage.count()"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd(".count()"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

    def test_update_everything(self):
        """Tests update command with errthang, like a baws."""
        cli = self.create()
        for classname, cls in storage.classes().items():
            obj = cls()
            obj.save()
            for attr, value in self.test_random_attributes.items():
                quotes = (attr == "str")
                self.help_test_update(obj, attr, value, cli, quotes, False)
                self.help_test_update(obj, attr, value, cli, quotes, True)
            if classname == "BaseModel":
                continue
            for attr, attr_type in storage.attributes()[classname].items():
                if attr_type not in (str, int, float):
                    continue
                self.help_test_update(obj, attr,
                                      self.attribute_values[attr_type],
                                      cli, True, False)
                self.help_test_update(obj, attr,
                                      self.attribute_values[attr_type],
                                      cli, True, True)

    def help_test_update(self, obj, attr, val, cli, quotes, func):
        """Tests update commmand."""
        f = io.StringIO()
        value_str = ('"{}"' if quotes else '{}').format(val)
        if func:
            cmd = '{}.update({}, {}, {})'
        else:
            cmd = 'update {} {} {} {}'
        cmd = cmd.format(type(obj).__name__, obj.id, attr, value_str)
        print("TESTING:", cmd)
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd(cmd))
        msg = f.getvalue()[:-1]
        self.assertEqual(len(msg), 0)
        self.assertEqual(getattr(obj, attr, None), val)
