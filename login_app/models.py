from django.db import models

# Create your models here.

class Credentials(models.Model):
    uname = models.CharField(max_length = 100, null = True)
