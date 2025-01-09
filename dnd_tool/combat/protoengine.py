# import json
# from dnd_combat_parser import parse_monster_sheet

# # Simulate a basic combat
# def simulate_combat(monster_1, monster_2):
#     print("\n⚔️ Starting Combat Simulation!")
#     print(f"{monster_1['Name']} vs {monster_2['Name']}")
    
#     # Extract necessary details
#     monster_1_hp = int(monster_1['HP'].split(' ')[0])  # Assuming HP is formatted as "135 (18d10 + 36)"
#     monster_2_hp = int(monster_2['HP'].split(' ')[0])
#     monster_1_ac = int(monster_1['AC'])
#     monster_2_ac = int(monster_2['AC'])
    
#     # Use the first attack for simulation
#     monster_1_attack = monster_1['Attacks'][0] if monster_1['Attacks'] else None
#     monster_2_attack = monster_2['Attacks'][0] if monster_2['Attacks'] else None

#     round_counter = 1

#     # Run combat for up to 5 rounds or until one monster is defeated
#     while monster_1_hp > 0 and monster_2_hp > 0 and round_counter <= 5:
#         print(f"\n--- 🕒 Round {round_counter} ---")

#         # Monster 1 attacks Monster 2
#         if monster_1_attack:
#             to_hit = int(monster_1_attack['ToHit'].replace('+', ''))
#             damage = eval(monster_1_attack['Damage'].replace('d', '*'))  # Convert "2d6+5" to 2*6+5
#             print(f"{monster_1['Name']} attacks {monster_2['Name']} with {monster_1_attack['Name']}!")
#             if to_hit >= monster_2_ac:
#                 monster_2_hp -= damage
#                 print(f"  - Hit! {monster_2['Name']} takes {damage} damage! ({monster_2_hp} HP left)")
#             else:
#                 print(f"  - Miss!")

#         # Monster 2 attacks Monster 1
#         if monster_2_attack:
#             to_hit = int(monster_2_attack['ToHit'].replace('+', ''))
#             damage = eval(monster_2_attack['Damage'].replace('d', '*'))  # Convert "3d6+5" to 3*6+5
#             print(f"{monster_2['Name']} attacks {monster_1['Name']} with {monster_2_attack['Name']}!")
#             if to_hit >= monster_1_ac:
#                 monster_1_hp -= damage
#                 print(f"  - Hit! {monster_1['Name']} takes {damage} damage! ({monster_1_hp} HP left)")
#             else:
#                 print(f"  - Miss!")

#         round_counter += 1

#     # Determine the winner
#     print("\n🏆 Combat Over!")
#     if monster_1_hp > monster_2_hp:
#         print(f"Winner: {monster_1['Name']}")
#     elif monster_2_hp > monster_1_hp:
#         print(f"Winner: {monster_2['Name']}")
#     else:
#         print("It's a draw!")

# # Main function
# if __name__ == '__main__':
#     # Example monster sheets
#     monster_sheet_1 = '''
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

#     monster_sheet_2 = '''
#     "name": "Adult Red Dragon",
#     "meta": "Huge dragon, chaotic evil",
#     "Armor Class": "19 (Natural Armor)",
#     "Hit Points": "256 (19d12 + 133)",
#     "Speed": "40 ft., climb 40 ft., fly 80 ft. ",
#     "STR": "27",
#     "STR_mod": "(+8)",
#     "DEX": "10",
#     "DEX_mod": "(+0)",
#     "CON": "25",
#     "CON_mod": "(+7)",
#     "INT": "16",
#     "INT_mod": "(+3)",
#     "WIS": "13",
#     "WIS_mod": "(+1)",
#     "CHA": "21",
#     "CHA_mod": "(+5)",
#     "Saving Throws": "DEX +6, CON +13, WIS +7, CHA +11",
#     "Skills": "Perception +13, Stealth +6",
#     "Damage Immunities": "Fire",
#     "Senses": "Blindsight 60 ft., Darkvision 120 ft.,  Passive Perception 23",
#     "Languages": "Common, Draconic",
#     "Challenge": "17 (18,000 XP)",
#     "Traits": "<p><em><strong>Legendary Resistance (3/Day).</strong></em> If the dragon fails a saving throw, it can choose to succeed instead.</p>",
#     "Actions": "<p><em><strong>Multiattack.</strong></em> The dragon can use its Frightful Presence. It then makes three attacks: one with its bite and two with its claws. </p><p><em><strong>Bite.</strong></em> <em>Melee Weapon Attack:</em> +14 to hit, reach 10 ft., one target. <em>Hit:</em> 19 (2d10 + 8) piercing damage plus 7 (2d6) fire damage. </p><p><em><strong>Claw.</strong></em> <em>Melee Weapon Attack:</em> +14 to hit, reach 5 ft., one target. <em>Hit:</em> 15 (2d6 + 8) slashing damage. </p><p><em><strong>Tail.</strong></em> <em>Melee Weapon Attack:</em> +14 to hit, reach 15 ft., one target. <em>Hit:</em> 17 (2d8 + 8) bludgeoning damage. </p><p><em><strong>Frightful Presence.</strong></em> Each creature of the dragon's choice that is within 120 feet of the dragon and aware of it must succeed on a DC 19 Wisdom saving throw or become frightened for 1 minute. A creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success. If a creature's saving throw is successful or the effect ends for it, the creature is immune to the dragon's Frightful Presence for the next 24 hours. </p><p><em><strong>Fire Breath (Recharge 5–6).</strong></em> The dragon exhales fire in a 60-foot cone. Each creature in that area must make a DC 21 Dexterity saving throw, taking 63 (18d6) fire damage on a failed save, or half as much damage on a successful one.</p>",
#     "Legendary Actions": "<p>The dragon can take 3 legendary actions, choosing from the options below. Only one legendary action option can be used at a time and only at the end of another creature's turn. The dragon regains spent legendary actions at the start of its turn. </p><p><em><strong>Detect.</strong></em> The dragon makes a Wisdom (Perception) check. </p><p><em><strong>Tail Attack.</strong></em> The dragon makes a tail attack. </p><p><em><strong>Wing Attack (Costs 2 Actions).</strong></em> The dragon beats its wings. Each creature within 10 feet of the dragon must succeed on a DC 22 Dexterity saving throw or take 15 (2d6 + 8) bludgeoning damage and be knocked prone. The dragon can then fly up to half its flying speed.</p>",
    
#     '''

#     # Parse monster data
#     monster_1 = parse_monster_sheet(monster_sheet_1)
#     monster_2 = parse_monster_sheet(monster_sheet_2)

#     # Ensure both monsters parsed correctly
#     if monster_1 and monster_2:
#         simulate_combat(monster_1, monster_2)
#     else:
#         print("Failed to parse one or both monsters.")








from dnd_combat_parser import parse_monster_sheet
import random

def roll_d20():
    """Simulates a d20 roll."""
    return random.randint(1, 20)

def calculate_damage(damage_expression):
    """Calculates average damage from a damage expression."""
    # Example: "2d10 + 8"
    try:
        parts = damage_expression.split("+")
        dice = parts[0].strip()
        modifier = int(parts[1].strip()) if len(parts) > 1 else 0

        num_dice, dice_type = map(int, dice.lower().replace("d", " ").split())
        avg_roll = (1 + dice_type) / 2  # Average roll of a die
        return num_dice * avg_roll + modifier
    except Exception:
        return 0  # Fallback if parsing fails

def simulate_combat(monster_1, monster_2):
    """Simulates combat between two monsters parsed from dnd_combat_parser."""
    print(f"⚔️ {monster_1['Name']} vs {monster_2['Name']} ⚔️")
    print(f"{monster_1['Name']} starts with {monster_1['HP']} HP")
    print(f"{monster_2['Name']} starts with {monster_2['HP']} HP\n")

    monster_1_hp = int(monster_1["HP"].split()[0])
    monster_2_hp = int(monster_2["HP"].split()[0])

    turn = 1
    while monster_1_hp > 0 and monster_2_hp > 0:
        print(f"--- 🕒 **Turn {turn}** ---")

        # Monster 1 attacks Monster 2
        for attack in monster_1["Attacks"]:
            to_hit = int(attack["ToHit"])
            damage = calculate_damage(attack["Damage"])
            roll = roll_d20()
            if roll + to_hit >= int(monster_2["AC"].split()[0]):
                monster_2_hp -= damage
                print(f"{monster_1['Name']} hits {monster_2['Name']} with {attack['Name']} for {damage} damage! ({monster_2_hp} HP remaining)")
            else:
                print(f"{monster_1['Name']} misses {monster_2['Name']} with {attack['Name']}!")

            if monster_2_hp <= 0:
                break

        if monster_2_hp <= 0:
            print(f"\n🏆 {monster_1['Name']} wins!")
            break

        # Monster 2 attacks Monster 1
        for attack in monster_2["Attacks"]:
            to_hit = int(attack["ToHit"])
            damage = calculate_damage(attack["Damage"])
            roll = roll_d20()
            if roll + to_hit >= int(monster_1["AC"].split()[0]):
                monster_1_hp -= damage
                print(f"{monster_2['Name']} hits {monster_1['Name']} with {attack['Name']} for {damage} damage! ({monster_1_hp} HP remaining)")
            else:
                print(f"{monster_2['Name']} misses {monster_1['Name']} with {attack['Name']}!")

            if monster_1_hp <= 0:
                break

        if monster_1_hp <= 0:
            print(f"\n🏆 {monster_2['Name']} wins!")
            break

        turn += 1

    if monster_1_hp > 0 and monster_2_hp > 0:
        print("\n🏆 The battle ends in a draw!")

if __name__ == "__main__":
    # Example monster sheets
    monster_sheet_1 = '''
    "name": "Adult Red Dragon",
    "meta": "Huge dragon, chaotic evil",
    "Armor Class": "19 (Natural Armor)",
    "Hit Points": "256 (19d12 + 133)",
    "Speed": "40 ft., climb 40 ft., fly 80 ft. ",
    "STR": "27",
    "STR_mod": "(+8)",
    "DEX": "10",
    "DEX_mod": "(+0)",
    "CON": "25",
    "CON_mod": "(+7)",
    "INT": "16",
    "INT_mod": "(+3)",
    "WIS": "13",
    "WIS_mod": "(+1)",
    "CHA": "21",
    "CHA_mod": "(+5)",
    "Saving Throws": "DEX +6, CON +13, WIS +7, CHA +11",
    "Skills": "Perception +13, Stealth +6",
    "Damage Immunities": "Fire",
    "Senses": "Blindsight 60 ft., Darkvision 120 ft.,  Passive Perception 23",
    "Languages": "Common, Draconic",
    "Challenge": "17 (18,000 XP)",
    "Traits": "<p><em><strong>Legendary Resistance (3/Day).</strong></em> If the dragon fails a saving throw, it can choose to succeed instead.</p>",
    "Actions": "<p><em><strong>Multiattack.</strong></em> The dragon can use its Frightful Presence. It then makes three attacks: one with its bite and two with its claws. </p><p><em><strong>Bite.</strong></em> <em>Melee Weapon Attack:</em> +14 to hit, reach 10 ft., one target. <em>Hit:</em> 19 (2d10 + 8) piercing damage plus 7 (2d6) fire damage. </p><p><em><strong>Claw.</strong></em> <em>Melee Weapon Attack:</em> +14 to hit, reach 5 ft., one target. <em>Hit:</em> 15 (2d6 + 8) slashing damage. </p><p><em><strong>Tail.</strong></em> <em>Melee Weapon Attack:</em> +14 to hit, reach 15 ft., one target. <em>Hit:</em> 17 (2d8 + 8) bludgeoning damage. </p><p><em><strong>Frightful Presence.</strong></em> Each creature of the dragon's choice that is within 120 feet of the dragon and aware of it must succeed on a DC 19 Wisdom saving throw or become frightened for 1 minute. A creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success. If a creature's saving throw is successful or the effect ends for it, the creature is immune to the dragon's Frightful Presence for the next 24 hours. </p><p><em><strong>Fire Breath (Recharge 5–6).</strong></em> The dragon exhales fire in a 60-foot cone. Each creature in that area must make a DC 21 Dexterity saving throw, taking 63 (18d6) fire damage on a failed save, or half as much damage on a successful one.</p>",
    "Legendary Actions": "<p>The dragon can take 3 legendary actions, choosing from the options below. Only one legendary action option can be used at a time and only at the end of another creature's turn. The dragon regains spent legendary actions at the start of its turn. </p><p><em><strong>Detect.</strong></em> The dragon makes a Wisdom (Perception) check. </p><p><em><strong>Tail Attack.</strong></em> The dragon makes a tail attack. </p><p><em><strong>Wing Attack (Costs 2 Actions).</strong></em> The dragon beats its wings. Each creature within 10 feet of the dragon must succeed on a DC 22 Dexterity saving throw or take 15 (2d6 + 8) bludgeoning damage and be knocked prone. The dragon can then fly up to half its flying speed.</p>",
    '''

    monster_sheet_2 = '''
    "name": "Adult White Dragon",
    "Armor Class": "18 (Natural Armor)",
    "Hit Points": "200 (16d12 + 96)",
    "Speed": "40 ft., fly 80 ft., swim 40 ft.",
    "Actions": "<p><em><strong>Multiattack.</strong></em> The dragon makes three attacks: one with its bite and two with its claws. </p><p><em><strong>Bite.</strong></em> <em>Melee Weapon Attack:</em> +11 to hit, reach 10 ft., one target. <em>Hit:</em> 17 (2d10 + 6) piercing damage plus 4 (1d8) cold damage. </p><p><em><strong>Claw.</strong></em> <em>Melee Weapon Attack:</em> +11 to hit, reach 5 ft., one target. <em>Hit:</em> 13 (2d6 + 6) slashing damage. </p>",
    '''

    # Parse the monster sheets
    monster_1 = parse_monster_sheet(monster_sheet_1)
    monster_2 = parse_monster_sheet(monster_sheet_2)

    # Simulate combat
    if monster_1 and monster_2:
        simulate_combat(monster_1, monster_2)
    else:
        print("Failed to parse one or both monsters.")
