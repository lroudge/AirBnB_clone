#!/usr/bin/python3
"""Unittest module for the BaseModel Class."""

import unittest
from datetime import datetime
import time
from models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):
    """Test Cases for the BaseModel class."""

    def setUp(self):
        """Sets up test methods."""
        pass

    def tearDown(self):
        """Tears down test methods."""
        pass
    
    def test_3_instantiation(self):
        """Tests instantiation of BaseModel class."""

        b = BaseModel()
        self.assertEqual(str(type(b)), "")
        self.assertIsInstance(b, BaseModel)
        self.assertFalse(issubclass(b, BaseModel))

    def test_3_attributes(self):
        """Tests attributes value for instance of a BaseModel class."""

        date_now = datetime.now()
        b = BaseModel()
        diff = b.updated_at - b.created_at
        self.assertTrue(diff.total_seconds() < abs(0.01))
        diff = b.created_at - date_now
        self.assertTrue(diff.total_seconds() < abs(0.1))

    def test_3_id(self):
        """Tests for unique user ids."""

        l = []
        for i in range(1000):
            b = BaseModel()
            l.append(b.id)
        self.assertEqual(len(set(l)), len(l))

    def test_3_save(self):
        """Tests the public instance method save()."""
        
        b = Base()
        time.sleep(0.5)
        date_now = datetime.now()
        b.save()
        diff = b.updated_at - date_now
        self.assertTrue(diff.total_seconds() < abs(0.01))

    def test_3_str(self):
        """Tests for __str__ method."""

        

    def test_3_to_dict(self):
        """Tests the public instance method to_dict()."""
        
        b = Base()
        b.name = "Laura"
        b.age = 23
        d = b.to_dict()
        self.assertEqual(d["id"], b.id)
        self.assertEqual(d["__class__"], type(b).__name__)
        self.assertEqual(d["created_at"], b.created_at.isoformat())
        self.assertEqual(d["updated_at"], b.updated_at.isoformat())
        self.assertEqual(d["name"], b.name)
        self.assertEqual(d["age"], b.age)

    def test_4_instantiation(self):
        """Tests instantiation with **kwargs."""

        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        my_model_json = my_model.to_dict()
        my_new_model = BaseModel(**my_model_json)
        """Test for dict equality?"""
