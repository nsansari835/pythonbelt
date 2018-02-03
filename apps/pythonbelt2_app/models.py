from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
from datetime import date
LETTER_REGEX = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
DIG_REGEX = re.compile(r".*[0-9].*")

class BeltManager(models.Manager):
    def regvalidator(self, postData, valid):
        errors = {}
        if len(postData["name"]) < 3:
            errors["name"] = "Name must be at least 3 characters!"
        elif DIG_REGEX.match(postData["name"]):
            errors["name"] = "First name cannot contain numbers!"
        if len(postData["username"]) < 3:
            errors['username'] = "User name must be at least 3 characters!"
        elif User.objects.filter(username=postData['username']):
            errors["email"] = "Username already exists!"
        if len(postData['password']) < 8:
            errors["password"] = "Password must be more than 8 characters"
        elif (postData["password"]) != (postData["passwords"]):
            errors["password"] = "Password must match Confirm password!"       
        return errors

    def logvalidator(self, postData, valid):
        errors = {}
        if not User.objects.filter(username=postData["username"]):
            errors["login"] = "Email is not registered"
        elif not User.objects.filter(password=postData["password"]):
            errors["password"] = "Incorrect password"
        return errors

    def tripvalidator(self, postData, valid):
        errors = {}
        start_date = unicode(postData['from_x'])
        date_today = unicode(date.today())
        end_date = unicode(postData['to_x'])
        if len(postData['desc']) < 1:
            errors['description'] = "Please provide a description"
        elif len(postData['destination']) < 1:
            errors['destination'] = "Please provide a destination"
        if len(postData['from_x']) < 8:
            errors['from_x'] = "Please provide a start date"
        elif len(postData['to_x']) < 8:
            errors['to_x'] = "Please provide an end date"
        if start_date <= date_today:
            errors['from_x'] = "Start date must be in the future"
        elif end_date < start_date:
            errors['to_x'] = "End date must be after the start date"
        return errors
        

class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BeltManager()
    def __str__(self):
        user_str = "id: " + str(self.id) + ", name: " + str(self.name) + ", username: " + str(self.username) + ", password: " + str(self.password) + ", created_at: " + str(self.created_at) + ", updated_at " + str(self.updated_at)
        return user_str

class Trip(models.Model):
    destination = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    travelfrom = models.DateField(auto_now=False, auto_now_add=False)
    travelto = models.DateField(auto_now=False, auto_now_add=False)
    user = models.ForeignKey(User, related_name="trips", null=True)
    jointrip = models.ManyToManyField(User, related_name= 'join')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BeltManager()
    def __str__(self):
        trip_str = "id: " + str(self.id) + ", destination: " + str(self.destination) + ", description: " + str(self.description) + ", travelfrom: " + str(self.travelfrom) + ", travelto: " + str(self.travelto) + ", user: " + str(self.user) + ", jointrip: " + str(self.jointrip) + ", created_at: " + str(self.created_at) + ", updated_at " + str(self.updated_at)
        return trip_str 



