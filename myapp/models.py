from django.db import models
from django.conf import settings  # Import settings to use AUTH_USER_MODEL
from django.contrib.auth.models import AbstractUser

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    published_date = models.DateTimeField(auto_now_add=True)  # Automatically set on creation, if appropriate

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author}"

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class ResearchItem(models.Model):
    title = models.CharField(max_length=255)  # Required
    century = models.IntegerField(null=True, blank=True)  # Optional
    description = models.TextField(blank=True)  # Optional
    other = models.TextField(blank=True)  # Optional
    CE_or_BCE = models.CharField(max_length=3, choices=(('CE', 'CE'), ('BCE', 'BCE')), blank=True)  # Optional
    author = models.CharField(max_length=255, blank=True)  # Optional
    published_date = models.DateField(null=True, blank=True)  # Optional
    source = models.CharField(max_length=255, blank=True)  # Optional
    country = models.ManyToManyField(Country, blank=True)  # Changed to ManyToManyField to allow multiple selections
    image = models.ImageField(upload_to='research_images/', null=True, blank=True)  # Optional
    file = models.FileField(upload_to='research_files/', null=True, blank=True)  # Optional
    subject = models.CharField(max_length=255, blank=True)  # Optional
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Required
    date = models.CharField(max_length=100, blank=True)  # Consider a more specific implementation based on your needs

    def __str__(self):
        return self.title
 
        


class Researcher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    address = models.TextField()
    # Assuming your User model already includes an email field
    position_title = models.CharField(max_length=100)
    affiliation_institution = models.CharField(max_length=100)
    research_interests = models.TextField()
    countries_of_research_focus = models.ManyToManyField(Country)
    degree_sought = models.CharField(max_length=100, blank=True, null=True)
    expected_degree_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
