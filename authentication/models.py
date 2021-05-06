from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
PermissionsMixin)

class UserManager(BaseUserManager):
    def create_user(self,email,name, password=None):
        
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,name, password=None):
        if not password:
            raise ValueError("User must have an password")
        if not email:
            raise ValueError("User must have an email address")

        user = self.create_user(
            name=name,
            email=self.normalize_email(email),
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user
        
class User(AbstractBaseUser, PermissionsMixin):
    name=models.CharField(max_length=60)
    email=models.EmailField(unique=True)
    date_joined=models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login=models.DateTimeField(verbose_name="last login", auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['name']
    
    objects = UserManager()

    def __str__(self):
        return self.email

    # generates refresh token and access_token 
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {'refresh':str(refresh),
        'access':str(refresh.access_token)}

    def has_perm(self,perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True