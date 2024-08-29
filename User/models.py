from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    MY_ROLES =[
        ('Admin','Admin'),
        ('Staff','Staff'),
    ]
    role = models.CharField(max_length=50, choices=MY_ROLES)
    organization = models. CharField(max_length=50)

    def save(self, *args, **kwargs):
        from Core.models import companyprofileTable
        super(User, self).save(*args, **kwargs)
        if self.organization:

            companyprofileTable.objects.get_or_create(
                company_name=self.organization,
                defaults={'company_email': self.email}
            )