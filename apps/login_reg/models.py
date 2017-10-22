from __future__ import unicode_literals

from django.db import models

import re

import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager (models.Manager):
    def regvalidation(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = 'Enter your First name'
        elif len(postData['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters'
        elif not postData['first_name'].isalpha():
            errors['first_name'] = 'First name must contain letters only'

        if len(postData['last_name']) < 1:
            errors['last_name'] = 'Enter your Last name'
        elif len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters'
        elif not postData['last_name'].isalpha():
            errors['last_name'] = 'Last name must contain letters only'

        if len(postData['email']) < 1:
            errors['email'] = 'Must enter a valid email'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email is not valid'

        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        elif postData['password'] != postData['cpassword']:
            errors['password'] = 'Passwords must match'

        if not errors:
            user_list = self.filter(email = postData['email'])
            if user_list:
                errors['email'] = 'Email already in use'

        return errors

    def newUser(self, post):
        email = post['email'].lower()
        password = bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt())
        Fname = post['first_name']
        Lname = post['last_name']
        return self.create(email = email, password = password, first_name = Fname, last_name = Lname)


    def login(self,post):#this is getting all the stuff from your form for checking
        email = post['email'].lower() #this gets the login email and stores it into a variable
        users = self.filter(email = email) #this queries the database and returns a list of emails that match the email that was passed in    
        if users: #if that list has users, take the first one (because we expect the lsit to only have one dude)
            user = users[0] #set the first dude to a user variable
            if bcrypt.checkpw(post['password'].encode(), user.password.encode()): #if you found an email address, then do a check using bcrypty
                return user #you want to return the user to the function so that they can parse their stuff and display on the template
        return False #else, you messed up

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    cpassword = models.CharField(max_length = 255)
    objects = UserManager()

    def  __str__(self):
        return "First name: {}/ Last name: {}/ Email: {}/".format(self.first_name, self.last_name, self.email)
        



