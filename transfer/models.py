from django.db import models

# Create your models here.
from django.db.models.fields import TextField


class Token(models.Model):
    token = TextField()
