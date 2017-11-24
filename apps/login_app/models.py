from __future__ import unicode_literals
from django.db import models
import bcrypt # to hash the password
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from datetime import date, datetime

# # Create your models here.
# def check_string(string):
#         for char in string: # iterate through the string
#             if not char.isalpha():
#                 return True # if character is not a letter, returns true (true that it's not proper)
#         return False
def checkBirthday(strbday): # function to check if entered birthday is from the future
    # set bday and today variable to match type and format
    bday = datetime.strptime(str(strbday), '%Y-%m-%d').date()
    today = date.today()
    if bday<today: # if bday is greater than today this is (future)
        return True # returns true (is from future)
    return False # otherwise returns false


class UserManager(models.Manager):
    def user_validator(self, postData): # for creating user
        errors = [] # empty error list
        if len(postData['name'])<2: # if first name is less than 2 characters
            errors.append("Please enter your name !")
        if not re.match("^[A-z][A-z|\.|\s]+$", postData['name']): # if first name contains other chars
            errors.append("Please enter a valid name !")
        if len(postData['username'])<2: # if first name is less than 2 characters
            errors.append("Please enter your Username!")
        if not re.match("^[A-z][A-z|\.|\s]+$", postData['username']): # if alias  contains other chars
            errors.append("Please enter a valid Username !")
        try: # while validate_email doesn't throw errors
            validate_email(postData['email']) # check if email is valid
            # this will check if email input is empty or in proper form (---@---.com)
        except ValidationError: # if it throws an error
            errors.append("Please enter valid email address !")
        if len(self.filter(email=postData['email'])): # check if email already exists
            errors.append("User with that email already exists !")
        if len(postData['password'])<8: # check if password is longer than 8 characters
            errors.append("Password should be at least 8 characters !")
        elif postData['password']!=postData['c_password']: # checks if password and c_password matches
            errors.append("Password doesn't match !")
        elif postData['password'].lower()=='password': # check if password is 'password'
            errors.append(" Your password cannot be word 'password' try something different ... !")
        if not postData['bday']: # if no bday was added
            errors.append("Please enter hire date !")
        elif checkBirthday(postData['bday']): # if birthday entered is future date
            errors.append("You can't be hired in the past!")
        return errors # returns the errors list

    def create_user(self, postData): # to create users
        # set each variable to according post data
        name = postData['name']
        username = postData['username']
        email = postData['email']
        birthday = postData['bday']
        # hash the password
        password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        # return the newly created user
        return self.create(name=name, username=username , email=email, password=password, birthday=birthday)

    def login_validator(self, postData): # validates login
        result = {'errors':[], 'user':None} # empty dictionary with keys 'errors' and 'user'
        matched_user = self.filter(email=postData['email']) # filters the user with the same email address
        if not len(postData['password']): # if password wasn't entered
            result['errors'].append('Please enter your password')
        if not len(postData['email']): # if email wasn't entered
            result['errors'].append('Please enter your email')
        elif not len(matched_user): # if no user was returned with that email
            result['errors'].append('No matching email')
        # if password doesn't match the user's password
        elif not bcrypt.checkpw(postData['password'].encode(), matched_user[0].password.encode()):
            result['errors'].append('No matching email') #append an object to the end of the list
        else: # if no errors
            result['user'] = matched_user[0] # set 'user' in dictionary to that matched user object
        return result # return result

class User(models.Model): #User class
    name = models.CharField(max_length = 200) #stores name
    username = models.CharField(max_length = 200) #stores name
    email = models.CharField(max_length = 200) #stores the email
    password = models.CharField(max_length = 200) #stores hashed pw
    birthday = models.DateField(auto_now_add=False, auto_now=False)
    created_at = models.DateTimeField(auto_now_add=True) # date/time user was created
    updated_at = models.DateTimeField(auto_now=True) # date/time user's info was updated
    objects = UserManager() # this is for Validation
