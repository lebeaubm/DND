import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnd_tool.settings")
django.setup()

from accounts.models import BasicMonster  # Import after setting up Django

def fetch_first_basic_monster():
    try:
        # Fetch all monsters
        monsters = BasicMonster.objects.all()

        if not monsters.exists():
            print("No BasicMonster entries found in the database.")
            return

        # Get the first monster
        first_monster = monsters.first()

        # Print the first monster details
        print(f"Name: {first_monster.name}")
        print(f"Hit Points: {first_monster.hit_points}")
        print(f"Armor Class: {first_monster.armor_class}")
        print(f"Speed: {first_monster.speed}")
        print(f"Strength: {first_monster.strength}")
        print(f"Dexterity: {first_monster.dexterity}")
        print(f"Constitution: {first_monster.constitution}")
        print(f"Intelligence: {first_monster.intelligence}")
        print(f"Wisdom: {first_monster.wisdom}")
        print(f"Charisma: {first_monster.charisma}")
        print(f"Actions: {first_monster.actions}")
        print(f"Traits: {first_monster.traits}")
        print(f"Legendary Actions: {first_monster.legendary_actions}")
        print(f"Image URL: {first_monster.image_url}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_first_basic_monster()
