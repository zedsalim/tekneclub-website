from django.db import models

class University(models.Model):
  name = models.CharField(max_length=200, unique=True)

  class Meta:
    verbose_name = "University"
    verbose_name_plural = "Universities"

  def __str__(self):
    return self.name

class Department(models.Model):
  name = models.CharField(max_length=200, unique=True)
  # university = models.ForeignKey(University, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

class StudyYear(models.Model):
  name = models.CharField(max_length=200, unique=True)
  # department = models.ForeignKey(Department, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

class Interests(models.Model):
  name = models.CharField(max_length=200, unique=True)

  class Meta:
    verbose_name = "Interests"
    verbose_name_plural = "Interests"

  def __str__(self):
    return self.name