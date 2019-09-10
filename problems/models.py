from django.db import models

import string


class Topic(models.Model):
    """Schema and methods for the topics provided to the user
    """
    name = models.CharField(max_length=64, primary_key=True)

    class Meta:
        ordering = ('name',)

    def __str(self):
        return self.name

class Skill(models.Model):
    """Schema and methods for the skills under a topic 
    """
    name = models.CharField(max_length=64)
    topics = models.ManyToManyField(Topic)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name

class Concept(models.Model):
    """Schema and methods for the concepts under a skill
    """
    name = models.CharField(max_length=256)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.name
    
class Questions(models.Model):
    """Schema for the questions available
    """
    title = models.TextField()
    description = models.TextField()

    LEVELS = (
        ('B', 'Beginner'),
        ('I', 'Intermediate'),
        ('A', 'Advanced'),
    )
    level = models.CharField(max_length=1, choices=LEVELS)
    concepts = models.ManyToManyField(Concept)
    
    def __str__(self):
        return self.title
