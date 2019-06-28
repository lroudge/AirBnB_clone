#!/usr/bin/python3
"""Module for FileStorage class."""
import os
import json

class FileStorage:
    """Class for serializtion and deserialization of base classes."""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns __objects dictionary."""
        # TODO: should this be a copy()?
        return FileStorage.__objects

    def new(self, obj):
        """Sets new obj in __objects dictionary."""
        # TODO: should these be more precise specifiers?
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialzes __objects to JSON file."""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            d = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
            json.dump(d, f)

    def reload(self):
        """Deserializes JSON file into __objects."""
        from models.base_model import BaseModel
        if not os.path.isfile(FileStorage.__file_path):
            return
        classes = {"BaseModel" : BaseModel}
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            obj_dict = json.load(f)
            obj_dict = {k: classes[v["__class__"]](**v) for k, v in obj_dict.items()}
            # TODO: should this overwrite or insert?
            FileStorage.__objects = obj_dict
