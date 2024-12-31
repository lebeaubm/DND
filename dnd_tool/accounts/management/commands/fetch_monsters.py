import json
from django.core.management.base import BaseCommand
from accounts.models import BasicMonster


class Command(BaseCommand):
    help = 'Import basic monsters from a JSON file'

    def handle(self, *args, **kwargs):
        file_path = 'path_to_your_json_file.json'  # Update with your JSON file path

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for monster_data in data:
            # Check if the monster already exists
            monster, created = BasicMonster.objects.get_or_create(
                name=monster_data.get('name')
            )

            # Update monster fields
            monster.size = monster_data.get('meta', '').split(' ')[0]
            monster.type = monster_data.get('meta', '').split(' ')[1] if len(monster_data.get('meta', '').split(' ')) > 1 else ''
            monster.armor_class = int(monster_data.get('Armor Class', '0').split(' ')[0]) if monster_data.get('Armor Class') else 0
            monster.hit_points = int(monster_data.get('Hit Points', '0').split(' ')[0]) if monster_data.get('Hit Points') else 0
            monster.speed = monster_data.get('Speed', '')

            # Ability scores
            monster.strength = int(monster_data.get('STR', 0))
            monster.dexterity = int(monster_data.get('DEX', 0))
            monster.constitution = int(monster_data.get('CON', 0))
            monster.intelligence = int(monster_data.get('INT', 0))
            monster.wisdom = int(monster_data.get('WIS', 0))
            monster.charisma = int(monster_data.get('CHA', 0))

            # Additional stats
            monster.saving_throws = monster_data.get('Saving Throws', '')
            monster.skills = monster_data.get('Skills', '')
            monster.damage_resistances = monster_data.get('Damage Resistances', '')
            monster.damage_immunities = monster_data.get('Damage Immunities', '')
            monster.condition_immunities = monster_data.get('Condition Immunities', '')
            monster.senses = monster_data.get('Senses', '')
            monster.languages = monster_data.get('Languages', '')
            monster.challenge_rating = monster_data.get('Challenge', '')

            # Abilities, Actions, Legendary Actions, and Reactions
            monster.traits = monster_data.get('Traits', '').replace('<p>', '').replace('</p>', '\n').replace('<em>', '').replace('</em>', '').replace('<strong>', '**').replace('</strong>', '**')
            monster.actions = monster_data.get('Actions', '').replace('<p>', '').replace('</p>', '\n').replace('<em>', '').replace('</em>', '').replace('<strong>', '**').replace('</strong>', '**')
            monster.legendary_actions = monster_data.get('Legendary Actions', '').replace('<p>', '').replace('</p>', '\n').replace('<em>', '').replace('</em>', '').replace('<strong>', '**').replace('</strong>', '**')
            monster.reactions = monster_data.get('Reactions', '').replace('<p>', '').replace('</p>', '\n').replace('<em>', '').replace('</em>', '').replace('<strong>', '**').replace('</strong>', '**')

            # Image URL
            monster.image_url = monster_data.get('img_url', '')

            # Save monster
            monster.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added monster: {monster.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Updated existing monster: {monster.name}'))
