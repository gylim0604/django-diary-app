from django.db import models

# Create your models here.
class Entry(models.Model):
    # Fields
    entry_date = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('entry', args=[str(self.ids)])