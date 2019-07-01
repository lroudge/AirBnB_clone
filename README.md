# AirBnB clone - The console

<p align="center">
    <img src="https://i.imgur.com/JOhaZ5m.png">
</p>

## Description

This team project is part of the Holberton School Full-Stack Software Engineer program.
It's the first step towards building a first full web application: an AirBnB clone.
This first step consists of a custom command-line interepreter for data management, and the base classes for the storage of this data.

## Usage

The console works both in interactive mode and non-interactive mode, much like a Unix shell.

To run the console:
```./console.py```

Quit the console:
```
(hbnb) quit
```

Display the help for a command:
```
(hbnb) help <command>
```

Create an object (prints its id):
```
(hbnb) create <class>
```

Show an object:
```
(hbnb) show <class> <id>
```
or
```
(hbnb) <class>.show(<id>)
```

Destroy an object:
```
(hbnb) destroy <class> <id>
```
or
```
(hbnb) <class>.destroy(<id>)
```

Show all objects, or all instances of a class:
```
(hbnb) all
```
or
```
(hbnb) all <class>
```

Update an attribute of an object:
```
(hbnb) update <class> <id> <attribute name> "<attribute value>"
```
or
```
(hbnb) <class>.update(<id>, <attribute name>, "<attribute value>")
```

Non-interactive mode example:
```bash
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update
```

## Models

The folder [models](./models/) contains all the classes used in this project.

File | Description
---- | -----------
[base_model.py](./models/base_model.py) | BaseModel class for all the other classes
[user.py](./models/user.py) | User class for future user information
[amenity.py](./models/amenity.py) | Amenity class for future amenity information
[city.py](./models/city.py) | City class for future location information
[state.py](./models/state.py) | State class for future location information
[place.py](./models/place.py) | Place class for future accomodation information
[review.py](./models/review.py) | Review class for future user/host review information

## File storage

The folder [engine](./models/engine/) manages the serialization and deserialization of all the data, following a JSON format.

A FileStorage class is defined in [file_storage.py](./models/engine/file_storage.py) with methods to follow this flow:
```<object> -> to_dict() -> <dictionary> -> JSON dump -> <json string> -> FILE -> <json string> -> JSON load -> <dictionary> -> <object>```

The [__init__.py](./models/__init__.py) file contains the instantiation of the FileStorage class called **storage**, followed by a call to the method reload() on that instance.
This allows the storage to be reloaded automatically at initialization, which recovers the serialized data.

## Tests

All the code is tested with the **unittest** module.
The test for the classes are in the [test_models](./tests/tests_models) folder.

## Authors

* **Arthur Damm** - [indigoarthur@gmail.com](https://github.com/arthurdamm)
