import re
from accounts.models import Monster

def parse_text_to_monster(text):
    """
    Parses monster data from text and returns a Monster object.
    """
    try:
        monster = {
            "name": re.search(r"^(.*?)\n", text).group(1).strip(),
            "size": re.search(r"(\w+)\s*fiend.*?,", text).group(1).strip(),
            "type": re.search(r"fiend\s*\((.*?)\)", text).group(1).strip(),
            "alignment": re.search(r",\s*(.*?)\n", text).group(1).strip(),
            "armor_class": int(re.search(r"Armor\s*Class\s*(\d+)", text).group(1)),
            "hit_points": int(re.search(r"Hit\s*Points\s*(\d+)", text).group(1)),
            "speed": re.search(r"Speed\s*(.*)", text).group(1).strip(),
            "strength": int(re.findall(r"STR.*?(\d+)", text)[0]),
            "dexterity": int(re.findall(r"DEX.*?(\d+)", text)[0]),
            "constitution": int(re.findall(r"CON.*?(\d+)", text)[0]),
            "intelligence": int(re.findall(r"INT.*?(\d+)", text)[0]),
            "wisdom": int(re.findall(r"WIS.*?(\d+)", text)[0]),
            "charisma": int(re.findall(r"CHA.*?(\d+)", text)[0]),
            "saving_throws": re.search(r"Saving\s*Throws\s*(.*?)\n", text).group(1).strip(),
            "damage_resistances": re.search(r"Damage\s*Resistances\s*(.*?)\n", text).group(1).strip(),
            "damage_immunities": re.search(r"Damage\s*Immunities\s*(.*?)\n", text).group(1).strip(),
            "condition_immunities": re.search(r"Condition\s*Immunities\s*(.*?)\n", text).group(1).strip(),
            "senses": re.search(r"Senses\s*(.*?)\n", text).group(1).strip(),
            "languages": re.search(r"Languages\s*(.*?)\n", text).group(1).strip(),
            "challenge_rating": re.search(r"Challenge\s*(.*?)\n", text).group(1).strip(),
            "abilities": re.search(r"(Hellish.*?Magic\s*Resistance.*?)Actions", text, re.S).group(1).strip(),
            "actions": re.search(r"Actions\s*(.*?)Reactions", text, re.S).group(1).strip(),
            "reactions": re.search(r"Reactions\s*(.*?)$", text, re.S).group(1).strip(),
        }
        
        return monster

    except (AttributeError, IndexError, ValueError) as e:
        raise ValueError(f"Parsing error: {e}")
