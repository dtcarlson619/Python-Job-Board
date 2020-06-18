from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Invalid email address!"
        users = self.filter(email=postData["email"])
        if users:
            errors["email"] = "Email already exists"
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData["password"]) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData["password"] != postData["password_confirm"]:
            errors["password"] = "Passwords do not match"
        return errors

    def loginCheck(self, postData):
        errors = {}
        if not self.filter(email=postData["email"]).exists():
            errors["email"] = "User account does not exist"
        else:
            userpw = User.objects.get(email=postData["email"]).password
            if not bcrypt.checkpw(postData["password"].encode(), userpw.encode()):
                errors["password"] = "Password does not match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.CharField(max_length=55)
    password = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class JobManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors["title"] = "Job title should be at least 3 characters"
        if len(postData['description']) < 3:
            errors["description"] = "Description should be at least 3 characters"
        if len(postData['location']) < 3:
            errors["location"] = "Location should be at least 3 characters"
        return errors

class Job(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="jobs", on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()

