from contextlib import contextmanager
from dotenv import load_dotenv
# from nicegui.elements.mixins.validation_element import ValidationElement
from nicegui import ui
import os
import re
import uuid
import random
import string

load_dotenv()

class HelperFunctions:
    """Helper functions for HRMS operations"""
    
    def generate_id(self) -> str:
        """Generate a unique ID"""
        return str(uuid.uuid4())
    
    def generate_employee_number(self) -> str:
        """Generate a unique employee number"""
        # Generate a random 6-digit employee number
        return f"EMP{random.randint(100000, 999999)}"

def imagePath(filename: str) -> str:
    return os.path.join("assets/images/", filename)

def emailValidation(email: str):
    email_regex= r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.fullmatch(email_regex, email))
#   print(text)
#   if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', text):
#      return True
#   else:
#      return False

def validate_password(password):
    """
    Validates a password against a strong password policy using regex.

    Requires:
    - Minimum 8 characters in length.
    - At least one uppercase English letter.
    - At least one lowercase English letter.
    - At least one digit.
    - At least one special character (from @$!%*#?&).
    """
    # Regex pattern for strong password validation
    # ^ asserts position at the start of the string.
    # (?=.*[a-z]) asserts that the string contains at least one lowercase letter.
    # (?=.*[A-Z]) asserts that the string contains at least one uppercase letter.
    # (?=.*\d) asserts that the string contains at least one digit.
    # (?=.*[@$!%*#?&]) asserts that the string contains at least one specified special character.
    # [A-Za-z\d@$!%*#?&]{8,} matches any allowed character (alphanumeric and specified special characters)
    #   and ensures a minimum length of 6 characters.
    # $ asserts position at the end of the string.
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$"
    
    # re.fullmatch() attempts to match the entire string to the pattern.
    return bool(re.fullmatch(password_regex, password))

def readEnv(key: str) -> str:
   return os.getenv(key)

@contextmanager
def disable_enable_button(button: ui.button):
    button.disable()
    try:
        yield
    finally:
        button.enable()

class Toggle_Boolean:
    def __init__(self):
        self.is_visible = False
        self.visible = True
        self.isChecked = False
        self.activeSearch = False
        self.isActive = -1
        
    def toggle(self):
        self.is_visible = not self.is_visible
        self.visible = not self.visible

    # if val: return True
    # else: return False
# userModel Class
# from pydantic import BaseModel, EmailStr, ValidationError, validator
# class UserFormModel(BaseModel):
#     name: str
#     age: int
#     email: EmailStr

#     @validator('name')
#     def name_must_be_alpha(cls, value):
#         if not value.replace(" ", "").isalpha():
#             raise ValueError("Name must only contain letters")
#         return value

#     @validator('age')
#     def age_must_be_positive(cls, value):
#         if value <= 0:
#             raise ValueError("Age must be a positive number")
#         return value

# form
# from pydantic import ValidationError
# from models import UserFormModel

# name_input = ui.input(label='Name').classes('w-full')
# age_input = ui.number(label='Age').classes('w-full')
# email_input = ui.input(label='Email').classes('w-full')

# name_error = ui.label().classes('text-red-600 text-sm')
# age_error = ui.label().classes('text-red-600 text-sm')
# email_error = ui.label().classes('text-red-600 text-sm')

# def reset_form():
#     name_input.value = ''
#     age_input.value = None
#     email_input.value = ''
#     name_error.text = ''
#     age_error.text = ''
#     email_error.text = ''
#     ui.notify('Form reset successfully.', color='blue')

# def validate_and_submit():
#     name_error.text = ''
#     age_error.text = ''
#     email_error.text = ''

#     try:
#         user = UserFormModel(
#             name=name_input.value,
#             age=int(age_input.value) if age_input.value is not None else None,
#             email=email_input.value
#         )
#         ui.notify('Form submitted successfully!', color='green')
#     except ValidationError as e:
#         for error in e.errors():
#             field = error['loc'][0]
#             msg = error['msg']
#             if field == 'name':
#                 name_error.text = msg
#             elif field == 'age':
#                 age_error.text = msg
#             elif field == 'email':
#                 email_error.text = msg
#         ui.notify('Please correct the highlighted fields.', color='red')

# # Buttons: Submit and Reset
# with ui.row().classes('justify-between w-full mt-4'):
#     ui.button('Submit', on_click=validate_and_submit).classes('bg-green-600 text-white')
#     ui.button('Reset', on_click=reset_form).classes('bg-gray-300 text-black')