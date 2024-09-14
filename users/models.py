import os
import uuid
from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from external_data.models import *

class NewUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username

class Role(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    description = models.TextField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name.title() 


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    profile_pic = models.ImageField(upload_to='profile_pics', default='default.jpg', blank=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    study_year = models.ForeignKey(StudyYear, on_delete=models.SET_NULL, null=True)
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    interests = models.ManyToManyField(Interests)
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.ManyToManyField(Role, blank=True)
    is_blog_poster = models.BooleanField(default=False)
    is_event_poster = models.BooleanField(default=False)
    is_responder = models.BooleanField(default=False)
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    def generate_unique_filename(self, filename):
        image_ext = filename.split('.')[-1]
        new_filename = f"{uuid.uuid4()}.{image_ext}"
        return os.path.join('profile_pics', new_filename)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)

        super(UserProfile, self).save(*args, **kwargs)

        if self.profile_pic and self.profile_pic != 'default.jpg':
            img = Image.open(self.profile_pic.path)
            if img.height > 100 or img.width > 100:
                output_size = (150, 150)
                img.thumbnail(output_size)
                img.save(self.profile_pic.path)

            new_filename = self.generate_unique_filename(self.profile_pic.name)
            new_path = os.path.join(os.path.dirname(self.profile_pic.path), os.path.basename(new_filename))
            os.rename(self.profile_pic.path, new_path)
            self.profile_pic.name = new_filename

            super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        full_name = f'{self.user.first_name} {self.user.last_name}'
        return full_name.title()
