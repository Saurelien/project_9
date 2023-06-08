from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    # extra fields permet de spécifié des champs supplémentaire (date de naissance, numero de telephone).
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse e-mail doit être spécifiée.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.Quelquechose_TEST)
        return user

    def create_superuser(self, email, password=None):
        self.setdefault('is_superuser', True)
        return self.create_user(email, password)


USERNAME_FIELD = 'email'
REQUIRED_FIELDS = ['first_name', 'last_name']


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    username_field = USERNAME_FIELD
    required_fields = REQUIRED_FIELDS

    def get_full_name(self):
        # petit rappel des self du projet 4 :)
        return f"{self.first_name} {self.last_name}"

    # metode de test pour afficher le nom de l'utilsateur
    def get_short_name(self):
        return self.first_name

    def permition(self, permission):
        pass