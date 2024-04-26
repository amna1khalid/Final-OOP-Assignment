#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pickle  # Import the pickle module for object serialization
from enum import Enum  # Import Enum class for creating enumerated constants

# Define Guest class to represent a guest instance
class Guest:
    data_file = "guests.pkl"  # File to store guest data

    # Initialize guest attributes with input validation
    def __init__(self, guest_id, name, address, contact_details):
        # Validate guest ID
        if not isinstance(guest_id, str) or not guest_id:
            raise ValueError("Guest ID must be a non-empty string")
        
        # Validate name
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string")
        
        # Validate address
        if not isinstance(address, str) or not address:
            raise ValueError("Address must be a non-empty string")
        
        # Validate contact details
        if not isinstance(contact_details, str) or not contact_details:
            raise ValueError("Contact details must be a non-empty string")

        # Set guest attributes
        self.guest_id = guest_id  # Assign guest ID
        self.name = name  # Assign guest name
        self.address = address  # Assign guest address
        self.contact_details = contact_details  # Assign guest contact details

    # Get guest details as a dictionary
    def get_guest_details(self):
        return {
            "Guest ID": self.guest_id,  # Return guest ID
            "Name": self.name,  # Return guest name
            "Address": self.address,  # Return guest address
            "Contact Details": self.contact_details  # Return guest contact details
        }

    # Class method to load guests from file
    @classmethod
    def load_guests(cls):
        try:
            with open(cls.data_file, "rb") as file:
                return pickle.load(file)  # Load guests from file using pickle
        except FileNotFoundError:
            return {}  # Return an empty dictionary if file does not exist

    # Class method to save guests to file
    @classmethod
    def save_guests(cls, guests):
        with open(cls.data_file, "wb") as file:
            pickle.dump(guests, file)  # Save guests to file using pickle
            


# In[ ]:




