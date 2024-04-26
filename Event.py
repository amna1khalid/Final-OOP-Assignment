#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import pickle  # Import the pickle module for object serialization
from enum import Enum  # Import Enum class for creating enumerated constants
import datetime  # Import datetime module for handling date and time

#import necessary classes from other files
from Client import Client
from Guest import Guest
from Supplier import Supplier
from Venue import Venue

# Define EventType enum to represent different types of events
class EventType(Enum):
    # Define event types with string values
    WEDDING = "Wedding"
    BIRTHDAY = "Birthday"
    THEMED_PARTY = "Themed Party"
    GRADUATION = "Graduation"

# Define Event class to represent an event instance
class Event:
    data_file = "events.pkl"  # File to store event data

    # Initialize event attributes with input validation
    def __init__(self, event_id, event_type, theme, date, time, duration, venue_address, client_id, guest_list,
                 catering_company, cleaning_company, decorations_company, entertainment_company,
                 furniture_supply_company, invoice):
        # Validate event ID
        if not isinstance(event_id, str) or not event_id:
            raise ValueError("Event ID must be a non-empty string")
        
        # Validate theme
        if not isinstance(theme, str) or not theme:
            raise ValueError("Theme must be a non-empty string")
        
        # Validate date format (should be dd/mm/yyyy)
        try:
            datetime.datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Date format should be dd/mm/yyyy")
        
        # Validate time format (should be hh:mm)
        try:
            datetime.datetime.strptime(time, "%H:%M")
        except ValueError:
            raise ValueError("Time format should be hh:mm")
        
        # Validate duration (must be a positive integer)
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("Duration must be a positive integer")
        
        # Validate venue address against existing venues
        venues = Venue.load_venues()
        venue = next((v for v in venues.values() if v.address == venue_address), None)
        if not venue:
            raise ValueError("Venue with address {} does not exist".format(venue_address))
        
        # Validate client ID against existing clients
        client = Client.load_clients().get(client_id)
        if not client:
            raise ValueError("Client does not exist")
        
        # Validate guest list format and existence
        if not isinstance(guest_list, list):
            raise ValueError("Guest list must be a list")
        
        guests = Guest.load_guests()
        for guest_id in guest_list:
            if not isinstance(guest_id, str):
                raise ValueError("Each guest ID in the guest list must be a string")
            if guest_id not in guests:
                raise ValueError(f"Guest with ID {guest_id} does not exist")
        
        # Validate catering company against existing suppliers
        catering_supplier = Supplier.load_suppliers().get(catering_company)
        if not catering_supplier:
            raise ValueError("Catering company with ID {} does not exist".format(catering_company))
        
        # Validate cleaning company against existing suppliers
        cleaning_supplier = Supplier.load_suppliers().get(cleaning_company)
        if not cleaning_supplier:
            raise ValueError("Cleaning company with ID {} does not exist".format(cleaning_company))
        
        # Validate decorations company against existing suppliers
        decorations_supplier = Supplier.load_suppliers().get(decorations_company)
        if not decorations_supplier:
            raise ValueError("Decorations company with ID {} does not exist".format(decorations_company))
        
        # Validate entertainment company against existing suppliers
        entertainment_supplier = Supplier.load_suppliers().get(entertainment_company)
        if not entertainment_supplier:
            raise ValueError("Entertainment company with ID {} does not exist".format(entertainment_company))
        
        # Validate furniture supply company against existing suppliers
        furniture_supplier = Supplier.load_suppliers().get(furniture_supply_company)
        if not furniture_supplier:
            raise ValueError("Furniture supply company with ID {} does not exist".format(furniture_supply_company))
        
        # Validate invoice amount against client's budget
        if not 0 < int(invoice) < client.budget: 
            raise ValueError("Invoice must be a positive number not exceeding the client's budget")
        
        # Validate guest count against venue capacity
        if not (venue.min_guests <= len(guest_list) <= venue.max_guests):
            raise ValueError("Number of guests does not meet venue capacity")

        # Set event attributes
        self.event_id = event_id
        self.event_type = event_type
        self.theme = theme
        self.date = date
        self.time = time
        self.duration = duration
        self.venue_address = venue_address
        self.client_id = client_id
        self.guest_list = guest_list
        self.catering_company = catering_company
        self.cleaning_company = cleaning_company
        self.decorations_company = decorations_company
        self.entertainment_company = entertainment_company
        self.furniture_supply_company = furniture_supply_company
        self.invoice = invoice

    # Get event details as a dictionary
    def get_event_details(self):
        return {
            "Event ID": self.event_id,
            "Type": self.event_type.value,  # Retrieve enum value
            "Theme": self.theme,
            "Date": self.date,
            "Time": self.time,
            "Duration": self.duration,
            "Venue Address": self.venue_address,
            "Client ID": self.client_id,
            # Get guest details for each guest in the guest list
            "Guest List": [guest.get_guest_details() for guest in self.guest_list],
            # Retrieve company name from Supplier class assuming it has a 'name' attribute
            "Catering Company": self.catering_company.name,
            "Cleaning Company": self.cleaning_company.name,
            "Decorations Company": self.decorations_company.name,
            "Entertainment Company": self.entertainment_company.name,
            "Furniture Supply Company": self.furniture_supply_company.name,
            "Invoice": self.invoice
        }

    # Class method to load events from file
    @classmethod
    def load_events(cls):
        try:
            with open(cls.data_file, "rb") as file:
                return pickle.load(file) or {}  # Load events from file or return an empty dictionary
        except FileNotFoundError:
            return {}  # Return an empty dictionary if file does not exist
        except Exception as e:
            print(f"Error loading events: {e}")
            return {}  # Return an empty dictionary if an error occurs during loading

    # Class method to save events to file
    @classmethod
    def save_events(cls, events):
        try:
            with open(cls.data_file, "wb") as file:
                pickle.dump(events, file)  # Save events to file using pickle
        except Exception as e:
            print(f"Error saving events: {e}")  # Print error message if saving fails


# In[ ]:




