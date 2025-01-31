from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


# Custom Manager
class CustomUserAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, phone_number, username, password=None):
        if not username:
            raise ValueError("username is required")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, phone_number, username, password=None):
        user = self.create_user(first_name, last_name, phone_number, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# Custom User
class CustomUserAccount(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.IntegerField(unique=True)
    username = models.CharField(max_length=255, unique=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']
