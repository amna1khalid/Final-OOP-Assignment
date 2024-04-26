#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import pickle  # Import the pickle module for object serialization
from enum import Enum  # Import Enum class for creating enumerated constants

# Define Supplier class to represent a supplier instance
class Supplier:
    data_file = "suppliers.pkl"  # File to store supplier data

    # Initialize supplier attributes with input validation
    def __init__(self, supplier_id, name, address, contact_details):
        # Validate supplier ID
        if not isinstance(supplier_id, str) or not supplier_id:
            raise ValueError("Supplier ID must be a non-empty string")
        
        # Validate name
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string")
        
        # Validate address
        if not isinstance(address, str) or not address:
            raise ValueError("Address must be a non-empty string")
        
        # Validate contact details
        if not isinstance(contact_details, str) or not contact_details:
            raise ValueError("Contact details must be a non-empty string")

        # Set supplier attributes
        self.supplier_id = supplier_id  # Assign supplier ID
        self.name = name  # Assign supplier name
        self.address = address  # Assign supplier address
        self.contact_details = contact_details  # Assign supplier contact details

    # Get supplier details as a dictionary
    def get_supplier_details(self):
        return {
            "Supplier ID": self.supplier_id,  # Return supplier ID
            "Name": self.name,  # Return supplier name
            "Address": self.address,  # Return supplier address
            "Contact Details": self.contact_details  # Return supplier contact details
        }

    # Class method to load suppliers from file
    @classmethod
    def load_suppliers(cls):
        try:
            with open(cls.data_file, "rb") as file:
                return pickle.load(file)  # Load suppliers from file using pickle
        except FileNotFoundError:
            return {}  # Return an empty dictionary if file does not exist

    # Class method to save suppliers to file
    @classmethod
    def save_suppliers(cls, suppliers):
        with open(cls.data_file, "wb") as file:
            pickle.dump(suppliers, file)  # Save suppliers to file using pickle


# In[ ]:




