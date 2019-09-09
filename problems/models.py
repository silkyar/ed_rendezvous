from django.db import models

import string


class Topic(models.Model):
    """Schema and methods for the topics provided to the user
    """
    topic = models.CharField(max_field=64)

    class Meta:
        ordering = ('topic',)
    
    def __str(self):
        return self.topic

class Skill(models.Model):
    """Schema and methods for the skills under a topic 
    """
    skill = models.CharField(max_field=64)
    topic = models.ManyToManyField(Topic)
     
    class Meta:
        ordering = ('skill',)
    
    def __str__(self):
        return self.skill

class Concept(models.Model):
    """Schema and methods for the concepts under a topic
    """
    concept = models.charField(max_field=256)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
   
    def __str__():
        return self.concept 
    
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
    level = models.CharField(max_field=1, choices=LEVELS)
    
    concept = models.ForiegnKey(Concept, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill)
    
    def __str__(self):
        return title
