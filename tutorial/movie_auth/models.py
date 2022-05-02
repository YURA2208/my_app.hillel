from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
# from django.conf import settings
from rest_framework.authtoken.models import Token

# class MyUser(models.Model):
#     user = models.OneToOneField(settings.AUTH_MODEL_USER, on_delete=models.CASCADE,
#                                 verbose_name="USER")
#
#     def __str__(self):
#         return f"{self.user.username}"

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("This is a required field")
        if not username:
            raise ValueError("This is a required field")
        if not dob:
            raise ValueError("This is a required field")
        user = self.model(username=username, email=self.normalize_email(email), dob=dob,)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def get_user_token(self, username, password):
        user = MyUser.objects.get_by_natural_key(username=username)
        if user.check_password(password):
            return Token.objects.get_or_create(user=user)

class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True, null=True)
    email = models.EmailField("Email", max_length=250, unique=True,null=True)
    password = models.CharField("Password", max_length=250, null=True)
    dob = models.DateTimeField("Dob", null=True)
    is_notified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return f"{self.name}"

