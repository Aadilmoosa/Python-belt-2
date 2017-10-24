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


    def login(self,post):
        email = post['email'].lower()
        users = self.filter(email = email)
        if users:
            user = users[0]
            if bcrypt.checkpw(post['password'].encode(), user.password.encode()):
                return user
        return False

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    cpassword = models.CharField(max_length = 255)
    objects = UserManager()

    def  __str__(self):
        return "First name: {}/ Last name: {}/ Email: {}/".format(self.first_name, self.last_name, self.email)

class QuoteManager(models.Manager):
    def validateQuote(self, postData):
        content = postData['content']
        # author = postData['author']

        errors = []

        if len(postData['content']) < 3:
            errors.append('Item name must contain at least 3 characters')
        # if len(postData['author']) < 1:
        #     errors.append('Must enter Author name')
        return errors

    def newQuote(self, post):
        content = post['content']
        # author = post['author']
        created_at = post['created_at']
        return self.create(content = content, author = passauthorword, created_at = created)

class Quote(models.Model):
    content = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255)
    poster = models.ForeignKey(User, related_name = 'authored_quotes')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    favorites = models.ManyToManyField("User", related_name="favorites", default=None)    
    objects = QuoteManager()
    def __str__(self):
        return 'content:{}, author:{}, poster:{}'.format(self.content, self.author, self.poster)