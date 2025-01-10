import os
import django
import requests
import json

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnd_tool.settings")
django.setup()

from accounts.models import BasicMonster  # Import after setting up Django

def test_monster_selection():
    # AI Prompt
    url = "http://localhost:8000/api/completions"  # Adjust if needed
    headers = {"Authorization": "Bearer your_api_key"}  # Add your API key if required
    
    prompt = "Select two basic monsters for combat. List their names."
    
    response = requests.post(
        url,
        headers=headers,
        json={
            "model": "mistral",
            "prompt": prompt,
            "max_tokens": 100,
            "temperature": 0.7
        },
        stream=True
    )
    
    # Collect AI response
    monster_names = []
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            content = data.get("message", {}).get("content", "")
            if content:
                monster_names.append(content.strip())
    
    # Simulate combat with two monsters
    if len(monster_names) < 2:
        print("AI did not return enough monsters.")
        return
    
    # Fetch from database
    selected_monsters = BasicMonster.objects.filter(name__in=monster_names[:2])
    if not selected_monsters.exists():
        print("No monsters found in the database with the given names.")
        return
    
    # Prepare for combat
    combatants = []
    for monster in selected_monsters:
        combatants.append({
            "name": monster.name,
            "hit_points": monster.hit_points,
            "armor_class": monster.armor_class,
            "strength": monster.strength,
            "dexterity": monster.dexterity,
            "constitution": monster.constitution,
            "intelligence": monster.intelligence,
            "wisdom": monster.wisdom,
            "charisma": monster.charisma,
            "actions": monster.actions,
            "traits": monster.traits,
        })
    
    # Print combatants' stats
    print("Combatants:")
    for combatant in combatants:
        print(json.dumps(combatant, indent=4))

if __name__ == "__main__":
    test_monster_selection()
