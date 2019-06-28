#!/usr/bin/python3
"""Unittest module for the FileStorage class."""

import unittest
from datetime import datetime
import time
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
import re
import json
import os

class TestFileStorage(unittest.TestCase):
    """Test Cases for the FileStorage class."""

    def setUp(self):
        """Sets up test methods."""
        pass

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        # TODO: should this reference the class attribute differently?
        # such as: storage.__class__.MANGLED_ATTR
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def tearDown(self):
        """Tears down test methods."""
        pass

    def test_5_instantiation(self):
        """Tests instantiation of storage class."""
        self.assertEqual(type(storage).__name__, "FileStorage")
        
    def test_5_attributes(self):
        """Tests class attributes."""
        self.resetStorage()
        self.assertTrue(hasattr(FileStorage, "_FileStorage__file_path"))
        self.assertTrue(hasattr(FileStorage, "_FileStorage__objects"))
        self.assertEqual(getattr(FileStorage, "_FileStorage__objects"), {})

    def test_5_all(self):
        """Tests all() method."""
        self.resetStorage()
        self.assertEqual(storage.all(), {})
        
        b = BaseModel()
        storage.new(b)
        key = "{}.{}".format(type(b).__name__, b.id)
        self.assertTrue(key in storage.all())
        self.assertEqual(storage.all()[key], b)

    def test_5_all_multiple(self):
        """Tests all() method with many objects."""
        self.resetStorage()
        self.assertEqual(storage.all(), {})
        
        objs = [BaseModel() for i in range(1000)]
        [storage.new(b) for b in objs]
        self.assertEqual(len(objs), len(storage.all()))
        for b in objs:
            key = "{}.{}".format(type(b).__name__, b.id)
            self.assertTrue(key in storage.all())
            self.assertEqual(storage.all()[key], b)

    def test_5_new(self):
        """Tests new() method."""
        self.resetStorage()
        
        b = BaseModel()
        storage.new(b)
        key = "{}.{}".format(type(b).__name__, b.id)
        self.assertTrue(key in FileStorage._FileStorage__objects)
        self.assertEqual(FileStorage._FileStorage__objects[key], b)

    def test_5_save(self):
        """Tests save() method."""
        self.resetStorage()
        b = BaseModel()
        storage.new(b)
        key = "{}.{}".format(type(b).__name__, b.id)
        storage.save()
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        d = { key: b.to_dict() }
        with open(FileStorage._FileStorage__file_path, "r", encoding="utf-8") as f:
            self.assertEqual(len(f.read()), len(json.dumps(d)))
            f.seek(0)
            self.assertEqual(json.load(f), d)

    def test_5_reload(self):
        """Tests reload() method."""
        self.resetStorage()
        storage.reload()
        self.assertEqual(FileStorage._FileStorage__objects, {})
        b = BaseModel()
        storage.new(b)
        key = "{}.{}".format(type(b).__name__, b.id)
        storage.save()
        storage.reload()
        self.assertEqual(b.to_dict(), storage.all()[key].to_dict())

    def test_5_reload_mismatch(self):
        """Tests reload() method."""
        self.resetStorage()
        storage.reload()
        self.assertEqual(FileStorage._FileStorage__objects, {})
        b = BaseModel()
        storage.new(b)
        key = "{}.{}".format(type(b).__name__, b.id)
        storage.save()
        b.name = "Laura"
        storage.reload()
        self.assertNotEqual(b.to_dict(), storage.all()[key].to_dict())

if __name__ == '__main__':
    unittest.main()
