from django.db import models
from django.contrib.auth.models import User

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

