from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class shortend_url(models.Model):

    users_id = models.ForeignKey(User, on_delete=models.CASCADE)
    orginal_url = models.CharField(max_length=200, null=False)
    shorted_url = models.CharField(max_length=50, null=True)
    no_of_visitor = models.IntegerField(null=True)
