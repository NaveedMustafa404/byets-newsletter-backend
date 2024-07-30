from django.db import models
import system_manager.helper

# Create your models here.


class Content(models.Model):
    title = models.CharField(max_length=500, null=True)
    slug = models.SlugField(max_length=255, null=True, unique=True)
    image = models.ImageField(upload_to=system_manager.helper.generate_filename, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null = True)



class SettingsEmail(models.Model):
    email = models.CharField(max_length=500, null=True)
    image = models.ImageField(upload_to=system_manager.helper.generate_filename, null=True)
    fb_link = models.CharField(max_length=500, null=True)
    twitter_link = models.CharField(max_length=500, null=True)
    instagram_link = models.CharField(max_length=500, null=True)
    linkedin_link = models.CharField(max_length=500, null=True)
    phone = models.CharField(max_length=500, null=True)
    website = models.CharField(max_length=500, null=True)
    country_office = models.CharField(max_length=500, null=True)
    project_office = models.CharField(max_length=500, null=True)
    
    

class Layout(models.Model):
    subject = models.TextField( null=True)
    inner_html = models.TextField( null=True)
    value = models.JSONField(null=True)
    published = models.BooleanField(blank=True, default=False)
    published_at = models.DateTimeField(null= True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True, null = True)

class LayoutDraft(models.Model):
    subject = models.TextField( null=True)
    inner_html = models.TextField( null=True)
    value = models.JSONField(null=True)



class Blogs(models.Model):
    title = models.CharField(max_length=500,default= "No Title", null = True, blank=True)
    file = models.FileField(upload_to=system_manager.helper.generate_filename,default="https://placehold.co/600x400?text=File\nBroken",
                            null = True)
    created_at = models.DateTimeField(auto_now_add=True, null = True)