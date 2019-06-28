#!/usr/bin/python3
"""Module for the entry point of the command interpreter."""

import cmd
import inspect
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage

class HBNBCommand(cmd.Cmd):
    """Class for the command interpreter."""

    prompt = "(hbnb) "

    def do_EOF(self, line):
        """Handles EOF."""
        return True

    def do_quit(self, line):
        """Quit command to exit the program
        """
        return True

    def emptyline(self):
        """Doesn't do anything on ENTER."""
        pass

    def do_create(self, line):
        """Creates an instance."""
        if line == "" or line is None:
            print("** class name missing **")
        elif line != "BaseModel":
        # TODO : find a not BF way to check if class exists
            print("** class doesn't exist **")
        else:
            b = BaseModel()
            print(b.id)

    def do_show(self, line):
        """Prints the string representation of an instance
        based on the class name and id."""
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] != "BaseModel":
            # TODO : find a not BF way to check if class exists
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if not key in FileStorage._FileStorage__objects:
                    print("** no instance found **")
                else:
                    print(FileStorage._FileStorage__objects[key])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id."""
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] != "BaseModel":
            # TODO : find a not BF way to check if class exists
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if not key in FileStorage._FileStorage__objects:
                    print("** no instance found **")
                else:
                    FileStorage._FileStorage__objects[key].save()
                    del FileStorage._FileStorage__objects[key]


    def do_all(self, line):
        """Prints all string representation of
        all instances based or not on the class name."""
        if line != "":
            words = line.split(' ')
            if words[0] != "BaseModel":
            # TODO : find a not BF way to check if class exists
                print("** class doesn't exist **")
        for k in FileStorage._FileStorage__objects:
            print(FileStorage._FileStorage__objects[k])

    def do_update(self, line):
        """Updates an instance based on the class
        name and id by adding or updating attribute."""
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] != "BaseModel":
            # TODO : find a not BF way to check if class exists
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            elif len(words) < 3:
                print("** attribute name missing **")
            elif len(words) < 4:
                print("** value missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if not key in FileStorage._FileStorage__objects:
                    print("** no instance found **")
                else:
                    setattr(FileStorage._FileStorage__objects[key], words[2], words[3])

if __name__ == '__main__':
    HBNBCommand().cmdloop()
