from django.db import models
from django.contrib.auth.models import User

class CharacterSheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)
    level = models.PositiveIntegerField()
    hit_points = models.PositiveIntegerField()
    strength = models.PositiveIntegerField()
    dexterity = models.PositiveIntegerField()
    constitution = models.PositiveIntegerField()
    intelligence = models.PositiveIntegerField()
    wisdom = models.PositiveIntegerField()
    charisma = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Level {self.level})"

