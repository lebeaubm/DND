import json
import re
from bs4 import BeautifulSoup  
from django.core.management.base import BaseCommand
from accounts.models import BasicMonster


# class Command(BaseCommand):
#     help = 'Import basic monsters from a JSON file'

#     def handle(self, *args, **kwargs):
#         file_path = 'monsters.json'  

#         try:
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 data = json.load(file)
#         except FileNotFoundError:
#             self.stderr.write(self.style.ERROR('File not found. Please ensure monsters.json exists.'))
#             return

#         for monster_data in data:
#             name = monster_data.get('name')
#             if not name:
#                 continue  

#             monster, created = BasicMonster.objects.get_or_create(
#                 name=name
#             )

#             # Map fields
#             monster.size = monster_data.get('meta', '').split(' ')[0]
#             monster.type = monster_data.get('meta', '').split(' ')[1] if len(monster_data.get('meta', '').split(' ')) > 1 else ''
#             monster.alignment = monster_data.get('meta', '').split(',')[-1].strip() if ',' in monster_data.get('meta', '') else ''

#             monster.armor_class = int(monster_data.get('Armor Class', '0').split(' ')[0]) if monster_data.get('Armor Class') else 0
#             monster.hit_points = int(monster_data.get('Hit Points', '0').split(' ')[0]) if monster_data.get('Hit Points') else 0
#             monster.speed = monster_data.get('Speed', '')

#             monster.strength = int(monster_data.get('STR', 0))
#             monster.dexterity = int(monster_data.get('DEX', 0))
#             monster.constitution = int(monster_data.get('CON', 0))
#             monster.intelligence = int(monster_data.get('INT', 0))
#             monster.wisdom = int(monster_data.get('WIS', 0))
#             monster.charisma = int(monster_data.get('CHA', 0))

#             monster.saving_throws = monster_data.get('Saving Throws', '')
#             monster.skills = monster_data.get('Skills', '')
#             monster.damage_resistances = monster_data.get('Damage Resistances', '')
#             monster.damage_immunities = monster_data.get('Damage Immunities', '')
#             monster.condition_immunities = monster_data.get('Condition Immunities', '')
#             monster.senses = monster_data.get('Senses', '')
#             monster.languages = monster_data.get('Languages', '')
#             monster.challenge_rating = monster_data.get('Challenge', '')

            
#             monster.traits = monster_data.get('Traits', '').replace('<p>', '\n').replace('</p>', '').replace('<em>', '').replace('</em>', '').replace('<strong>', '**').replace('</strong>', '**')
#             monster.actions = monster_data.get('Actions', '').replace('<p>', '\n').replace('</p>', '').replace('<em>', '').replace('</em>', '').replace('<strong>', '**').replace('</strong>', '**')
#             monster.legendary_actions = monster_data.get('Legendary Actions', '').replace('<p>', '\n').replace('</p>', '').replace('<em>', '').replace('</em>', '').replace('<strong>', '**').replace('</strong>', '**')
#             monster.reactions = monster_data.get('Reactions', '').replace('<p>', '\n').replace('</p>', '').replace('<em>', '').replace('</em>', '').replace('<strong>', '**').replace('</strong>', '**')

#             monster.image_url = monster_data.get('img_url', '')

#             monster.save()

#             if created:
#                 self.stdout.write(self.style.SUCCESS(f'Added monster: {name}'))
#             else:
#                 self.stdout.write(self.style.WARNING(f'Updated monster: {name}'))



class Command(BaseCommand):
    help = 'Import basic monsters from a JSON file'

    def handle(self, *args, **kwargs):
        file_path = 'monsters.json'  # Ensure this matches your file name

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR('File not found. Please ensure monster.json exists in the root directory.'))
            return
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR('Invalid JSON format. Please check the file contents.'))
            return

        for monster_data in data:
            name = monster_data.get('name')
            if not name:
                continue  # Skip entries without a name

            # Check if the monster already exists, update if it does
            monster, created = BasicMonster.objects.get_or_create(
                name=name
            )

            # Safely map all the fields from the JSON data
            monster.size = monster_data.get('meta', '').split(' ')[0]
            monster.type = (
                monster_data.get('meta', '').split(' ')[1]
                if len(monster_data.get('meta', '').split(' ')) > 1
                else ''
            )
            monster.alignment = (
                monster_data.get('meta', '').split(',')[-1].strip()
                if ',' in monster_data.get('meta', '')
                else ''
            )

            monster.armor_class = int(monster_data.get('Armor Class', '0').split(' ')[0]) if monster_data.get('Armor Class') else 0
            monster.hit_points = int(monster_data.get('Hit Points', '0').split(' ')[0]) if monster_data.get('Hit Points') else 0
            monster.speed = monster_data.get('Speed', '')

            monster.strength = int(monster_data.get('STR', 0))
            monster.dexterity = int(monster_data.get('DEX', 0))
            monster.constitution = int(monster_data.get('CON', 0))
            monster.intelligence = int(monster_data.get('INT', 0))
            monster.wisdom = int(monster_data.get('WIS', 0))
            monster.charisma = int(monster_data.get('CHA', 0))

            monster.saving_throws = monster_data.get('Saving Throws', '')
            monster.skills = monster_data.get('Skills', '')
            monster.damage_resistances = monster_data.get('Damage Resistances', '')
            monster.damage_immunities = monster_data.get('Damage Immunities', '')
            monster.condition_immunities = monster_data.get('Condition Immunities', '')
            monster.senses = monster_data.get('Senses', '')
            monster.languages = monster_data.get('Languages', '')
            monster.challenge_rating = monster_data.get('Challenge', '')

            # Clean up traits, actions, legendary actions, and reactions
            def clean_html_tags(text):
                if text:
                    return (
                        text.replace('<p>', '\n')
                        .replace('</p>', '')
                        .replace('<em>', '')
                        .replace('</em>', '')
                        .replace('<strong>', '**')
                        .replace('</strong>', '**')
                        .strip()
                    )
                return ''

            monster.traits = clean_html_tags(monster_data.get('Traits', ''))
            monster.actions = clean_html_tags(monster_data.get('Actions', ''))
            monster.legendary_actions = clean_html_tags(monster_data.get('Legendary Actions', ''))
            monster.reactions = clean_html_tags(monster_data.get('Reactions', ''))

            monster.image_url = monster_data.get('img_url', '')

            # Save the monster instance
            monster.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f'Added monster: {name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Updated monster: {name}'))

