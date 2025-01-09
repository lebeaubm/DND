import re
import math

# Accurate Average Damage Formula
def calculate_accurate_average_damage(avg_damage_per_hit, chance_to_hit, chance_to_crit):
    avg_crit_damage = avg_damage_per_hit * 2
    return (avg_damage_per_hit * (chance_to_hit - chance_to_crit)) + (avg_crit_damage * chance_to_crit)

# Extract key details from the monster stat block
def parse_monster_stat_block(stat_block):
    stats = {}
    
    # Extract AC
    ac_match = re.search(r"Armor Class (\d+)", stat_block)
    stats['AC'] = int(ac_match.group(1)) if ac_match else 15  # Default AC
    
    # Extract HP
    hp_match = re.search(r"Hit Points (\d+)", stat_block)
    stats['HP'] = int(hp_match.group(1)) if hp_match else 100  # Default HP
    
    # Extract Multiattack details
    multiattack_match = re.search(r"Multiattack.*?(\d+)", stat_block)
    stats['attacks_per_round'] = int(multiattack_match.group(1)) if multiattack_match else 1  # Default 1 attack
    
    # Extract attack bonus
    attack_match = re.search(r"to hit, reach.*?\+(\d+)", stat_block)
    stats['attack_bonus'] = int(attack_match.group(1)) if attack_match else 5  # Default +5
    
    # Extract damage
    damage_match = re.findall(r"\((\d+d\d+)\)", stat_block)
    if damage_match:
        damage = damage_match[0]
        dice_count, dice_type = map(int, damage.split('d'))
        stats['damage_dice'] = (dice_count, dice_type)
    else:
        stats['damage_dice'] = (1, 8)  # Default 1d8
    
    # Extract damage modifier
    mod_match = re.search(r"Hit:.*?\((\d+)\)", stat_block)
    stats['damage_modifier'] = int(mod_match.group(1)) if mod_match else 0  # Default 0
    
    return stats

# Calculate average damage per round
def calculate_dpr(stats, target_ac=18):
    # Average damage per hit
    dice_avg = (stats['damage_dice'][1] + 1) / 2
    avg_damage_per_hit = (dice_avg * stats['damage_dice'][0]) + stats['damage_modifier']
    
    # Chance to hit
    chance_to_hit = max((21 - target_ac + stats['attack_bonus']) / 20, 0)
    chance_to_crit = 1 / 20  # Default 5% crit chance
    
    # Accurate Average Damage per hit
    avg_damage = calculate_accurate_average_damage(avg_damage_per_hit, chance_to_hit, chance_to_crit)
    
    # Total DPR considering Multiattack
    total_dpr = avg_damage * stats['attacks_per_round']
    return total_dpr

# Main execution
if __name__ == "__main__":
    monster_text = """
    Ancient White Dragon
    Gargantuan dragon, chaotic evil
    Armor Class 20 (natural armor)
    Hit Points 333 (18d20+144)
    Speed 40 ft., fly 80 ft., swim 40 ft.
    
    Multiattack. The dragon makes three attacks: one with its bite and two with its claws.
    Bite. Melee Weapon Attack: +14 to hit, reach 15 ft., one target. Hit: (2d10+8) piercing damage.
    Claw. Melee Weapon Attack: +14 to hit, reach 10 ft., one target. Hit: (2d6+8) slashing damage.
    """
    
    stats = parse_monster_stat_block(monster_text)
    dpr = calculate_dpr(stats)
    
    print("📊 Monster Combat Stats:")
    print(f"Armor Class: {stats['AC']}")
    print(f"Hit Points: {stats['HP']}")
    print(f"Attacks Per Round: {stats['attacks_per_round']}")
    print(f"Attack Bonus: +{stats['attack_bonus']}")
    print(f"Damage Dice: {stats['damage_dice'][0]}d{stats['damage_dice'][1]}")
    print(f"Damage Modifier: +{stats['damage_modifier']}")
    print(f"🎯 Estimated DPR (vs AC 18): {dpr:.2f}")
