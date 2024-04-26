#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import pickle  # Import the pickle module for object serialization
from enum import Enum  # Import Enum class for creating enumerated constants
# Define Venue class to represent a venue instance
class Venue:
    data_file = "venues.pkl"  # File to store venue data

    # Initialize venue attributes with input validation
    def __init__(self, venue_id, name, address, contact, min_guests, max_guests):
        # Validate venue ID
        if not isinstance(venue_id, str) or not venue_id:
            raise ValueError("Venue ID must be a non-empty string")
        
        # Validate name
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string")
        
        # Validate address
        if not isinstance(address, str) or not address:
            raise ValueError("Address must be a non-empty string")
        
        # Validate contact
        if not isinstance(contact, str) or not contact:
            raise ValueError("Contact must be a non-empty string")
        
        # Validate minimum number of guests (must be a positive integer)
        if not isinstance(min_guests, int) or min_guests <= 0:
            raise ValueError("Minimum number of guests must be a positive integer")
        
        # Validate maximum number of guests (must be greater than minimum number of guests)
        if not isinstance(max_guests, int) or max_guests <= min_guests:
            raise ValueError("Maximum number of guests must be greater than the Minimum number of guests")

        # Set venue attributes
        self.venue_id = venue_id  # Assign venue ID
        self.name = name  # Assign venue name
        self.address = address  # Assign venue address
        self.contact = contact  # Assign venue contact
        self.min_guests = min_guests  # Assign minimum number of guests
        self.max_guests = max_guests  # Assign maximum number of guests

    # Get venue details as a dictionary
    def get_venue_details(self):
        return {
            "Venue ID": self.venue_id,  # Return venue ID
            "Name": self.name,  # Return venue name
            "Address": self.address,  # Return venue address
            "Contact": self.contact,  # Return venue contact
            "Minimum Number of Guests": self.min_guests,  # Return minimum number of guests
            "Maximum Number of Guests": self.max_guests  # Return maximum number of guests
        }

    # Class method to load venues from file
    @classmethod
    def load_venues(cls):
        try:
            with open(cls.data_file, "rb") as file:
                return pickle.load(file)  # Load venues from file using pickle
        except FileNotFoundError:
            return {}  # Return an empty dictionary if file does not exist

    # Class method to save venues to file
    @classmethod
    def save_venues(cls, venues):
        with open(cls.data_file, "wb") as file:
            pickle.dump(venues, file)  # Save venues to file using pickle
            


# In[ ]:




