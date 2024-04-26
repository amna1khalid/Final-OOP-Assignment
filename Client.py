#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pickle  # Import the pickle module for object serialization
from enum import Enum  # Import Enum class for creating enumerated constants

# Define Client class to represent a client instance
class Client:
    data_file = "clients.pkl"  # File to store client data

    # Initialize client attributes with input validation
    def __init__(self, client_id, name, address, contact_details, budget):
        # Validate client ID
        if not isinstance(client_id, str) or not client_id:
            raise ValueError("Client ID must be a non-empty string")
        
        # Validate name
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string")
        
        # Validate address
        if not isinstance(address, str) or not address:
            raise ValueError("Address must be a non-empty string")
        
        # Validate contact details
        if not isinstance(contact_details, str) or not contact_details:
            raise ValueError("Contact details must be an non-empty string")
        
        # Validate budget (must be at least 5000)
        if not isinstance(budget, (int, float)) or budget < 5000:
            raise ValueError("Budget must be at least 5000")

        # Set client attributes
        self.client_id = client_id  # Assign client ID
        self.name = name  # Assign client name
        self.address = address  # Assign client address
        self.contact_details = contact_details  # Assign client contact details
        self.budget = budget  # Assign client budget

    # Get client details as a dictionary
    def get_client_details(self):
        return {
            "Client ID": self.client_id,  # Return client ID
            "Name": self.name,  # Return client name
            "Address": self.address,  # Return client address
            "Contact Details": self.contact_details,  # Return client contact details
            "Budget": self.budget  # Return client budget
        }

    # Class method to load clients from file
    @classmethod
    def load_clients(cls):
        try:
            with open(cls.data_file, "rb") as file:
                return pickle.load(file)  # Load clients from file using pickle
        except FileNotFoundError:
            return {}  # Return an empty dictionary if file does not exist

    # Class method to save clients to file
    @classmethod
    def save_clients(cls, clients):
        with open(cls.data_file, "wb") as file:
            pickle.dump(clients, file)  # Save clients to file using pickle


# In[ ]:




