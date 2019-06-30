#!/usr/bin/python3
"""Module for the entry point of the command interpreter."""

import cmd
import inspect
from models.base_model import BaseModel
from models import storage
import re


class HBNBCommand(cmd.Cmd):

    """Class for the command interpreter."""

    prompt = "(hbnb) "

    def precmd(self, line):
        """Intercepts commands to test for class.syntax()"""
        match = re.search("^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line
        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)
        command = method + " " + classname + " " + args
        self.onecmd(command)
        return ""

    def do_EOF(self, line):
        """Handles EOF."""
        print()
        return True

    def do_quit(self, line):
        """Exits the program.
        """
        return True

    def emptyline(self):
        """Doesn't do anything on ENTER.
        """
        pass

    def do_create(self, line):
        """Creates an instance.
        """
        if line == "" or line is None:
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class doesn't exist **")
        else:
            b = storage.classes()[line]()
            b.save()
            print(b.id)

    def do_show(self, line):
        """Prints the string representation of an instance\
        based on the class name and id.
        """
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id.
        """
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, line):
        """Prints all string representation of\
        all instances based or not on the class name.
        """
        if line != "":
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                l = [str(obj) for key, obj in storage.all().items() \
                     if type(obj).__name__ == words[0]]
                print(l)
        else:
                l = [str(obj) for key, obj in storage.all().items()]
                print(l)

    def do_count(self, line):
        """Counts the instances of a class.
        """
        words = line.split(' ')
        if not words[0]:
            print("** class name missing **")
        elif words[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            matches = [k for k in storage.all() if k.startswith(words[0] + '.')]
            print(len(matches))

    def do_update(self, line):
        """Updates an instance based on the class\
        name and id by adding or updating attribute.
        """
        if line == "" or line is None:
            print("** class name missing **")
            return

        rex = '^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, line)
        if not match:
            print("** class name missing **")
        elif match.group(1) not in storage.classes():
            print("** class doesn't exist **")
        elif match.group(2) is None:
            print("** instance id missing **")
        elif match.group(3) is None:
            print("** attribute name missing **")
        elif match.group(4) is None:
            print("** value missing **")
        else:
            value = match.group(4).replace('"', '')
            key = "{}.{}".format(match.group(1), match.group(2))
            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[match.group(1)]
                if match.group(3) in attributes:
                    value = attributes[match.group(3)](value)
                setattr(storage.all()[key], match.group(3), value)
                storage.all()[key].save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
