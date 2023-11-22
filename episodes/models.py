from django.db import models

# Create your models here.

class Episode(models.Model):
    """A class that defines a model"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    podcast_name = models.CharField(max_length=200)
    guid = models.CharField(max_length=50)

    def __str__(self):
        """Returns a string representation of podcast name and title"""
        return (f"{self.podcast_name}: {self.title}")

