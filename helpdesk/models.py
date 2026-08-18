from django.db import models
from django.contrib.auth.models import User


class HardwareAsset(models.Model):

    ASSET_TYPES = [
        ('Laptop', 'Laptop'),
        ('Desktop', 'Desktop'),
        ('Monitor', 'Monitor'),
        ('Keyboard', 'Keyboard'),
        ('Mouse', 'Mouse'),
        ('Other', 'Other'),
    ]

    asset_name = models.CharField(max_length=100)

    asset_type = models.CharField(
        max_length=50,
        choices=ASSET_TYPES
    )

    serial_number = models.CharField(
        max_length=100,
        unique=True
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hardware_assets'
    )

    purchase_date = models.DateField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.asset_name} - {self.serial_number}"


class SoftwareLicense(models.Model):

    software_name = models.CharField(max_length=100)

    license_key = models.CharField(
        max_length=200,
        unique=True
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='software_licenses'
    )

    expiry_date = models.DateField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.software_name