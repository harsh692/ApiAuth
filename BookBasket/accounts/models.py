from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# custom user model 

# Copied usermanager from docs

# class MyUserManager(BaseUserManager):
#     def create_user(self, email, phone,location, password=None, password2=None):
#         """
#         Creates and saves a User with the given email, phone,location
#         and password.
#         """
#         if not email:
#             raise ValueError("Users must have an email address")

#         user = self.model(
#             email=self.normalize_email(email),
#             phone=phone,
#             location=location
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, phone,location, password=None):
#         """
#         Creates and saves a superuser with the given email, phone,location
#         and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#             phone=phone,
#             location=location
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

# # Copied main user model class from docs

# class User(AbstractBaseUser):
#     email = models.EmailField(
#         verbose_name="email address",
#         max_length=255,
#         unique=True,
#     )
#     phone = models.DecimalField(max_digits=10,decimal_places=0,null=True,blank=True)
#     location = models.CharField(max_length = 255,null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)

#     objects = MyUserManager()

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["phone","location"]

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return self.is_admin

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True

#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         # Simplest possible answer: All admins are staff
#         return self.is_admin
# # Create your models here.

# models.py
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, password2=None,**extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    # No REQUIRED_FIELDS here

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255,null=True,blank=True) 
    phone = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return f"Profile for {self.user.email}"

