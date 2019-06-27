#!/usr/bin/python3
"""Unittest module for the BaseModel Class."""

import unittest
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
        self.assertTrue(isinstance(b, BaseModel))
        self.assertFalse(issubclass(b, BaseModel))

    def test_3_attributes(self):
        """Tests attributes value for instance of a BaseModel class."""

        b = BaseModel()
        """How to test for random values like id and dates?"""

    def test_3_save(self):
        """Tests the public instance method save()."""
        
        b = Base()
        b.save()
        """How to test for random date?"""

    def test_3_to_dict(self):
        """Tests the public instance method to_dict()."""
        
        b = Base()
        d = b.to_dict()
        """How to test for random values like id and dates?"""

    def test_4_instantiation(self):
        """Tests instantiation with **kwargs."""

        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        my_model_json = my_model.to_dict()
        my_new_model = BaseModel(**my_model_json)
        """Test for dict equality?"""
