from django.db import models

# Create your models here.
class Notes(models.Model):
    notes = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.notes
