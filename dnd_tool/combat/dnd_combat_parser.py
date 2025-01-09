# import ollama
# import re
# import json

# # Initialize the Ollama Mistral model
# def query_mistral(prompt):
#     response = ollama.chat(model='mistral', messages=[
#         {'role': 'user', 'content': prompt}
#     ])
#     return response['message']['content']

# # Parse combat-relevant information
# def parse_monster_sheet(sheet_text):
#     prompt = f"""
#     Extract key combat details from the following D&D monster/character sheet:

#     {sheet_text}

#     Provide the information in the following JSON structure:
#     {{
#         "Name": "Monster/Character Name",
#         "AC": "Armor Class",
#         "HP": "Hit Points",
#         "Speed": "Speed",
#         "Attacks": [
#             {{
#                 "Name": "Attack Name",
#                 "ToHit": "Attack Bonus",
#                 "Damage": "Damage Dice",
#                 "Type": "Damage Type"
#             }}
#         ],
#         "Multiattack": "Describe Multiattack",
#         "SpecialAttacks": [
#             {{
#                 "Name": "Special Attack Name",
#                 "Description": "Description of the special attack, including recharge mechanics if any"
#             }}
#         ],
#         "LegendaryActions": ["Action1", "Action2"]
#     }}
#     """
    
#     response = query_mistral(prompt)
#     return json.loads(response)

# # Example usage
# if __name__ == '__main__':
#     monster_sheet = '''
#     "name": "Aboleth",
#     "meta": "Large aberration, lawful evil",
#     "Armor Class": "17 (Natural Armor)",
#     "Hit Points": "135 (18d10 + 36)",
#     "Speed": "10 ft., swim 40 ft. ",
#     "STR": "21",
#     "STR_mod": "(+5)",
#     "DEX": "9",
#     "DEX_mod": "(-1)",
#     "CON": "15",
#     "CON_mod": "(+2)",
#     "INT": "18",
#     "INT_mod": "(+4)",
#     "WIS": "15",
#     "WIS_mod": "(+2)",
#     "CHA": "18",
#     "CHA_mod": "(+4)",
#     "Saving Throws": "CON +6, INT +8, WIS +6",
#     "Skills": "History +12, Perception +10",
#     "Senses": "Darkvision 120 ft.,  Passive Perception 20",
#     "Languages": "Deep Speech, Telepathy 120 ft.",
#     "Challenge": "10 (5,900 XP)",
#     "Traits": "<p><em><strong>Amphibious.</strong></em> The aboleth can breathe air and water. </p><p><em><strong>Mucous Cloud.</strong></em> While underwater, the aboleth is surrounded by transformative mucus. A creature that touches the aboleth or that hits it with a melee attack while within 5 feet of it must make a DC 14 Constitution saving throw. On a failure, the creature is diseased for 1d4 hours. The diseased creature can breathe only underwater. </p><p><em><strong>Probing Telepathy.</strong></em> If a creature communicates telepathically with the aboleth, the aboleth learns the creature's greatest desires if the aboleth can see the creature.</p>",
#     "Actions": "<p><em><strong>Multiattack.</strong></em> The aboleth makes three tentacle attacks. </p><p><em><strong>Tentacle.</strong></em> <em>Melee Weapon Attack:</em> +9 to hit, reach 10 ft., one target. <em>Hit:</em> 12 (2d6 + 5) bludgeoning damage. If the target is a creature, it must succeed on a DC 14 Constitution saving throw or become diseased. The disease has no effect for 1 minute and can be removed by any magic that cures disease. After 1 minute, the diseased creature's skin becomes translucent and slimy, the creature can't regain hit points unless it is underwater, and the disease can be removed only by heal or another disease-curing spell of 6th level or higher. When the creature is outside a body of water, it takes 6 (1d12) acid damage every 10 minutes unless moisture is applied to the skin before 10 minutes have passed. </p><p><em><strong>Tail.</strong></em> <em>Melee Weapon Attack:</em> +9 to hit, reach 10 ft. one target. <em>Hit:</em> 15 (3d6 + 5) bludgeoning damage. </p><p><em><strong>Enslave (3/Day).</strong></em> The aboleth targets one creature it can see within 30 feet of it. The target must succeed on a DC 14 Wisdom saving throw or be magically charmed by the aboleth until the aboleth dies or until it is on a different plane of existence from the target. The charmed target is under the aboleth's control and can't take reactions, and the aboleth and the target can communicate telepathically with each other over any distance. </p><p>Whenever the charmed target takes damage, the target can repeat the saving throw. On a success, the effect ends. No more than once every 24 hours, the target can also repeat the saving throw when it is at least 1 mile away from the aboleth.</p>",
#     "Legendary Actions": "<p>The aboleth can take 3 legendary actions, choosing from the options below. Only one legendary action option can be used at a time and only at the end of another creature's turn. The aboleth regains spent legendary actions at the start of its turn. </p><p><em><strong>Detect.</strong></em> The aboleth makes a Wisdom (Perception) check. </p><p><em><strong>Tail Swipe.</strong></em> The aboleth makes one tail attack. </p><p><em><strong>Psychic Drain</strong></em> (Costs 2 Actions). One creature charmed by the aboleth takes 10 (3d6) psychic damage, and the aboleth regains hit points equal to the damage the creature takes.</p>",
    
#     '''
    
#     combat_data = parse_monster_sheet(monster_sheet)
#     print(json.dumps(combat_data, indent=2))
import ollama
import re
import json

# Initialize the Ollama model
def query_mistral(prompt):
    """
    Query the Ollama model with a given prompt.
    """
    try:
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]
    except Exception as e:
        print(f"Error querying Ollama: {e}")
        return None

# Parse combat-relevant information
def parse_monster_sheet(sheet_text):
    """
    Parse a monster sheet using Ollama. Fallback to manual parsing if needed.
    """
    prompt = f"""
    Extract combat-relevant details from the following D&D monster/character sheet:

    {sheet_text}

    Strictly follow this JSON structure and provide realistic and complete values based on the input:

    {{
        "Name": "Monster/Character Name",
        "AC": "Armor Class (e.g., 17)",
        "HP": "Hit Points (e.g., 135)",
        "Speed": "Speed (e.g., 30 ft.)",
        "Attacks": [
            {{
                "Name": "Attack Name (e.g., Tentacle)",
                "ToHit": "Attack Bonus (e.g., +9)",
                "Damage": "Damage Dice (e.g., 2d6 + 5)",
                "Type": "Damage Type (e.g., Bludgeoning)"
            }}
        ],
        "Multiattack": "Describe Multiattack actions (e.g., The monster makes three tentacle attacks.)",
        "SpecialAttacks": [
            {{
                "Name": "Special Attack Name (e.g., Enslave)",
                "Description": "Full description, including mechanics and recharge rules."
            }}
        ],
        "LegendaryActions": [
            "Legendary Action 1 (e.g., Detect: The monster makes a Perception check.)",
            "Legendary Action 2 (e.g., Tail Swipe: The monster makes a tail attack.)"
        ]
    }}

    Ensure all fields have meaningful values based on the input data. If any data is missing, explain why in comments, but still adhere to the JSON structure.
    """
    # Query the AI
    response = query_mistral(prompt)
    if response:
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print("Failed to parse JSON. Attempting to extract manually...")
    
    # Fallback to manual parsing if Ollama fails
    return fallback_parse(sheet_text)

def fallback_parse(sheet_text):
    """
    Fallback mechanism to extract combat-relevant details from raw text.
    """
    print("Using fallback parser...")
    
    # Extract Name
    name = re.search(r'"name":\s*"(.*?)"', sheet_text, re.IGNORECASE)
    name = name.group(1) if name else "Unknown"

    # Extract AC
    ac = re.search(r'"Armor Class":\s*"([\d()]+)"', sheet_text, re.IGNORECASE)
    ac = ac.group(1) if ac else "Unknown"

    # Extract HP
    hp = re.search(r'"Hit Points":\s*"([\d()d+\-]+)"', sheet_text, re.IGNORECASE)
    hp = hp.group(1) if hp else "Unknown"

    # Extract Speed
    speed = re.search(r'"Speed":\s*"([\w.,\s]+)"', sheet_text, re.IGNORECASE)
    speed = speed.group(1) if speed else "Unknown"

    # Extract Attacks
    attacks = []
    attack_pattern = re.compile(
        r'<em><strong>(.*?)</strong></em>\s*<em>(?:Melee|Ranged) Weapon Attack:</em>\s*\+(\d+).*?<em>Hit:</em>\s*([\d+d+\-()\s]+)\s*(\w+)',
        re.IGNORECASE
    )
    for match in attack_pattern.finditer(sheet_text):
        attacks.append({
            "Name": match.group(1),
            "ToHit": f"+{match.group(2)}",
            "Damage": match.group(3),
            "Type": match.group(4)
        })

    # Extract Multiattack Description
    multiattack = re.search(r'<em><strong>Multiattack\.</strong></em>\s*(.*?)</p>', sheet_text, re.IGNORECASE)
    multiattack = multiattack.group(1) if multiattack else "Unknown"

    # Extract Special Attacks
    special_attacks = []
    special_pattern = re.compile(r'<em><strong>(.*?)</strong></em>(.*?)(?:</p>|$)', re.IGNORECASE)
    for match in special_pattern.finditer(sheet_text):
        if "Multiattack" not in match.group(1):
            special_attacks.append({
                "Name": match.group(1),
                "Description": match.group(2).strip()
            })

    # Extract Legendary Actions
    legendary_actions = []
    legendary_section = re.search(r'"Legendary Actions":(.*?)</p>', sheet_text, re.IGNORECASE)
    if legendary_section:
        actions = re.findall(r'<em><strong>(.*?)</strong></em>', legendary_section.group(1))
        legendary_actions = actions if actions else []

    # Return structured data
    return {
        "Name": name,
        "AC": ac,
        "HP": hp,
        "Speed": speed,
        "Attacks": attacks,
        "Multiattack": multiattack,
        "SpecialAttacks": special_attacks,
        "LegendaryActions": legendary_actions
    }

# Example usage
if __name__ == "__main__":
    monster_sheet = '''
    "name": "Aboleth",
    "meta": "Large aberration, lawful evil",
    "Armor Class": "17 (Natural Armor)",
    "Hit Points": "135 (18d10 + 36)",
    "Speed": "10 ft., swim 40 ft. ",
    "STR": "21",
    "STR_mod": "(+5)",
    "DEX": "9",
    "DEX_mod": "(-1)",
    "CON": "15",
    "CON_mod": "(+2)",
    "INT": "18",
    "INT_mod": "(+4)",
    "WIS": "15",
    "WIS_mod": "(+2)",
    "CHA": "18",
    "CHA_mod": "(+4)",
    "Saving Throws": "CON +6, INT +8, WIS +6",
    "Skills": "History +12, Perception +10",
    "Senses": "Darkvision 120 ft.,  Passive Perception 20",
    "Languages": "Deep Speech, Telepathy 120 ft.",
    "Challenge": "10 (5,900 XP)",
    "Traits": "<p><em><strong>Amphibious.</strong></em> The aboleth can breathe air and water. </p><p><em><strong>Mucous Cloud.</strong></em> While underwater, the aboleth is surrounded by transformative mucus. A creature that touches the aboleth or that hits it with a melee attack while within 5 feet of it must make a DC 14 Constitution saving throw. On a failure, the creature is diseased for 1d4 hours. The diseased creature can breathe only underwater. </p><p><em><strong>Probing Telepathy.</strong></em> If a creature communicates telepathically with the aboleth, the aboleth learns the creature's greatest desires if the aboleth can see the creature.</p>",
    "Actions": "<p><em><strong>Multiattack.</strong></em> The aboleth makes three tentacle attacks. </p><p><em><strong>Tentacle.</strong></em> <em>Melee Weapon Attack:</em> +9 to hit, reach 10 ft., one target. <em>Hit:</em> 12 (2d6 + 5) bludgeoning damage. </p><p><em><strong>Tail.</strong></em> <em>Melee Weapon Attack:</em> +9 to hit, reach 10 ft. one target. <em>Hit:</em> 15 (3d6 + 5) bludgeoning damage. </p>",
    "Legendary Actions": "<p>The aboleth can take 3 legendary actions, choosing from the options below. Only one legendary action option can be used at a time and only at the end of another creature's turn. The aboleth regains spent legendary actions at the start of its turn. </p><p><em><strong>Detect.</strong></em> The aboleth makes a Wisdom (Perception) check. </p><p><em><strong>Tail Swipe.</strong></em> The aboleth makes one tail attack. </p><p><em><strong>Psychic Drain</strong></em> (Costs 2 Actions). One creature charmed by the aboleth takes 10 (3d6) psychic damage.</p>",
    '''

    combat_data = parse_monster_sheet(monster_sheet)
    print(json.dumps(combat_data, indent=2))















