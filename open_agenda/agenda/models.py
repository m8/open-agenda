from django.db import models

# Create your models here.
class Notes(models.Model):
    notes = models.CharField(max_length=5000)
    pub_date = models.CharField(max_length=50)

    # def __init__(self, notes,pub_date):
    #     self.notes = notes,
    #     self.pub_date = pub_date

class Project(models.Model):
    notes = models.CharField(max_length=50000)
    icon = models.CharField(max_length=50)
    name =  models.CharField(max_length=30)