from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid
import qrcode
from io import BytesIO
from django.core.files import File


class UserManager(BaseUserManager):

    def create_user(self, email, name=None, password=None, role='citizen'):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            name=name,
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not password:
            raise ValueError("Superuser must have a password")

        user = self.model(
            email=self.normalize_email(email),
            name="Government Admin",
            role="govt",
            **extra_fields
        )

        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ('citizen', 'Citizen'),
        ('doctor', 'Doctor'),
        ('hospital', 'Hospital'),
        ('govt', 'Government'),
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    unique_health_id = models.CharField(max_length=20, unique=True, blank=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.unique_health_id:
            self.unique_health_id = str(uuid.uuid4())[:12].upper()

        super().save(*args, **kwargs)  # First save to ensure ID exists

        # Generate QR with FULL ACCESS URL
        if not self.qr_code:
            access_url = f"pulseid.onrender.com/citizen/access/{self.unique_health_id}/"

            qr = qrcode.make(access_url)

            buffer = BytesIO()
            qr.save(buffer, format='PNG')

            file_name = f"{self.unique_health_id}.png"

            self.qr_code.save(file_name, File(buffer), save=False)

            super().save(update_fields=['qr_code'])