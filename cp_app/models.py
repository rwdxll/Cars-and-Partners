from django.db import models
from django.contrib.postgres.fields import ArrayField
from unixtimestampfield.fields import UnixTimeStampField

# Create your models here.
class Partner(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    name = models.CharField(max_length=160)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    company_name = models.CharField(max_length=160)
    cars = ArrayField(
        models.IntegerField(), blank=True
        )
    created_at = UnixTimeStampField(auto_now_add=True, use_numeric=True)
    modified_at = UnixTimeStampField(auto_now=True, use_numeric=True)
    deleted_at = UnixTimeStampField(default=0, use_numeric=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.id = Partner.objects.latest('id').id +1
        super().save(*args, **kwargs)