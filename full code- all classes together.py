#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import necessary modules
import tkinter as tk  # Import the tkinter library and alias it as tk for easier access
from tkinter import ttk, messagebox, simpledialog  # Import specific modules from tkinter

import pickle  # Import the pickle module for object serialization
from enum import Enum  # Import Enum class for creating enumerated constants
import datetime  # Import datetime module for handling date and time
import ast  # Import ast module for working with abstract syntax trees (not used in this script)

# Define JobTitle enum
class JobTitle(Enum):  # Create a custom enumeration class for job titles
    # Define job title enum options as constants with string values
    SALES_MANAGER = "Sales Manager"
    SALESPERSON = "Salesperson"
    MARKETING_MANAGER = "Marketing Manager"
    MARKETER = "Marketer"
    ACCOUNTANT = "Accountant"
    DESIGNER = "Designer"
    HANDYMAN = "Handyman"

# Define Employee class
class Employee:  # Create a class to represent an employee
    # Define data file path as a class variable
    data_file = "employees.pkl"

    # Initialize employee attributes with input validation
    def __init__(self, name, employee_id, department, job_title, basic_salary, age, date_of_birth, passport_details):
        # Validate name input
        if not isinstance(name, str) or not name.strip():  # Check if name is a non-empty string
            raise ValueError("Name must be a non-empty string")

        # Validate employee ID input
        if not isinstance(employee_id, str) or not employee_id.strip():  # Check if employee_id is a non-empty string
            raise ValueError("Employee ID must be a non-empty string")

        # Validate department input
        if not isinstance(department, str) or not department.strip():  # Check if department is a non-empty string
            raise ValueError("Department must be a non-empty string")

        # Validate job title input against predefined options
        if not isinstance(job_title, str) or job_title.strip() not in [e.value for e in JobTitle]:  # Check if job_title is a valid option
            raise ValueError("Invalid job title")

        # Validate basic salary input
        if not isinstance(basic_salary, (int, float)) or float(basic_salary) < 5000:  # Check if basic_salary is a numeric value of at least 5000
            raise ValueError("Basic salary must be at least a 5000 numeric value")

        # Validate age input
        if not isinstance(age, int) or int(age) < 18:  # Check if age is an integer of at least 18
            raise ValueError("Age must be an integer value and greater than or equal to 18")

        # Validate date of birth input
        if not isinstance(date_of_birth, str) or not date_of_birth.strip():  # Check if date_of_birth is a non-empty string
            raise ValueError("Date of birth must be a non-empty string")

        # Validate passport details input
        passport_details = passport_details.strip()  # Remove leading and trailing whitespace
        if not (isinstance(passport_details, str) and len(passport_details) in range(8, 10) and passport_details.isdigit()):  # Check if passport_details is a string of 8 to 9 digits
            raise ValueError("Passport details must be a string of 8 to 9 digits")

        # Assign validated attributes to the instance
        self.name = name
        self.employee_id = employee_id
        self.department = department
        self.job_title = job_title
        self.basic_salary = basic_salary
        self.age = age
        self.date_of_birth = date_of_birth
        self.passport_details = passport_details

    # Method to update employee salary
    def update_salary(self, new_salary):  # Define a method to update the employee's basic salary
        # Validate new salary input
        if not isinstance(new_salary, (int, float)) or new_salary <= 0:  # Check if new_salary is a positive number
            raise ValueError("New salary must be a positive number")
        self.basic_salary = new_salary  # Update the employee's basic salary

    # Method to retrieve employee details as a dictionary
    def get_employee_details(self):  # Define a method to return employee details as a dictionary
        return {
            "Name": self.name,
            "Employee ID": self.employee_id,
            "Department": self.department,
            "Job Title": self.job_title.value,  # Retrieve the enum value of job title
            "Basic Salary": self.basic_salary,
            "Age": self.age,
            "Date of Birth": self.date_of_birth,
            "Passport Details": self.passport_details
        }

    # Class method to load employees from a file
    @classmethod
    def load_employees(cls):  # Define a class method to load employees from a file
        try:
            with open(cls.data_file, "rb") as file:  # Open the data file in read binary mode
                return pickle.load(file)  # Load employees from the file using pickle
        except FileNotFoundError:  # Handle file not found error
            return {}  # Return an empty dictionary if the file is not found
        except Exception as e:  # Handle other exceptions
            print(f"Error loading employees: {e}")  # Print error message if loading fails

    # Class method to save employees to a file
    @classmethod
    def save_employees(cls, employees):  # Define a class method to save employees to a file
        try:
            with open(cls.data_file, "wb") as file:  # Open the data file in write binary mode
                pickle.dump(employees, file)  # Save employees to the file using pickle
        except Exception as e:  # Handle exceptions
            print(f"Error saving employees: {e}")  # Print error message if saving fails
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
            

# Define the main GUI class for the Event Management System
class EventManagementSystemGUI(tk.Tk):  # Subclass of tk.Tk for the main application window
    def __init__(self):
        super().__init__()  # Initialize the main Tkinter application window
        self.title("Event Management System")  # Set the window title
        self.geometry("800x600")  # Set the window size

        # Initialize data storage (load existing data or create new empty dictionaries)
        try:
            self.employees = Employee.load_employees()  # Load employee data from file
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load employee data: {e}")
            self.employees = {}  # Initialize empty dictionary for employees if loading fails
        
        # Repeat the above process for other data types: events, clients, guests, suppliers, and venues
        try:
            self.events = Event.load_events()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load event data: {e}")
            self.events = {}

        try:
            self.clients = Client.load_clients()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load client data: {e}")
            self.clients = {}

        try:
            self.guests = Guest.load_guests()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load guest data: {e}")
            self.guests = {}

        try:
            self.suppliers = Supplier.load_suppliers()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load supplier data: {e}")
            self.suppliers = {}

        try:
            self.venues = Venue.load_venues()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load venue data: {e}")
            self.venues = {}

        # Create a notebook (tabbed interface) to organize different functionalities
        self.notebook = ttk.Notebook(self)  # Create a ttk Notebook widget
        self.notebook.pack(fill=tk.BOTH, expand=True)  # Pack the notebook to fill the main window

        # Create tabs for different functionalities
        self.create_employee_tab()  # Method to create the employee management tab
        self.create_client_tab()  # Method to create the client management tab
        self.create_guest_tab()  # Method to create the guest management tab
        self.create_venue_tab()  # Method to create the venue management tab
        self.create_supplier_tab()  # Method to create the supplier management tab
        self.create_event_tab()  # Method to create the event management tab

    # Method to create the employee management tab
    def create_employee_tab(self):
        employee_tab = ttk.Frame(self.notebook)  # Create a new tab frame for employees
        self.notebook.add(employee_tab, text="Employees")  # Add the employee tab to the notebook

        # Add widgets for employee management within the tab
        employee_frame = ttk.LabelFrame(employee_tab, text="Add / Modify Employee")  # Create a labeled frame for employee operations
        employee_frame.pack(padx=10, pady=10, fill=tk.BOTH)  # Pack the employee frame with padding and fill options

        # Add entry fields for employee details
        tk.Label(employee_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)  # Label for employee name
        tk.Label(employee_frame, text="ID:").grid(row=1, column=0, padx=5, pady=5)  # Label for employee ID
        tk.Label(employee_frame, text="Department:").grid(row=2, column=0, padx=5, pady=5)  # Label for employee department
        tk.Label(employee_frame, text="Job Title:").grid(row=3, column=0, padx=5, pady=5)  # Label for employee job title
        tk.Label(employee_frame, text="Basic Salary:").grid(row=4, column=0, padx=5, pady=5)  # Label for employee basic salary
        tk.Label(employee_frame, text="Age:").grid(row=5, column=0, padx=5, pady=5)  # Label for employee age
        tk.Label(employee_frame, text="Date of Birth:").grid(row=6, column=0, padx=5, pady=5)  # Label for employee date of birth
        tk.Label(employee_frame, text="Passport Details:").grid(row=7, column=0, padx=5, pady=5)  # Label for employee passport details

        self.name_entry = tk.Entry(employee_frame)  # Entry field for employee name
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)  # Grid placement for name entry
        self.id_entry = tk.Entry(employee_frame)  # Entry field for employee ID
        self.id_entry.grid(row=1, column=1, padx=5, pady=5)  # Grid placement for ID entry
        self.department_entry = tk.Entry(employee_frame)  # Entry field for employee department
        self.department_entry.grid(row=2, column=1, padx=5, pady=5)  # Grid placement for department entry

        # Use OptionMenu for job title selection with predefined options
        self.selected_job_title = tk.StringVar(employee_frame)  # Variable to store selected job title
        self.selected_job_title.set(JobTitle.SALES_MANAGER.value)  # Set default job title
        job_title_options = [e.value for e in JobTitle]  # Get list of job title options
        job_title_menu = tk.OptionMenu(employee_frame, self.selected_job_title, *job_title_options)  # Create job title dropdown menu
        job_title_menu.grid(row=3, column=1, padx=5, pady=5)  # Grid placement for job title dropdown

        # Additional entry fields for other employee details
        self.salary_entry = tk.Entry(employee_frame)  # Entry field for employee salary
        self.salary_entry.grid(row=4, column=1, padx=5, pady=5)  # Grid placement for salary entry
        self.age_entry = tk.Entry(employee_frame)  # Entry field for employee age
        self.age_entry.grid(row=5, column=1, padx=5, pady=5)  # Grid placement for age entry
        self.dob_entry = tk.Entry(employee_frame)  # Entry field for employee date of birth
        self.dob_entry.grid(row=6, column=1, padx=5, pady=5)  # Grid placement for date of birth entry
        self.passport_entry = tk.Entry(employee_frame)  # Entry field for employee passport details
        self.passport_entry.grid(row=7, column=1, padx=5, pady=5)  # Grid placement for passport details entry

        # Button to add or modify employee
        add_employee_button = tk.Button(employee_frame, text="Add / Modify Employee", command=self.add_employee)  # Button to add or modify employee
        add_employee_button.grid(row=8, columnspan=2, padx=5, pady=5)  # Grid placement for add/modify button

        # Add search bar for employee ID
        search_employee_frame = ttk.LabelFrame(employee_tab, text="Search Employee")  # Create a labeled frame for employee search
        search_employee_frame.pack(padx=10, pady=10, fill=tk.BOTH)  # Pack the search frame with padding and fill options

        tk.Label(search_employee_frame, text="Search by ID:").pack(side=tk.LEFT, padx=5, pady=5)  # Label for search entry
        self.employee_search_entry = tk.Entry(search_employee_frame)  # Entry field for search
        self.employee_search_entry.pack(side=tk.LEFT, padx=5, pady=5)  # Pack the search entry field

        search_employee_button = tk.Button(search_employee_frame, text="Search", command=self.search_employee)  # Search button
        search_employee_button.pack(side=tk.LEFT, padx=5, pady=5)  # Pack the search button

        # Treeview to display employee records
        employee_tree_frame = ttk.LabelFrame(employee_tab, text="Employee Records")  # Create a labeled frame for employee records
        employee_tree_frame.pack(padx=10, pady=10, fill=tk.BOTH)  # Pack the records frame with padding and fill options

        # Create the Treeview widget with columns for employee details
        self.employee_tree = ttk.Treeview(employee_tree_frame, columns=("Name", "Department", "Job Title", "Basic Salary", "Age", "Date of Birth", "Passport Details"))  # Create Treeview with specified columns
        self.employee_tree.pack(fill=tk.BOTH)  # Pack the Treeview widget to fill the available space

        # Configure column headings for the Treeview
        self.employee_tree.heading("#0", text="ID")  # Column heading for employee ID
        self.employee_tree.heading("Name", text="Name")  # Column heading for employee name
        self.employee_tree.heading("Department", text="Department")  # Column heading for employee department
        self.employee_tree.heading("Job Title", text="Job Title")  # Column heading for employee job title
        self.employee_tree.heading("Basic Salary", text="Basic Salary")  # Column heading for employee basic salary
        self.employee_tree.heading("Age", text="Age")  # Column heading for employee age
        self.employee_tree.heading("Date of Birth", text="Date of Birth")  # Column heading for employee date of birth
        self.employee_tree.heading("Passport Details", text="Passport Details")  # Column heading for employee passport details

        # Insert employee records into the Treeview
        for emp_id, employee in self.employees.items():  # Iterate over employee dictionary
            # Insert each employee's details into the Treeview
            self.employee_tree.insert("", "end", text=emp_id, values=(employee.name, employee.employee_id, employee.department, employee.job_title, employee.basic_salary, employee.age, employee.date_of_birth, employee.passport_details))

        # Button to delete selected employee
        delete_employee_button = tk.Button(employee_tree_frame, text="Delete Employee", command=self.delete_employee)  # Create delete button for employees
        delete_employee_button.pack(side=tk.RIGHT, padx=5, pady=5)  # Pack the delete button on the right side

    def search_employee(self):
        # Search for an employee by ID
        employee_id = self.employee_search_entry.get()  # Get the employee ID from the search entry field
        if employee_id:
            if employee_id in self.employees:  # Check if employee ID exists in the dictionary
                employee = self.employees[employee_id]  # Retrieve employee details
                # Display employee details in a message box
                messagebox.showinfo("Employee found!",
                    f"Name: {employee.name}\n"
                    f"ID: {employee.employee_id}\n"
                    f"Department: {employee.department}\n"
                    f"Job Title: {employee.job_title}\n"
                    f"Basic Salary: {employee.basic_salary}\n"
                    f"Age: {employee.age}\n"
                    f"Date of Birth: {employee.date_of_birth}\n"
                    f"Passport Details: {employee.passport_details}")
            else:
                # Show message if employee ID is not found
                messagebox.showinfo("Not Found", f"No employee found with ID: {employee_id}")
        else:
            # Show error message if no employee ID is provided
            messagebox.showerror("Error", "Please enter an employee ID to search.")

    def add_employee(self):
        # Get employee details from entry fields
        name = self.name_entry.get().strip()
        employee_id = self.id_entry.get().strip()
        department = self.department_entry.get().strip()
        job_title = self.selected_job_title.get()
        basic_salary = self.salary_entry.get().strip()
        age = self.age_entry.get().strip()
        date_of_birth = self.dob_entry.get().strip()
        passport_details = self.passport_entry.get().strip()

        # Validate input fields
        if not all([name, employee_id, department, job_title, basic_salary, age, date_of_birth, passport_details]):
            # Show error message if any field is empty
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            # Convert input data to appropriate types
            basic_salary = float(basic_salary)
            age = int(age)

            # Create a new Employee object and add to dictionary
            self.employees[employee_id] = Employee(name, employee_id, department, job_title, float(basic_salary), int(age), date_of_birth, passport_details)

            # Save updated employee data to file
            Employee.save_employees(self.employees)

            # Show success message
            messagebox.showinfo("Success", "Employee details added successfully.")

            # Clear input fields after adding employee
            self.name_entry.delete(0, tk.END)
            self.id_entry.delete(0, tk.END)
            self.department_entry.delete(0, tk.END)
            self.salary_entry.delete(0, tk.END)
            self.age_entry.delete(0, tk.END)
            self.dob_entry.delete(0, tk.END)
            self.passport_entry.delete(0, tk.END)

            # Refresh the employee records in the Treeview
            self.refresh_employee_tree()

        except ValueError as ve:
            # Show error message if data conversion fails
            messagebox.showerror("Error", f"Failed to add employee: {ve}")

        except Exception as e:
            # Show error message for unexpected errors
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def delete_employee(self):
        # Get the selected employee from the Treeview
        selected_item = self.employee_tree.selection()
        if not selected_item:
            # Show error message if no employee is selected
            messagebox.showerror("Error", "Please select an employee to delete.")
            return

        # Get the employee ID from the selected Treeview item
        emp_id = self.employee_tree.item(selected_item, "text")

        # Ask for confirmation before deleting the employee
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete employee with ID: {emp_id}?")
        if confirm:
            try:
                # Delete the employee from the dictionary
                del self.employees[emp_id]

                # Save updated employee data to file
                Employee.save_employees(self.employees)

                # Show success message
                messagebox.showinfo("Success", "Employee deleted successfully.")

                # Refresh the employee records in the Treeview
                self.refresh_employee_tree()

            except Exception as e:
                # Show error message if deletion fails
                messagebox.showerror("Error", f"Failed to delete employee: {e}")

    def refresh_employee_tree(self):
        # Clear all existing items in the Treeview
        self.employee_tree.delete(*self.employee_tree.get_children())

        # Insert updated employee records into the Treeview
        for emp_id, employee in self.employees.items():
            self.employee_tree.insert("", "end", text=emp_id, values=(employee.name, employee.employee_id, employee.department, employee.job_title, employee.basic_salary, employee.age, employee.date_of_birth, employee.passport_details))
    def create_client_tab(self):
        # Create a new frame for the client tab within the notebook
        client_tab = ttk.Frame(self.notebook)
        # Add the client tab to the notebook with a specified text label
        self.notebook.add(client_tab, text="Clients")

        # Create a labeled frame for adding or modifying client details
        client_frame = ttk.LabelFrame(client_tab, text="Add / Modify Client")
        client_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Labels and entry fields for client information within the client frame
        tk.Label(client_frame, text="Client ID:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(client_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(client_frame, text="Address:").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(client_frame, text="Contact Details:").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(client_frame, text="Budget:").grid(row=4, column=0, padx=5, pady=5)

        # Entry fields for entering client details
        self.client_id_entry = tk.Entry(client_frame)
        self.client_id_entry.grid(row=0, column=1, padx=5, pady=5)
        self.client_name_entry = tk.Entry(client_frame)
        self.client_name_entry.grid(row=1, column=1, padx=5, pady=5)
        self.client_address_entry = tk.Entry(client_frame)
        self.client_address_entry.grid(row=2, column=1, padx=5, pady=5)
        self.client_contact_entry = tk.Entry(client_frame)
        self.client_contact_entry.grid(row=3, column=1, padx=5, pady=5)
        self.client_budget_entry = tk.Entry(client_frame)
        self.client_budget_entry.grid(row=4, column=1, padx=5, pady=5)

        # Button to add or modify a client using the entered details
        add_client_button = tk.Button(client_frame, text="Add / Modify Client", command=self.add_client)
        add_client_button.grid(row=5, columnspan=2, padx=5, pady=5)

        # Create a labeled frame for searching clients
        search_client_frame = ttk.LabelFrame(client_tab, text="Search Client")
        search_client_frame.pack(padx=10, pady=10, fill=tk.BOTH)

        # Label and entry field for searching clients by ID
        tk.Label(search_client_frame, text="Search by ID:").pack(side=tk.LEFT, padx=5, pady=5)
        self.client_search_entry = tk.Entry(search_client_frame)
        self.client_search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        search_client_button = tk.Button(search_client_frame, text="Search", command=self.search_client)
        search_client_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create a labeled frame for displaying client records
        client_tree_frame = ttk.LabelFrame(client_tab, text="Client Records")
        client_tree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create a Treeview widget to display client records with specified columns
        self.client_tree = ttk.Treeview(client_tree_frame, columns=("Name", "Address", "Contact Details", "Budget"), selectmode="browse")
        self.client_tree.pack(fill="both", expand=True)

        # Configure column headings for the Treeview
        self.client_tree.heading("#0", text="Client ID")
        self.client_tree.heading("Name", text="Name")
        self.client_tree.heading("Address", text="Address")
        self.client_tree.heading("Contact Details", text="Contact Details")
        self.client_tree.heading("Budget", text="Budget")

        # Insert existing client records into the Treeview
        for client_id, client in self.clients.items():
            self.client_tree.insert("", "end", text=client_id, values=(client.name, client.address, client.contact_details, client.budget))

        # Button to delete a selected client from the Treeview
        delete_client_button = tk.Button(client_tree_frame, text="Delete Client", command=self.delete_client)
        delete_client_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def search_client(self):
        # Retrieve the client ID from the search entry field
        client_id = self.client_search_entry.get()
        if client_id:
            if client_id in self.clients:  # Check if the client ID exists in the clients dictionary
                client = self.clients[client_id]  # Retrieve the client object
                # Display the client details in a message box
                messagebox.showinfo("Client found!",
                    f"Client ID: {client_id}\n"
                    f"Name: {client.name}\n"
                    f"Address: {client.address}\n"
                    f"Contact Details: {client.contact_details}\n"
                    f"Budget: {client.budget}")
            else:
                # Show a message if the client ID is not found
                messagebox.showinfo("Not Found", f"No client found with ID: {client_id}")
        else:
            # Show an error message if no client ID is provided
            messagebox.showerror("Error", "Please enter a client ID to search.")

    def add_client(self):
        # Retrieve client details from the entry fields
        client_id = self.client_id_entry.get()
        name = self.client_name_entry.get()
        address = self.client_address_entry.get()
        contact_details = self.client_contact_entry.get()
        budget = self.client_budget_entry.get()

        # Check if all required fields are filled
        if client_id and name and address and contact_details and budget:
            try:
                # Convert budget to float and validate
                budget = float(budget)
                if budget < 5000:
                    raise ValueError("Budget must be at least 5000")
            except ValueError as e:
                # Show error message for invalid budget value
                messagebox.showerror("Error", str(e))
                return

            try:
                # Create a new Client object and add it to the clients dictionary
                new_client = Client(client_id, name, address, contact_details, budget)
                self.clients[client_id] = new_client

                # Save updated clients data to file
                Client.save_clients(self.clients)

                # Show success message
                messagebox.showinfo("Success", "Client added successfully.")

                # Clear entry fields after adding client
                self.client_id_entry.delete(0, tk.END)
                self.client_name_entry.delete(0, tk.END)
                self.client_address_entry.delete(0, tk.END)
                self.client_contact_entry.delete(0, tk.END)
                self.client_budget_entry.delete(0, tk.END)

                # Refresh the client records in the Treeview
                self.refresh_client_tree()

            except Exception as e:
                # Show error message for unexpected errors
                messagebox.showerror("Error", f"Failed to add client: {e}")
        else:
            # Show error message if any required field is missing
            messagebox.showerror("Error", "Please fill in all fields for the client.")

    def delete_client(self):
        # Get the selected client from the Treeview
        selected_item = self.client_tree.selection()
        if not selected_item:
            # Show error message if no client is selected
            messagebox.showerror("Error", "Please select a client to delete.")
            return

        # Get the client ID from the selected Treeview item
        client_id = self.client_tree.item(selected_item, "text")

        # Ask for confirmation before deleting the client
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete client with ID: {client_id}?")
        if confirm:
            try:
                # Delete the client from the clients dictionary
                del self.clients[client_id]

                # Save updated clients data to file
                Client.save_clients(self.clients)

                # Show success message
                messagebox.showinfo("Success", "Client deleted successfully.")

                # Refresh the client records in the Treeview
                self.refresh_client_tree()

            except Exception as e:
                # Show error message if deletion fails
                messagebox.showerror("Error", f"Failed to delete client: {e}")

    def refresh_client_tree(self):
        # Clear all existing items in the Treeview
        self.client_tree.delete(*self.client_tree.get_children())

        # Insert updated client records into the Treeview
        for client_id, client in self.clients.items():
            self.client_tree.insert("", "end", text=client_id, values=(client.name, client.address, client.contact_details, client.budget))
    
    

    
    # Create guest tab with widgets for guest management
    def create_guest_tab(self):
        guest_tab = ttk.Frame(self.notebook)
        self.notebook.add(guest_tab, text="Guests")

        # Add widgets for guest management
        guest_frame = ttk.LabelFrame(guest_tab, text="Add / Modify Guest")
        guest_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Add entry fields for guest details
        # Labels for entry fields
        tk.Label(guest_frame, text="Guest ID:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(guest_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(guest_frame, text="Address:").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(guest_frame, text="Contact Details:").grid(row=3, column=0, padx=5, pady=5)
        # Entry fields
        self.guest_id_entry = tk.Entry(guest_frame)
        self.guest_id_entry.grid(row=0, column=1, padx=5, pady=5)
        self.guest_name_entry = tk.Entry(guest_frame)
        self.guest_name_entry.grid(row=1, column=1, padx=5, pady=5)
        self.guest_address_entry = tk.Entry(guest_frame)
        self.guest_address_entry.grid(row=2, column=1, padx=5, pady=5)
        self.guest_contact_entry = tk.Entry(guest_frame)
        self.guest_contact_entry.grid(row=3, column=1, padx=5, pady=5)
        # Add / Modify Guest button
        add_guest_button = tk.Button(guest_frame, text="Add / Modify Guest", command=self.add_guest)
        add_guest_button.grid(row=4, columnspan=2, padx=5, pady=5)

        # Add search bar for guest ID
        search_guest_frame = ttk.LabelFrame(guest_tab, text="Search Guest")
        search_guest_frame.pack(padx=10, pady=10, fill=tk.BOTH)

        tk.Label(search_guest_frame, text="Search by ID:").pack(side=tk.LEFT, padx=5, pady=5)
        self.guest_search_entry = tk.Entry(search_guest_frame)
        self.guest_search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        # Search button
        search_guest_button = tk.Button(search_guest_frame, text="Search", command=self.search_guest)
        search_guest_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Treeview for displaying guest records
        guest_tree_frame = ttk.LabelFrame(guest_tab, text="Guest Records")
        guest_tree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.guest_tree = ttk.Treeview(guest_tree_frame, columns=("Name", "Address", "Contact Details"), selectmode="browse")
        self.guest_tree.pack(fill="both", expand=True)

        # Configure column headings
        self.guest_tree.heading("#0", text="Guest ID")
        self.guest_tree.heading("Name", text="Name")
        self.guest_tree.heading("Address", text="Address")
        self.guest_tree.heading("Contact Details", text="Contact Details")

        # Insert guest records into the treeview
        for guest_id, guest in self.guests.items():
            self.guest_tree.insert("", "end", text=guest_id, values=(guest.name, guest.address, guest.contact_details))

        # Delete Guest button
        delete_guest_button = tk.Button(guest_tree_frame, text="Delete Guest", command=self.delete_guest)
        delete_guest_button.pack(side=tk.RIGHT, padx=5, pady=5)

    # Search for a guest
    def search_guest(self):
        # Get the guest ID from the entry field
        guest_id = self.guest_search_entry.get()
        if guest_id:
            if guest_id in self.guests:
                # If guest found, retrieve its details from the guests dictionary
                guest = self.guests[guest_id]
                # Display guest details in a message box
                messagebox.showinfo("Guest found!",
                    f"Guest ID: {guest_id}\n"
                    f"Name: {guest.name}\n"
                    f"Address: {guest.address}\n"
                    f"Contact Details: {guest.contact_details}")
            else:
                # If guest not found, display a message
                messagebox.showinfo("Not Found", f"No guest found with ID: {guest_id}")
        else:
            # If no guest ID provided, show an error message
            messagebox.showerror("Error", "Please enter a guest ID to search.")

    # Delete a guest
    def delete_guest(self):
        selected_item = self.guest_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a guest to delete.")
            return

        guest_id = self.guest_tree.item(selected_item, "text")
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete guest with ID: {guest_id}?")
        if confirm:
            del self.guests[guest_id]
            Guest.save_guests(self.guests)
            messagebox.showinfo("Success", "Guest deleted successfully.")

            # Refresh guest records tree view
            self.guest_tree.delete(selected_item)
        else:
            return

    # Add a new guest
    def add_guest(self):
        guest_id = self.guest_id_entry.get()
        name = self.guest_name_entry.get()
        address = self.guest_address_entry.get()
        contact_details = self.guest_contact_entry.get()

        if guest_id and name and address and contact_details:
            try:
                new_guest = Guest(guest_id, name, address, contact_details)
                self.guests[guest_id] = new_guest
                Guest.save_guests(self.guests)
                messagebox.showinfo("Success", "Guest details added successfully.")

                # Clear input fields
                self.guest_id_entry.delete(0, tk.END)
                self.guest_name_entry.delete(0, tk.END)
                self.guest_address_entry.delete(0, tk.END)
                self.guest_contact_entry.delete(0, tk.END)

                # Refresh guest records tree view
                self.refresh_guest_tree()
            except ValueError as ve:
                messagebox.showerror("Error", f"Failed to add guest: {ve}")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    # Refresh the guest treeview
    def refresh_guest_tree(self):
        self.guest_tree.delete(*self.guest_tree.get_children())
        for guest_id, guest in self.guests.items():
            self.guest_tree.insert("", "end", text=guest_id, values=(guest.name, guest.address, guest.contact_details))
    
    
    # Define method to create supplier tab
    def create_supplier_tab(self):
        # Create a frame for the supplier tab
        supplier_tab = ttk.Frame(self.notebook)
        self.notebook.add(supplier_tab, text="Suppliers")

        # Add widgets for supplier management
        supplier_frame = ttk.LabelFrame(supplier_tab, text="Add / Modify Supplier")
        supplier_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Add entry fields for supplier details
        # Labels for entry fields
        tk.Label(supplier_frame, text="Supplier ID:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(supplier_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(supplier_frame, text="Address:").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(supplier_frame, text="Contact Details:").grid(row=3, column=0, padx=5, pady=5)
        # Entry fields
        self.supplier_id_entry = tk.Entry(supplier_frame)
        self.supplier_id_entry.grid(row=0, column=1, padx=5, pady=5)
        self.supplier_name_entry = tk.Entry(supplier_frame)
        self.supplier_name_entry.grid(row=1, column=1, padx=5, pady=5)
        self.supplier_address_entry = tk.Entry(supplier_frame)
        self.supplier_address_entry.grid(row=2, column=1, padx=5, pady=5)
        self.supplier_contact_entry = tk.Entry(supplier_frame)
        self.supplier_contact_entry.grid(row=3, column=1, padx=5, pady=5)
        # Add / Modify Supplier button
        add_supplier_button = tk.Button(supplier_frame, text="Add / Modify Supplier", command=self.add_supplier)
        add_supplier_button.grid(row=4, columnspan=2, padx=5, pady=5)

        # Add search bar
        supplier_search_frame = ttk.LabelFrame(supplier_tab, text="Search Supplier by ID")
        supplier_search_frame.pack(padx=10, pady=10, fill=tk.BOTH)

        self.supplier_search_entry = tk.Entry(supplier_search_frame)
        self.supplier_search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        search_supplier_button = tk.Button(supplier_search_frame, text="Search", command=self.search_supplier_by_id)
        search_supplier_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Treeview for displaying supplier records
        supplier_tree_frame = ttk.LabelFrame(supplier_tab, text="Supplier Records")
        supplier_tree_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.supplier_tree = ttk.Treeview(supplier_tree_frame, columns=("Name", "Address", "Contact Details"), selectmode="browse")
        self.supplier_tree.pack(fill="both", expand=True)

        # Configure column headings
        self.supplier_tree.heading("#0", text="Supplier ID")
        self.supplier_tree.heading("Name", text="Name")
        self.supplier_tree.heading("Address", text="Address")
        self.supplier_tree.heading("Contact Details", text="Contact Details")

        # Insert supplier records into the treeview
        for supplier_id, supplier in self.suppliers.items():
            self.supplier_tree.insert("", "end", text=supplier_id, values=(supplier.name, supplier.address, supplier.contact_details))

        # Delete Supplier button
        delete_supplier_button = tk.Button(supplier_tree_frame, text="Delete Supplier", command=self.delete_supplier)
        delete_supplier_button.pack(side=tk.RIGHT, padx=5, pady=5)

    # Define method to delete a supplier
    def delete_supplier(self):
        # Get the selected item from the treeview
        selected_item = self.supplier_tree.selection()
        # Check if an item is selected
        if not selected_item:
            messagebox.showerror("Error", "Please select a supplier to delete.")
            return

        # Get the supplier ID from the selected item
        supplier_id = self.supplier_tree.item(selected_item, "text")
        # Ask for confirmation before deletion
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete supplier with ID: {supplier_id}?")
        # If user confirms deletion
        if confirm:
            # Delete the supplier from the dictionary
            del self.suppliers[supplier_id]
            # Save the updated supplier data
            Supplier.save_suppliers(self.suppliers)
            # Show success message
            messagebox.showinfo("Success", "Supplier deleted successfully.")

            # Refresh supplier records tree view
            self.supplier_tree.delete(selected_item)
        else:
            return

    # Define method to add a new supplier
    def add_supplier(self):
        # Get supplier details from entry fields
        supplier_id = self.supplier_id_entry.get().strip()
        name = self.supplier_name_entry.get().strip()
        address = self.supplier_address_entry.get().strip()
        contact_details = self.supplier_contact_entry.get().strip()

        # Validate input fields
        if not all([supplier_id, name, address, contact_details]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            # Create a new supplier object
            new_supplier = Supplier(supplier_id, name, address, contact_details)
            # Add the new supplier to the dictionary
            self.suppliers[supplier_id] = new_supplier
            # Save the updated supplier data
            Supplier.save_suppliers(self.suppliers)
            # Show success message
            messagebox.showinfo("Success", "Supplier details added successfully.")
            # Clear input fields
            self.supplier_id_entry.delete(0, tk.END)
            self.supplier_name_entry.delete(0, tk.END)
            self.supplier_address_entry.delete(0, tk.END)
            self.supplier_contact_entry.delete(0, tk.END)

            # Refresh supplier records tree view
            self.refresh_supplier_tree()
            
        except ValueError as ve:
            # Handle ValueError raised during object creation
            messagebox.showerror("Error", f"Failed to add supplier: {ve}")
        except Exception as e:
            # Handle other exceptions during object creation
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # Define method to refresh the supplier tree view
    def refresh_supplier_tree(self):
        # Clear existing entries in the tree view
        self.supplier_tree.delete(*self.supplier_tree.get_children())
        # Insert updated supplier records into the treeview
        for supplier_id, supplier in self.suppliers.items():
            self.supplier_tree.insert("", "end", text=supplier_id, values=(supplier.name, supplier.address, supplier.contact_details))

    # Define method to search for a supplier by ID
    def search_supplier_by_id(self):
        # Get the supplier ID from the entry field
        supplier_id = self.supplier_search_entry.get().strip()
        if supplier_id:
            if supplier_id in self.suppliers:
                # If supplier found, retrieve its details from the suppliers dictionary
                supplier = self.suppliers[supplier_id]
                # Display supplier details in a message box
                messagebox.showinfo("Supplier found!",
                    f"Supplier ID: {supplier_id}\n"
                    f"Name: {supplier.name}\n"
                    f"Address: {supplier.address}\n"
                    f"Contact Details: {supplier.contact_details}")
            else:
                # If supplier not found, display a message
                messagebox.showinfo("Not Found", f"No supplier found with ID: {supplier_id}")
        else:
            # If no supplier ID provided, show an error message
            messagebox.showerror("Error", "Please enter a supplier ID to search.")

            
            
    # Define method to create the venue tab
    def create_venue_tab(self):
        # Create a frame for the venue tab
        venue_tab = ttk.Frame(self.notebook)
        self.notebook.add(venue_tab, text="Venues")

        # Add widgets for venue management
        venue_frame = ttk.LabelFrame(venue_tab, text="Add / Modify Venue")
        venue_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Add entry fields for venue details
        # Labels for entry fields
        tk.Label(venue_frame, text="Venue ID:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(venue_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(venue_frame, text="Address:").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(venue_frame, text="Contact:").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(venue_frame, text="Min Guests:").grid(row=4, column=0, padx=5, pady=5)
        tk.Label(venue_frame, text="Max Guests:").grid(row=5, column=0, padx=5, pady=5)
        # Entry fields
        self.venue_id_entry = tk.Entry(venue_frame)
        self.venue_id_entry.grid(row=0, column=1, padx=5, pady=5)
        self.venue_name_entry = tk.Entry(venue_frame)
        self.venue_name_entry.grid(row=1, column=1, padx=5, pady=5)
        self.venue_address_entry = tk.Entry(venue_frame)
        self.venue_address_entry.grid(row=2, column=1, padx=5, pady=5)
        self.venue_contact_entry = tk.Entry(venue_frame)
        self.venue_contact_entry.grid(row=3, column=1, padx=5, pady=5)
        self.venue_min_guests_entry = tk.Entry(venue_frame)
        self.venue_min_guests_entry.grid(row=4, column=1, padx=5, pady=5)
        self.venue_max_guests_entry = tk.Entry(venue_frame)
        self.venue_max_guests_entry.grid(row=5, column=1, padx=5, pady=5)
        # Button to add or modify venue
        add_venue_button = tk.Button(venue_frame, text="Add / Modify Venue", command=self.add_venue)
        add_venue_button.grid(row=6, columnspan=2, padx=5, pady=5)

        # Add search bar
        venue_search_frame = ttk.LabelFrame(venue_tab, text="Search Venue by ID")
        venue_search_frame.pack(padx=10, pady=10, fill=tk.BOTH)

        self.venue_search_entry = tk.Entry(venue_search_frame)
        self.venue_search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        search_venue_button = tk.Button(venue_search_frame, text="Search", command=self.search_venue_by_id)
        search_venue_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Treeview for displaying venue records
        venue_tree_frame = ttk.LabelFrame(venue_tab, text="Venue Records")
        venue_tree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.venue_tree = ttk.Treeview(venue_tree_frame, columns=("Name", "Address", "Contact", "Min Guests", "Max Guests"), selectmode="browse")
        self.venue_tree.pack(fill="both", expand=True)

        # Configure column headings
        self.venue_tree.heading("#0", text="Venue ID")
        self.venue_tree.heading("Name", text="Name")
        self.venue_tree.heading("Address", text="Address")
        self.venue_tree.heading("Contact", text="Contact")
        self.venue_tree.heading("Min Guests", text="Min Guests")
        self.venue_tree.heading("Max Guests", text="Max Guests")

        # Insert venue records into the treeview
        for venue_id, venue in self.venues.items():
            self.venue_tree.insert("", "end", text=venue_id, values=(venue.name, venue.address, venue.contact, venue.min_guests, venue.max_guests))
        
        # Button to delete venue
        delete_venue_button = tk.Button(venue_tree_frame, text="Delete Venue", command=self.delete_venue)
        delete_venue_button.pack(side=tk.RIGHT, padx=5, pady=5)


    # Define method to search for a venue by ID
    def search_venue_by_id(self):
        # Get the venue ID from the entry field
        venue_id = self.venue_search_entry.get()
        if venue_id:
            if venue_id in self.venues:
                # If venue found, retrieve its details from the venues dictionary
                venue = self.venues[venue_id]
                # Display venue details in a message box
                messagebox.showinfo("Venue found!",
                    f"Venue ID: {venue_id}\n"
                    f"Name: {venue.name}\n"
                    f"Address: {venue.address}\n"
                    f"Contact: {venue.contact}\n"
                    f"Min Guests: {venue.min_guests}\n"
                    f"Max Guests: {venue.max_guests}")
            else:
                # If venue not found, display a message
                messagebox.showinfo("Not Found", f"No venue found with ID: {venue_id}")
        else:
            # If no venue ID provided, show an error message
            messagebox.showerror("Error", "Please enter a venue ID to search.")

    # Define method to add a new venue
    def add_venue(self):
        # Get venue details from entry fields
        venue_id = self.venue_id_entry.get().strip()
        name = self.venue_name_entry.get().strip()
        address = self.venue_address_entry.get().strip()
        contact = self.venue_contact_entry.get().strip()
        min_guests = self.venue_min_guests_entry.get().strip()
        max_guests = self.venue_max_guests_entry.get().strip()

        # Validate input fields
        if not all([venue_id, name, address, contact, min_guests, max_guests]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            # Create a new venue object
            new_venue = Venue(venue_id, name, address, contact, int(min_guests), int(max_guests))
            # Add the new venue to the dictionary
            self.venues[venue_id] = new_venue
            # Save the updated venue data
            Venue.save_venues(self.venues)
            # Show success message
            messagebox.showinfo("Success", "Venue details added successfully.")
            # Clear input fields
            self.venue_id_entry.delete(0, tk.END)
            self.venue_name_entry.delete(0, tk.END)
            self.venue_address_entry.delete(0, tk.END)
            self.venue_contact_entry.delete(0, tk.END)
            self.venue_min_guests_entry.delete(0, tk.END)
            self.venue_max_guests_entry.delete(0, tk.END)

            # Refresh venue records tree view
            self.refresh_venue_tree()
            
        except ValueError as ve:
            # Handle ValueError raised during object creation
            messagebox.showerror("Error", f"Failed to add venue: {ve}")
        except Exception as e:
            # Handle other exceptions during object creation
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")


    # Define method to delete a venue
    def delete_venue(self):
        # Check if a venue is selected
        selected_item = self.venue_tree.selection()
        if not selected_item:
            # If no venue is selected, show an error message
            messagebox.showerror("Error", "Please select a venue to delete.")
            return

        # Get the ID of the selected venue
        venue_id = self.venue_tree.item(selected_item, "text")
        # Ask for confirmation before deleting
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete venue with ID: {venue_id}?")
        if confirm:
            # If confirmed, delete the venue from the dictionary
            del self.venues[venue_id]
            # Save the updated venue data
            Venue.save_venues(self.venues)
            # Show success message
            messagebox.showinfo("Success", "Venue deleted successfully.")

            # Refresh venue records tree view
            self.refresh_venue_tree()

    # Define method to refresh the venue tree view
    def refresh_venue_tree(self):
        # Clear existing entries in the tree view
        self.venue_tree.delete(*self.venue_tree.get_children())
        # Insert updated venue records into the treeview
        for venue_id, venue in self.venues.items():
            self.venue_tree.insert("", "end", text=venue_id, values=(venue.name, venue.address, venue.contact, venue.min_guests, venue.max_guests))

    # Define method to create the event tab
    def create_event_tab(self):
        # Create a frame for the event tab
        event_tab = ttk.Frame(self.notebook)
        self.notebook.add(event_tab, text="Events")

        # Add widgets for event management
        event_frame = ttk.LabelFrame(event_tab, text="Add / Modify Event")
        event_frame.pack(padx=10, pady=10, fill=tk.BOTH)

        # Add entry fields for event details
        tk.Label(event_frame, text="Event ID:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(event_frame, text="Type:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(event_frame, text="Theme:").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(event_frame, text="Date:").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(event_frame, text="Time:").grid(row=4, column=0, padx=5, pady=5)
        tk.Label(event_frame, text="Duration:").grid(row=5, column=0, padx=5, pady=5)
        tk.Label(event_frame, text="Venue Address:").grid(row=6, column=0, padx=5, pady=5)
        tk.Label(event_frame, text="Client ID:").grid(row=7, column=0, padx=5, pady=5)
        tk.Label(event_frame, text="Guest List:").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(event_frame, text="Catering Company:").grid(row=1, column=2, padx=5, pady=5)
        tk.Label(event_frame, text="Cleaning Company:").grid(row=2, column=2, padx=5, pady=5)
        tk.Label(event_frame, text="Decorations Company:").grid(row=3, column=2, padx=5, pady=5)
        tk.Label(event_frame, text="Entertainment Company:").grid(row=4, column=2, padx=5, pady=5)
        tk.Label(event_frame, text="Furniture Supply Company:").grid(row=5, column=2, padx=5, pady=5)
        tk.Label(event_frame, text="Invoice:").grid(row=6, column=2, padx=5, pady=5)

        # Entry fields
        self.event_id_entry = tk.Entry(event_frame)
        self.event_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Use OptionMenu for event type with predefined options
        self.selected_event_type = tk.StringVar(event_frame)
        self.selected_event_type.set(EventType.WEDDING.value)  # Default value
        event_type_options = [e.value for e in EventType]
        event_type_menu = tk.OptionMenu(event_frame, self.selected_event_type, *event_type_options)
        event_type_menu.grid(row=1, column=1, padx=5, pady=5)

        # Other entry fields
        self.theme_entry = tk.Entry(event_frame)
        self.theme_entry.grid(row=2, column=1, padx=5, pady=5)
        self.date_entry = tk.Entry(event_frame)
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)
        self.time_entry = tk.Entry(event_frame)
        self.time_entry.grid(row=4, column=1, padx=5, pady=5)
        self.duration_entry = tk.Entry(event_frame)
        self.duration_entry.grid(row=5, column=1, padx=5, pady=5)
        self.venue_entry = tk.Entry(event_frame)
        self.venue_entry.grid(row=6, column=1, padx=5, pady=5)
        self._client_id_entry = tk.Entry(event_frame)
        self._client_id_entry.grid(row=7, column=1, padx=5, pady=5)
        self.guest_list_entry = tk.Entry(event_frame)
        self.guest_list_entry.grid(row=0, column=3, padx=5, pady=5)
        self.catering_entry = tk.Entry(event_frame)
        self.catering_entry.grid(row=1, column=3, padx=5, pady=5)
        self.cleaning_entry = tk.Entry(event_frame)
        self.cleaning_entry.grid(row=2, column=3, padx=5, pady=5)
        self.decorations_entry = tk.Entry(event_frame)
        self.decorations_entry.grid(row=3, column=3, padx=5, pady=5)
        self.entertainment_entry = tk.Entry(event_frame)
        self.entertainment_entry.grid(row=4, column=3, padx=5, pady=5)
        self.furniture_entry = tk.Entry(event_frame)
        self.furniture_entry.grid(row=5, column=3, padx=5, pady=5)
        self.invoice_entry = tk.Entry(event_frame)
        self.invoice_entry.grid(row=6, column=3, padx=5, pady=5)

        # Button to add or modify event
        add_event_button = tk.Button(event_frame, text="Add / Modify Event", command=self.add_event)
        add_event_button.grid(row=8, columnspan=2, padx=5, pady=5)

        # Add search bar for event ID
        search_event_frame = ttk.LabelFrame(event_tab, text="Search Event")
        search_event_frame.pack(padx=10, pady=10, fill=tk.BOTH)

        tk.Label(search_event_frame, text="Search by ID:").pack(side=tk.LEFT, padx=5, pady=5)
        self.event_search_entry = tk.Entry(search_event_frame)
        self.event_search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        search_event_button = tk.Button(search_event_frame, text="Search", command=self.search_event)
        search_event_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Treeview for displaying event records
        event_tree_frame = ttk.LabelFrame(event_tab, text="Event Records")
        event_tree_frame.pack(padx=5, pady=5, fill=tk.BOTH)

        self.event_tree = ttk.Treeview(event_tree_frame, columns=("Type", "Theme", "Date", "Time", "Duration", "Venue Address", "Client ID", "Guest List", "Catering Company", "Cleaning Company", "Decorations Company", "Entertainment Company", "Furniture Supply Company", "Invoice"), selectmode="browse", height=5)
        self.event_tree.pack(fill="both")
        
        # Configure column headings
        self.event_tree.heading("#0", text="ID")
        self.event_tree.heading("Type", text="Type")
        self.event_tree.heading("Theme", text="Theme")
        self.event_tree.heading("Date", text="Date")
        self.event_tree.heading("Time", text="Time")
        self.event_tree.heading("Duration", text="Duration")
        self.event_tree.heading("Venue Address", text="Venue Address")
        self.event_tree.heading("Client ID", text="Client ID")
        self.event_tree.heading("Guest List", text="Guest List")
        self.event_tree.heading("Catering Company", text="Catering Company")
        self.event_tree.heading("Cleaning Company", text="Cleaning Company")
        self.event_tree.heading("Decorations Company", text="Decorations Company")
        self.event_tree.heading("Entertainment Company", text="Entertainment Company")
        self.event_tree.heading("Furniture Supply Company", text="Furniture Supply Company")
        self.event_tree.heading("Invoice", text="Invoice")

        # Insert event records into the treeview
        for event_id, event in self.events.items():
            self.event_tree.insert("", "end", text=event_id, values=(event.event_type, event.theme, event.date, event.time, event.duration, event.venue_address, event.client_id, event.guest_list, event.catering_company, event.cleaning_company, event.decorations_company, event.entertainment_company, event.furniture_supply_company, event.invoice))

        # Button to delete event
        delete_event_button = tk.Button(event_tree_frame, text="Delete Event", command=self.delete_event)
        delete_event_button.pack(side=tk.RIGHT, padx=5, pady=5)
         
                                 
    # Function to search for an event
    def search_event(self):
        # Get the event ID from the entry field
        event_id = self.event_search_entry.get()
        if event_id:
            if event_id in self.events:
                # If event found, retrieve its details from the events dictionary
                event = self.events[event_id]
                # Display event details in a message box
                messagebox.showinfo("Event found!",
                    f"Event ID: {event_id}\n"
                    f"Type: {event.event_type}\n"
                    f"Theme: {event.theme}\n"
                    f"Date: {event.date}\n"
                    f"Time: {event.time}\n"
                    f"Duration: {event.duration}\n"
                    f"Venue Address: {event.venue_address}\n"
                    f"Client ID: {event.client_id}\n"
                    f"Guest List: {event.guest_list}\n"
                    f"Catering Company: {event.catering_company}\n"
                    f"Cleaning Company: {event.cleaning_company}\n"
                    f"Decorations Company: {event.decorations_company}\n"
                    f"Entertainment Company: {event.entertainment_company}\n"
                    f"Furniture Supply Company: {event.furniture_supply_company}\n"
                    f"Invoice: {event.invoice}")
            else:
                # If event not found, display a message
                messagebox.showinfo("Not Found", f"No event found with ID: {event_id}")
        else:
            # If no event ID provided, show an error message
            messagebox.showerror("Error", "Please enter an event ID to search.")

    # Function to add or modify an event
    def add_event(self):
        # Retrieve data from entry fields
        event_id = self.event_id_entry.get()
        event_type = self.selected_event_type.get()
        theme = self.theme_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        duration = self.duration_entry.get()
        venue_address = self.venue_entry.get()
        client_id = self._client_id_entry.get()
        guest_list = self.guest_list_entry.get()
        catering_company = self.catering_entry.get()
        cleaning_company = self.cleaning_entry.get()
        decorations_company = self.decorations_entry.get()
        entertainment_company = self.entertainment_entry.get()
        furniture_supply_company = self.furniture_entry.get()
        invoice = self.invoice_entry.get()

        try:
            # Validate input fields
            if not all([event_id, event_type, theme, date, time, duration, venue_address, client_id, guest_list, catering_company, cleaning_company, decorations_company, entertainment_company, furniture_supply_company, invoice]):
                raise ValueError("Please fill in all fields.")

            # Create the event instance
            self.events[event_id] = Event(event_id, event_type, theme, date, time, int(duration), venue_address, client_id, ast.literal_eval(guest_list), catering_company, cleaning_company, decorations_company, entertainment_company, furniture_supply_company, int(invoice))
            Event.save_events(self.events)
            messagebox.showinfo("Success", "Event details added successfully.")
            
            # Clear input fields
            self.event_id_entry.delete(0, tk.END)
            self.theme_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
            self.duration_entry.delete(0, tk.END)
            self.venue_entry.delete(0, tk.END)
            self._client_id_entry.delete(0, tk.END)
            self.guest_list_entry.delete(0, tk.END)
            self.catering_entry.delete(0, tk.END)
            self.cleaning_entry.delete(0, tk.END)
            self.decorations_entry.delete(0, tk.END)
            self.entertainment_entry.delete(0, tk.END)
            self.furniture_entry.delete(0, tk.END)
            self.invoice_entry.delete(0, tk.END)

            # Refresh event records tree view
            self.refresh_event_tree()
        
        except ValueError as ve:
            # Display error message in messagebox
            messagebox.showerror("Error", str(ve))

        except Exception as e:
            # Display unexpected error in messagebox
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # Function to refresh event records tree view
    def refresh_event_tree(self):
        # Clear existing entries in the tree view
        self.event_tree.delete(*self.event_tree.get_children())
        # Insert updated event records into the treeview
        for event_id, event in self.events.items():
            self.event_tree.insert("", "end", text=event_id, values=(event.event_type, event.theme, event.date, event.time, event.duration, event.venue_address, event.client_id, event.guest_list, event.catering_company, event.cleaning_company, event.decorations_company, event.entertainment_company, event.furniture_supply_company, event.invoice))

    # Function to delete an event
    def delete_event(self):
        selected_item = self.event_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an event to delete.")
            return

        event_id = self.event_tree.item(selected_item, "text")
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete event with ID: {event_id}?")
        if confirm:
            try:
                del self.events[event_id]
                Event.save_events(self.events)
                messagebox.showinfo("Success", "Event deleted successfully.")
                # Refresh event records tree view
                self.refresh_event_tree()
            except Exception as e:
                # Handle deletion error
                messagebox.showerror("Error", f"Failed to delete event: {e}")

if __name__ == "__main__":
    # Create an instance of the EventManagementSystemGUI class
    app = EventManagementSystemGUI()
    # Run the application
    app.mainloop()


# In[ ]:




