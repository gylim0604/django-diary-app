from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.

#Model for a single entry
class Entry(models.Model):
    # Fields
    entry_date = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('entry-detail', args=[str(self.id)])


