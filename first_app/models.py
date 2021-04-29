from django.db import models
from datetime import datetime, timedelta
import re
from ckeditor.fields import RichTextField
import bcrypt



class UserManager(models.Manager):

    def basic_validator(self, post_data):
        errors = {}

        email_regex = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        year = datetime.now() - timedelta(weeks = 676)

        if not email_regex.match(post_data["email"]):
            errors["email"] = "Email is invalid."

        if post_data["username"] == "" or len(post_data["username"]) < 2 or len(post_data["username"]) > 50:
            errors["username"] = "Username is invalid."



        if post_data["email"] == "" or len(post_data["email"]) < 2 or len(post_data["email"]) > 50:
            errors["email"] = "Email is invalid."
        if post_data["pw"] == "" or len(post_data["pw"]) < 8 or len(post_data["pw"]) > 50:
            errors["pw"] = "Password should be at least 8 characters."
        if post_data["pw"] != post_data["confirm_pw"]:
            errors["confirm_pw"] = "Password and confirm password should match."

        if post_data["date"] == '' or datetime.strptime(post_data["date"], '%Y-%m-%d') > year:
            errors["date"] = "Must be at least 13 years old to register."

        try:
            self.get(email=post_data["email"])
            errors["email"] = "Email already in use."
        except:
            pass

        try:
            self.get(username=post_data["username"])
            errors["username"] = "Username already in use."
        except:
            pass
        return errors
    
    def update_info_validator(self, post_data, user_id):
        errors = {}

        email_regex = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        year = datetime.now() - timedelta(weeks = 676)

        if not email_regex.match(post_data["email"]):
            errors["email"] = "Email is invalid"

        if post_data["username"] == "" or len(post_data["username"]) < 2 or len(post_data["username"]) > 50:
            errors["username"] = "Username should have 2 characters to 50 characters long."
        if post_data["email"] == "" or  len(post_data["email"]) > 50:
            errors["email"] = "Email can't exceed more than 50 characters long"
        if post_data["date"] == '' or datetime.strptime(post_data["date"], '%Y-%m-%d') > year:
            errors["date"] = "Must be at least 13 years old to register"

        this_user_email = User.objects.get(id = user_id).email
        if post_data['email'] != this_user_email:
            this_email = User.objects.filter(email = post_data['email'])
            if len(this_email) > 0:
                errors['email'] = 'Email already exists.'

        this_username = User.objects.get(id = user_id).username
        if post_data['username'] != this_user_email:
            this_username = User.objects.filter(username = post_data['username'])
            if len(this_username) > 0:
                errors['username'] = 'Username already in use.'

        return errors

    def update_password_validator(self, post_data, user_id):
        errors = {}

        user = User.objects.get(id = user_id)
        if len(post_data['current_pw']) < 8 or len(post_data['current_pw']) == '':
            errors['current_pw'] = "Your current password doesn't match."
            if not bcrypt.checkpw(post_data['current_pw'].encode(), user.password.encode()):
                errors['current_pw'] = "Your current password doesn't match."
    
        if len(post_data['new_pw']) < 8:
            errors["new_pw"] = "New password should be at least 8 characters."

        if post_data['new_pw'] != '':
            if post_data["new_pw"] == "" or len(post_data["new_pw"]) < 8:
                errors["new_pw"] = "New password should be at least 8 characters."
            if post_data["new_pw"] != post_data["confirm_pw"]:
                errors["confirm_pw"] = "New password and confirm password should match."
    
        return errors

class RecipeImageManager(models.Manager):
    def image_validator(self, post_data):
        errors = {}

        if len(post_data) == 0:
            errors['images'] = 'Please upload at least one image of the recipe.'

        return errors

class RecipeManager(models.Manager):
    def recipe_validator(self, post_data):
        errors = {}

        if len(post_data['content']) < 500:
            errors['content'] = "Recipe content is too short. Content should have at least 500 characters."

        return errors

class User(models.Model):
    username = models.CharField(max_length = 50, unique = True)
    email = models.CharField(max_length = 384, unique = True)
    password = models.CharField(max_length = 60)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

class Recipe(models.Model):
    title = models.CharField(max_length = 50)
    content = RichTextField(config_name='awesome_ckeditor')
    uploader = models.ForeignKey(User, related_name = 'recipes', on_delete = models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name = 'liked_recipes')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = RecipeManager()


class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe, related_name = 'images', on_delete = models.CASCADE)
    image = models.ImageField(upload_to='images/')

    objects = RecipeImageManager()