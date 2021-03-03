from django.db import models

# Create your models here.
class Notes(models.Model):
    notes = models.CharField(max_length=5000)
    pub_date = models.CharField(max_length=50)

    def __str__(self):
        return self.notes