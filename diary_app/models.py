from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

#Model for a single entry
class Entry(models.Model):
    # Fields
    entry_date = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, default=None,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('entry-detail', args=[str(self.id)])


