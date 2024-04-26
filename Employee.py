#!/usr/bin/env python
# coding: utf-8

# In[2]:



import pickle  # Import the pickle module for object serialization
from enum import Enum  # Import Enum class for creating enumerated constants

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


# In[ ]:




