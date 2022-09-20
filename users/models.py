from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


# Create your models here.
class UserManager(BaseUserManager):
    """
        User Account Manger
    """

    def create_user(self, first_name, last_name, email, password=None):
        """
            Creates and Saves a User with the Given Firest Name, Last Name, Email and Password.
        """
        if not email:
            raise ValueError("Users Must Have an Valid Email Address")

        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email.lower()
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,  first_name, last_name, email, password=None):
        """
            Creates and Saves a User with the Given Firest Name, Last Name, Email and Password.
        """
        user = self.create_user(
            first_name,
            last_name,
            email,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
        User Account
    """
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email
