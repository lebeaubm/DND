from django.db import models
from django.contrib.auth.models import User
import json


class Monster(models.Model):
    name = models.CharField(max_length=100)  # Required field
    size = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    alignment = models.CharField(max_length=50, null=True, blank=True)
    
    armor_class = models.IntegerField(null=True, blank=True)
    hit_points = models.IntegerField(null=True, blank=True)
    speed = models.CharField(max_length=100, null=True, blank=True)
    
    strength = models.IntegerField(null=True, blank=True)
    dexterity = models.IntegerField(null=True, blank=True)
    constitution = models.IntegerField(null=True, blank=True)
    intelligence = models.IntegerField(null=True, blank=True)
    wisdom = models.IntegerField(null=True, blank=True)
    charisma = models.IntegerField(null=True, blank=True)
    
    saving_throws = models.TextField(null=True, blank=True)
    damage_resistances = models.TextField(null=True, blank=True)
    damage_immunities = models.TextField(null=True, blank=True)
    condition_immunities = models.TextField(null=True, blank=True)
    
    senses = models.TextField(null=True, blank=True)
    languages = models.TextField(null=True, blank=True)
    challenge_rating = models.CharField(max_length=20, null=True, blank=True)
    abilities = models.TextField(null=True, blank=True)
    
    actions = models.TextField(null=True, blank=True)
    reactions = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name



class BasicMonster(models.Model):
    # General Information
    name = models.CharField(max_length=100, unique=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    alignment = models.CharField(max_length=50, null=True, blank=True)

    # Combat Stats
    armor_class = models.IntegerField(default=0)
    hit_points = models.IntegerField(default=0)
    speed = models.CharField(max_length=100, null=True, blank=True)

    # Ability Scores
    strength = models.IntegerField(default=0)
    strength_mod = models.CharField(max_length=5, null=True, blank=True)
    dexterity = models.IntegerField(default=0)
    dexterity_mod = models.CharField(max_length=5, null=True, blank=True)
    constitution = models.IntegerField(default=0)
    constitution_mod = models.CharField(max_length=5, null=True, blank=True)
    intelligence = models.IntegerField(default=0)
    intelligence_mod = models.CharField(max_length=5, null=True, blank=True)
    wisdom = models.IntegerField(default=0)
    wisdom_mod = models.CharField(max_length=5, null=True, blank=True)
    charisma = models.IntegerField(default=0)
    charisma_mod = models.CharField(max_length=5, null=True, blank=True)

    # Additional Stats
    saving_throws = models.CharField(max_length=255, null=True, blank=True)
    skills = models.CharField(max_length=255, null=True, blank=True)
    damage_resistances = models.CharField(max_length=255, null=True, blank=True)
    damage_immunities = models.CharField(max_length=255, null=True, blank=True)
    condition_immunities = models.CharField(max_length=255, null=True, blank=True)
    senses = models.CharField(max_length=255, null=True, blank=True)
    languages = models.CharField(max_length=255, null=True, blank=True)
    challenge_rating = models.CharField(max_length=20, null=True, blank=True)

    # Descriptive Fields
    traits = models.TextField(null=True, blank=True)
    actions = models.TextField(null=True, blank=True)
    reactions = models.TextField(null=True, blank=True)
    legendary_actions = models.TextField(null=True, blank=True)

    # Image URL
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name











class CharacterSheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Basic Info
    name = models.CharField(max_length=100)  # Required
    class_name = models.CharField(max_length=100, blank=True, null=True)
    level = models.PositiveIntegerField(default=1, blank=True, null=True)
    race = models.CharField(max_length=100, blank=True, null=True)
    alignment = models.CharField(max_length=50, blank=True, null=True)
    
    # Combat Stats
    hit_points = models.PositiveIntegerField(default=10, blank=True, null=True)
    armor_class = models.PositiveIntegerField(default=10, blank=True, null=True)
    initiative = models.IntegerField(default=0, blank=True, null=True)
    speed = models.PositiveIntegerField(default=30, blank=True, null=True)
    
    # Abilities
    strength = models.PositiveIntegerField(default=10, blank=True, null=True)
    dexterity = models.PositiveIntegerField(default=10, blank=True, null=True)
    constitution = models.PositiveIntegerField(default=10, blank=True, null=True)
    intelligence = models.PositiveIntegerField(default=10, blank=True, null=True)
    wisdom = models.PositiveIntegerField(default=10, blank=True, null=True)
    charisma = models.PositiveIntegerField(default=10, blank=True, null=True)
    
    # Saving Throws
    saving_throw_strength = models.BooleanField(default=False)
    saving_throw_dexterity = models.BooleanField(default=False)
    saving_throw_constitution = models.BooleanField(default=False)
    saving_throw_intelligence = models.BooleanField(default=False)
    saving_throw_wisdom = models.BooleanField(default=False)
    saving_throw_charisma = models.BooleanField(default=False)
    
    # Spellcasting
    spell_slots = models.JSONField(default=dict, blank=True, null=True)
    spells_known = models.TextField(blank=True, null=True)
    
    # Attacks
    primary_attack_name = models.CharField(max_length=100, blank=True, null=True)
    primary_attack_type = models.CharField(max_length=20, choices=[('Melee', 'Melee'), ('Ranged', 'Ranged')], blank=True, null=True)
    primary_attack_bonus = models.IntegerField(default=0, blank=True, null=True)
    primary_attack_damage = models.CharField(max_length=20, blank=True, null=True)
    primary_attack_damage_type = models.CharField(max_length=20, blank=True, null=True)
    
    secondary_attack_name = models.CharField(max_length=100, blank=True, null=True)
    secondary_attack_type = models.CharField(max_length=20, blank=True, null=True)
    secondary_attack_bonus = models.IntegerField(default=0, blank=True, null=True)
    secondary_attack_damage = models.CharField(max_length=20, blank=True, null=True)
    secondary_attack_damage_type = models.CharField(max_length=20, blank=True, null=True)
    
    # Special Abilities & Reactions
    special_abilities = models.TextField(blank=True, null=True)
    reactions = models.TextField(blank=True, null=True)
    
    # Combat Preferences
    combat_role = models.CharField(max_length=50, blank=True, null=True)
    preferred_range = models.CharField(max_length=20, blank=True, null=True)
    attack_priority = models.CharField(max_length=50, blank=True, null=True)
    escape_threshold = models.PositiveIntegerField(default=20, blank=True, null=True)
    
    # Conditions & Status Effects
    conditions = models.TextField(blank=True, null=True)
    temporary_hit_points = models.PositiveIntegerField(default=0, blank=True, null=True)
    ongoing_damage = models.CharField(max_length=50, blank=True, null=True)
    
    # Actions
    available_actions = models.JSONField(default=dict, blank=True, null=True)
    bonus_actions = models.JSONField(default=dict, blank=True, null=True)
    
    # Finished Status (Hidden, Automatic)
    finished = models.BooleanField(default=False, editable=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} (Level {self.level or 'N/A'})"
    
    def check_if_finished(self):
        """Check if required fields are filled for the sheet to be considered finished."""
        required_fields = [
            self.name,
            self.hit_points, self.armor_class, self.initiative, self.speed,
            self.strength, self.dexterity, self.constitution,
            self.intelligence, self.wisdom, self.charisma,
            self.primary_attack_name, self.primary_attack_type,
            self.primary_attack_damage, self.primary_attack_damage_type
        ]
        return all(field not in [None, '', 0] for field in required_fields)
    
    def save(self, *args, **kwargs):
        """Override save to automatically set 'finished' status."""
        self.finished = self.check_if_finished()
        super(CharacterSheet, self).save(*args, **kwargs)


    




















