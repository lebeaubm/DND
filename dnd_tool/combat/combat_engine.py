import random
import re
# from ollama_parser import parse_monster_sheet
# from damage_calculator import calculate_accurate_damage


class Entity:
    def __init__(self, name, hp, actions):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.actions = actions
        self.attacks = []
        self.multiattack_pattern = []
        self.parse_attacks(actions)

    def calculate_average_damage(self, damage_text):
        """
        Calculate average damage from dice notation (e.g., '2d6+3')
        """
        dice_match = re.match(r'(\d+)d(\d+)(?:\s*\+\s*(\d+))?', damage_text)
        if not dice_match:
            return 0

        num_dice = int(dice_match.group(1))
        dice_sides = int(dice_match.group(2))
        bonus = int(dice_match.group(3)) if dice_match.group(3) else 0

        avg_damage = (num_dice * (dice_sides + 1) / 2) + bonus
        return avg_damage

    def parse_attacks(self, actions):
        """
        Parse the attack descriptions from the 'Actions' field.
        """
        self.attacks = []
        if not actions:
            return

        attack_patterns = [
            (r'\*\*(.*?)\.\*\*.*?\+(\d+).*?Hit:.*?\(([\d+d\+\-]+)\)', 'explicit'),  # Named attack patterns
            (r'\*\*(.*?)\.\*\*.*?Hit:.*?(\d+)', 'average_damage')  # Fallback average damage patterns
        ]

        for pattern, _type in attack_patterns:
            for match in re.finditer(pattern, actions):
                name = match.group(1).strip().lower()
                bonus = int(match.group(2)) if len(match.groups()) > 1 else 0
                avg_damage = self.calculate_average_damage(match.group(3)) if len(match.groups()) > 2 else 0

                self.attacks.append({
                    'name': name,
                    'bonus': bonus,
                    'avg_damage': avg_damage
                })

        # Debugging parsed attacks
        print(f"DEBUG: {self.name} Parsed Attacks: {self.attacks}")

        # Extract Multiattack Pattern
        multiattack_match = re.search(r'\*\*Multiattack\.\*\* The .*? makes (.*?)\.', actions)
        if multiattack_match:
            attack_sequence = multiattack_match.group(1)
            # Extract attack types and quantities
            attack_list = re.findall(r'one with its (\w+)|two with its (\w+)', attack_sequence)
            for one, two in attack_list:
                if one:
                    self.multiattack_pattern.append(one.lower())
                if two:
                    self.multiattack_pattern.extend([two.lower()] * 2)

            print(f"DEBUG: {self.name} Multiattack Pattern: {self.multiattack_pattern}")

    def normalize_attack_name(self, attack_name):
        """
        Normalize attack names to match available attacks.
        """
        attack_name_clean = attack_name.strip().rstrip('.').lower()
        if attack_name_clean.endswith('s'):  # Handle plural forms like 'claws'
            attack_name_clean = attack_name_clean.rstrip('s')
        return attack_name_clean

    def perform_attack(self, target, attack_name):
        """
        Handles a single attack of a specific type against a target.
        """
        attack_name_clean = self.normalize_attack_name(attack_name)
        print(f"DEBUG: {self.name} attempting attack '{attack_name_clean}'")
        print(f"DEBUG: Available Attacks: {[atk['name'] for atk in self.attacks]}")

        matching_attacks = [
            atk for atk in self.attacks
            if atk['name'] == attack_name_clean
        ]

        if not matching_attacks:
            print(f"DEBUG: No matching attack found for '{attack_name_clean}'")
            return f"  - **{attack_name_clean}** attack failed! {self.name} doesn't know how to use it.\n"

        attack = matching_attacks[0]
        hit_roll = random.randint(1, 20) + attack['bonus']
        if hit_roll >= 15:  # Arbitrary AC for now
            damage = attack['avg_damage']
            target.hp -= damage
            return f"  - **{attack['name']}** hits for {damage} damage! {target.name} now has {max(0, target.hp)} HP.\n"
        else:
            return f"  - **{attack['name']}** misses.\n"

    def perform_multiattack(self, target):
        """
        Handles multiattack pattern.
        """
        print(f"{self.name} performs Multiattack:")
        log = ""
        for attack_name in self.multiattack_pattern:
            log += self.perform_attack(target, attack_name)
        return log

    def is_alive(self):
        return self.hp > 0


def run_combat(team_a, team_b, max_rounds=5):
    """
    Simulates combat between two teams.
    """
    combat_log = "==== Combat Log ====\n\n"

    # Initiative order
    combatants = team_a + team_b
    random.shuffle(combatants)
    combatants.sort(key=lambda entity: random.randint(1, 20), reverse=True)

    combat_log += "⚔️ **Combat Start! Initiative Order:**\n"
    for entity in combatants:
        combat_log += f"- {entity.name} (Initiative: {random.randint(1, 20)})\n"
    combat_log += "\n"

    for round_num in range(1, max_rounds + 1):
        combat_log += f"--- 🕒 **Round {round_num}** ---\n"
        for entity in combatants:
            if not entity.is_alive():
                continue

            target_team = team_b if entity in team_a else team_a
            target = next((t for t in target_team if t.is_alive()), None)
            if not target:
                break

            if entity.multiattack_pattern:
                combat_log += f"{entity.name} attacks {target.name}!\n"
                combat_log += entity.perform_multiattack(target)
            else:
                combat_log += f"{entity.name} attacks {target.name}!\n"
                combat_log += entity.perform_attack(target, 'claw')

            if not target.is_alive():
                combat_log += f"💀 {target.name} has fallen!\n"

    combat_log += "\n🏆 **Combat Over! Winner: Draw**\n"
    return combat_log



# def simulate_combat(monster_1_text, monster_2_text):
#     """
#     Simulates combat between two parsed monsters.
#     """
#     monster_1 = parse_monster_sheet(monster_1_text)
#     monster_2 = parse_monster_sheet(monster_2_text)
    
#     if not monster_1 or not monster_2:
#         print("Failed to parse one or both monsters.")
#         return
    
#     hp1 = int(monster_1['HP'].split(' ')[0])
#     hp2 = int(monster_2['HP'].split(' ')[0])
#     ac1 = int(monster_1['AC'])
#     ac2 = int(monster_2['AC'])
    
#     print(f"⚔️ Combat Start: {monster_1['Name']} vs {monster_2['Name']} ⚔️")
    
#     round_counter = 1
#     while hp1 > 0 and hp2 > 0 and round_counter <= 5:
#         print(f"--- 🕒 Round {round_counter} ---")
        
#         # Monster 1 Attacks
#         for attack in monster_1['Attacks']:
#             attack_name = attack['Name']
#             to_hit = int(attack['ToHit'].replace('+', ''))
#             damage = attack['Damage']
            
#             damage_output = calculate_accurate_damage(to_hit, damage, ac2)
#             hp2 -= damage_output
#             print(f"{monster_1['Name']} uses {attack_name} → Deals {damage_output:.1f} damage. {monster_2['Name']} has {hp2:.1f} HP left.")
#             if hp2 <= 0:
#                 print(f"🏆 {monster_1['Name']} wins!")
#                 return
        
#         # Monster 2 Attacks
#         for attack in monster_2['Attacks']:
#             attack_name = attack['Name']
#             to_hit = int(attack['ToHit'].replace('+', ''))
#             damage = attack['Damage']
            
#             damage_output = calculate_accurate_damage(to_hit, damage, ac1)
#             hp1 -= damage_output
#             print(f"{monster_2['Name']} uses {attack_name} → Deals {damage_output:.1f} damage. {monster_1['Name']} has {hp1:.1f} HP left.")
#             if hp1 <= 0:
#                 print(f"🏆 {monster_2['Name']} wins!")
#                 return
        
#         round_counter += 1
    
#     print("🏆 Combat ends in a draw after 5 rounds!")


# Test Example
if __name__ == '__main__':
    red_dragon = Entity('Adult Red Dragon', 250, '**Multiattack.** The dragon makes three attacks: one with its bite and two with its claws. **Bite.** +14 to hit, Hit: (2d10+8). **Claw.** +14 to hit, Hit: (2d6+8).')
    white_dragon = Entity('Adult White Dragon', 250, '**Multiattack.** The dragon makes three attacks: one with its bite and two with its claws. **Bite.** +12 to hit, Hit: (2d10+6). **Claw.** +12 to hit, Hit: (2d6+6).')

    print(run_combat([red_dragon], [white_dragon]))
