import os
import django
import random
import requests
import json
import sys

# # Set up Django environment
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnd_tool.settings")
# django.setup()

# from accounts.models import BasicMonster


##Needed

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnd_tool.settings")  # Replace "dnd_tool" with your project name

# Setup Django
django.setup()

from accounts.models import BasicMonster  # Import after setting up Django


# Accurate Average Damage Formula
def accurate_average_damage(avg_damage, chance_to_hit, chance_to_crit, avg_crit_damage):
    return (avg_damage * (chance_to_hit - chance_to_crit)) + (avg_crit_damage * chance_to_crit)

# Fetch BasicMonster Data
def fetch_monsters(names):
    return [BasicMonster.objects.get(name=name) for name in names]

# Use Mistral to Parse Monster Data
def parse_with_mistral(monsters):
    monster_data = [{"name": m.name, "armor_class": m.armor_class, "hit_points": m.hit_points, 
                     "strength": m.strength, "dexterity": m.dexterity, 
                     "constitution": m.constitution, "actions": m.actions} for m in monsters]

    mistral_input = f"Parse the following monster data: {json.dumps(monster_data)}"
    response = requests.post(
        "http://localhost:11434/api/completions",
        json={"model": "mistral", "messages": [{"role": "user", "content": mistral_input}]}
    )
    parsed_data = response.json().get("message", {}).get("content", "")
    return json.loads(parsed_data)

# Simulate Combat
def simulate_combat(monsters):
    turn_order = sorted(monsters, key=lambda m: random.randint(1, 20) + m["dexterity"], reverse=True)
    combat_log = []
    combat_log.append(f"Turn Order: {', '.join([m['name'] for m in turn_order])}")

    while len([m for m in monsters if m["hit_points"] > 0]) > 1:
        for monster in turn_order:
            if monster["hit_points"] <= 0:
                continue  # Skip defeated monsters

            # Pick a target
            target = random.choice([m for m in monsters if m["hit_points"] > 0 and m != monster])

            # Simulate Attack
            avg_damage = random.randint(5, 15)  # Replace with real damage calculation
            chance_to_hit = 0.7  # Replace with actual calculation
            chance_to_crit = 0.1  # Replace with actual calculation
            avg_crit_damage = avg_damage * 2  # Replace with real crit calculation

            damage = accurate_average_damage(avg_damage, chance_to_hit, chance_to_crit, avg_crit_damage)
            target["hit_points"] -= damage

            combat_log.append(f"{monster['name']} attacks {target['name']} for {damage:.2f} damage!")

            if target["hit_points"] <= 0:
                combat_log.append(f"{target['name']} has been defeated!")

            if len([m for m in monsters if m["hit_points"] > 0]) == 1:
                break

    winner = [m for m in monsters if m["hit_points"] > 0][0]
    combat_log.append(f"{winner['name']} wins the combat!")
    return combat_log

# # Test the Engine
# def test_engine():
#     # Pick two monster names (replace with actual names in your DB)
#     selected_names = ["Goblin", "Orc"]

#     # Fetch monster data
#     monsters = fetch_monsters(selected_names)
#     print("Fetched Monsters:", monsters)

#     # Parse data with Mistral
#     parsed_data = parse_with_mistral(monsters)
#     print("Parsed Data:", parsed_data)

#     # Simulate combat
#     combat_log = simulate_combat(parsed_data)
#     print("\nCombat Log:")
#     for entry in combat_log:
#         print(entry)

# if __name__ == "__main__":
#     test_engine()



def test_engine():
    # Mock data for testing
    selected_names = ["Goblin", "Orc"]  # Replace with actual names in your DB

    # Fetch monster data
    try:
        monsters = fetch_monsters(selected_names)
        print("Fetched Monsters:")
        for m in monsters:
            print(f"Name: {m.name}, HP: {m.hit_points}, AC: {m.armor_class}")
    except Exception as e:
        print("Error fetching monsters:", e)
        return

    # Parse data with mock Mistral response
    mock_parsed_data = [
        {"name": "Goblin", "hit_points": 15, "armor_class": 12, "dexterity": 14, "actions": "Attack"},
        {"name": "Orc", "hit_points": 30, "armor_class": 13, "dexterity": 10, "actions": "Smash"},
    ]
    print("\nMock Parsed Data:", mock_parsed_data)

    # Simulate combat
    combat_log = simulate_combat(mock_parsed_data)
    print("\nCombat Log:")
    for entry in combat_log:
        print(entry)

if __name__ == "__main__":
    test_engine()
