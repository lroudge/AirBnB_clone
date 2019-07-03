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

    reset_values = {
        str: "",
        int: 0,
        float: 0.0
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

    def dont_test_help(self):
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

    def dont_test_help_EOF(self):
        """Tests the help command."""
        cli = self.create()
        self.assertFalse(cli.onecmd("help EOF"))
        self.mock_stdout.flush()
        self.assertTrue(self.mock_stdout.flush.called)
        s = "*** No help on EOF\n"
        self.assertNotEqual(s, self.last_write(1))

    def dont_test_emptyline(self):
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

    def test_do_create(self):
        """Tests create for all classes."""
        for classname in storage.classes():
            self.help_test_do_create(classname)

    def help_test_do_create(self, classname):
        """Helper method to test the create commmand."""
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("create {}".format(classname)))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)
        key = "{}.{}".format(classname, uid)
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
        """Tests show for all classes."""
        for classname in storage.classes():
            self.help_test_do_show(classname)
            self.help_test_show_advanced(classname)

    def help_test_do_show(self, classname):
        """Helps test the show command."""
        o = storage.classes()[classname]()
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("show {} {}".format(classname, o.id)))
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

    def help_test_show_advanced(self, classname):
        """Helps test .show() command."""
        o = storage.classes()[classname]()
        o.save()
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(
                cli.precmd(
                    '{}.show("{}")'.format(
                        classname,
                        o.id)))
        s = f.getvalue()
        self.assertTrue(len(s) > 0)
        self.help_test_dict(o, s)

    def test_do_show_error_advanced(self):
        """Tests show() command with errors."""
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd(".show()"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd("garbage.show()"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd("BaseModel.show()"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd('BaseModel.show("6524359")'))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def test_do_destroy(self):
        """Tests destroy for all classes."""
        for classname in storage.classes():
            self.help_test_do_destroy(classname)
            self.help_test_destroy_advanced(classname)

    def help_test_do_destroy(self, classname):
        """Helps test the destroy command."""
        o = storage.classes()[classname]()
        key = self.key(o)
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(
                cli.onecmd(
                    "destroy {} {}".format(
                        classname,
                        o.id)))
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

    def help_test_destroy_advanced(self, classname):
        """Helps test the .destroy() command."""
        o = storage.classes()[classname]()
        o.save()
        key = self.key(o)
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(
                cli.precmd(
                    '{}.destroy("{}")'.format(
                        classname, o.id)))
        s = f.getvalue()
        self.assertTrue(len(s) == 0)
        self.assertFalse(key in storage.all())

    def test_do_destroy_error_advanced(self):
        """Tests destroy() command with errors."""
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd(".destroy()"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd("garbage.destroy()"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd("BaseModel.destroy()"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd('BaseModel.destroy("6524359")'))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def test_do_all(self):
        """Tests all for all classes."""
        for classname in storage.classes():
            self.help_test_do_all(classname)
            self.help_test_all_advanced(classname)

    def help_test_do_all(self, classname):
        """Helps test the all command."""
        o = storage.classes()[classname]()
        c = City()
        d = User()
        o.save()
        c.save()
        d.save()
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
            self.assertFalse(cli.onecmd("all {}".format(classname)))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        l = json.loads(s)
        self.assertEqual(
            l, [str(v) for k, v in storage.all().items()
                if type(v).__name__ == classname])

    def test_do_all_error(self):
        """Tests all command with errors."""
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("all garbage"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def help_test_all_advanced(self, classname):
        """Helps test the .all() command."""
        o = storage.classes()[classname]()
        c = City()
        o.save()
        c.save()
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd("{}.all()".format(classname)))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        l = json.loads(s)
        self.assertEqual(
            l, [str(v) for k, v in storage.all().items()
                if type(v).__name__ == classname])

    def test_do_all_error_advanced(self):
        """Tests all() command with errors."""
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd("garbage.all()"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def test_count_all(self):
        """Tests count for all classes."""
        for classname in storage.classes():
            self.help_test_count_advanced(classname)

    def help_test_count_advanced(self, classname):
        """Helps test .count() command."""
        for i in range(20):
            c = storage.classes()[classname]()
            c.save()
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd("{}.count()".format(classname)))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        self.assertEqual(s, "20")

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
                """
                if type(value) is not str:
                    continue
                """
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
                                      cli, False, True)

    def help_test_update(self, obj, attr, val, cli, quotes, func):
        """Tests update commmand."""
        f = io.StringIO()
        value_str = ('"{}"' if quotes else '{}').format(val)
        if func:
            cmd = '{}.update("{}", "{}", {})'
        else:
            cmd = 'update {} {} {} {}'
        cmd = cmd.format(type(obj).__name__, obj.id, attr, value_str)
        # print("TESTING:", cmd)
        with redirect_stdout(f):
            if func:
                self.assertFalse(cli.precmd(cmd))
            else:
                self.assertFalse(cli.onecmd(cmd))
        msg = f.getvalue()[:-1]
        self.assertEqual(len(msg), 0)
        self.assertEqual(getattr(obj, attr, None), val)
        setattr(obj, attr, self.reset_values[type(attr)])

    def test_do_update_error(self):
        """Tests update command with errors."""
        cli = self.create()
        b = BaseModel()
        b.save()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("update"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("update garbage"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("update BaseModel"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd("update BaseModel 6534276893"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.onecmd('update BaseModel {}'.format(b.id)))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** attribute name missing **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(
                cli.onecmd(
                    'update BaseModel {} name'.format(
                        b.id)))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** value missing **")

    def test_do_update_error_advanced(self):
        """Tests update() command with errors."""
        cli = self.create()
        b = BaseModel()
        b.save()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd(".update()"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd("garbage.update()"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd("BaseModel.update()"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd("BaseModel.update(6534276893)"))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(cli.precmd('BaseModel.update("{}")'.format(b.id)))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** attribute name missing **")

        f = io.StringIO()
        with redirect_stdout(f):
            self.assertFalse(
                cli.precmd(
                    'BaseModel.update("{}", "name")'.format(
                        b.id)))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** value missing **")

    def dont_test_do_quit(self):
        """Tests quit commmand."""
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertTrue(cli.onecmd("quit"))
        self.mock_stdout.flush()
        msg = f.getvalue()
        self.assertTrue(len(msg) == 0)
        self.assertEqual("", msg)
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertTrue(cli.onecmd("quit garbage"))
        self.mock_stdout.flush()
        msg = f.getvalue()
        self.assertTrue(len(msg) == 0)
        self.assertEqual("", msg)

    def dont_test_do_EOF(self):
        """Tests EOF commmand."""
        cli = self.create()
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertTrue(cli.onecmd("EOF"))
        self.mock_stdout.flush()
        msg = f.getvalue()
        self.assertTrue(len(msg) == 1)
        self.assertEqual("\n", msg)
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertTrue(cli.onecmd("EOF garbage"))
        self.mock_stdout.flush()
        msg = f.getvalue()
        self.assertTrue(len(msg) == 1)
        self.assertEqual("\n", msg)


if __name__ == "__main__":
    unittest.main()
