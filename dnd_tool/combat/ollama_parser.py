import ollama
import json

# Query Ollama
def query_mistral(prompt):
    response = ollama.chat(model='mistral', messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']

# Parse Combat Details from Stat Block
def parse_monster_sheet(sheet_text):
    """
    Extract key combat details from a D&D monster/character sheet.
    """
    prompt = f"""
Extract key combat details from the following D&D monster/character sheet:

{sheet_text}

Provide the information in the following JSON structure:
{{
    "Name": "Monster/Character Name",
    "AC": "Armor Class",
    "HP": "Hit Points",
    "Speed": "Speed",
    "Attacks": [
        {{
            "Name": "Attack Name",
            "ToHit": "+X",
            "Damage": "2d6+5",
            "Type": "Damage Type"
        }}
    ],
    "Multiattack": "The creature makes three attacks: one with its bite and two with its claws.",
    "SpecialAttacks": [
        {{
            "Name": "Special Attack Name",
            "Description": "Description of the special attack, including recharge mechanics if any"
        }}
    ],
    "LegendaryActions": ["Action1", "Action2"]
}}
"""
    try:
        response = query_mistral(prompt)
        return json.loads(response)
    except json.JSONDecodeError:
        print("Failed to parse JSON from Ollama response.")
        return None








