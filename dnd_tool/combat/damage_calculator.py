import re

def calculate_accurate_damage(to_hit_bonus, damage_formula, target_ac):
    """
    Calculate accurate average damage based on your formula.
    """
    import random

    # Extract damage values
    damage_parts = re.findall(r'(\d+)d(\d+)', damage_formula)
    flat_bonus = sum(map(int, re.findall(r'\+(\d+)', damage_formula)))

    avg_damage = 0
    for num_dice, die_type in damage_parts:
        avg_damage += int(num_dice) * ((int(die_type) + 1) / 2)

    avg_damage += flat_bonus

    # Calculate chance to hit
    chance_to_hit = max(min((21 - target_ac + to_hit_bonus) / 20, 1), 0)
    chance_to_crit = 1 / 20

    avg_crit_damage = avg_damage * 2

    accurate_avg_damage = (avg_damage * (chance_to_hit - chance_to_crit)) + (avg_crit_damage * chance_to_crit)
    return accurate_avg_damage
