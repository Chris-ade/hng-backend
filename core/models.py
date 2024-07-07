from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, userId, firstName, lastName, email, password=None, phone=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not userId:
            raise ValueError('Users must have a user ID')

        user = self.model(
            userId=userId,
            firstName=firstName,
            lastName=lastName,
            email=self.normalize_email(email),
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userId, firstName, lastName, email, password=None):
        user = self.create_user(
            userId=userId,
            firstName=firstName,
            lastName=lastName,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    userId = models.CharField(max_length=255, unique=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['userId', 'firstName', 'lastName']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

class Organization(models.Model):
    orgId = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name='organizations')

    def __str__(self):
        return self.name