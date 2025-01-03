import random


class Entity:
    def __init__(self, name, attack_bonus, damage_dice, crit_range, ac, hp):
        """
        Initialize an Entity (Character, Monster, etc.)
        :param name: Entity name
        :param attack_bonus: Attack roll bonus
        :param damage_dice: Damage dice string (e.g., '2d6+4')
        :param crit_range: Range for a critical hit (e.g., 20, 19-20)
        :param ac: Armor Class
        :param hp: Hit Points
        """
        self.name = name
        self.attack_bonus = attack_bonus  # Bonus to attack rolls
        self.damage_dice = damage_dice  # e.g., '2d6+4'
        self.crit_range = crit_range  # Usually 20, but may be 19-20, etc.
        self.ac = ac  # Armor Class
        self.hp = hp  # Current HP

    def roll_damage(self):
        """
        Parse the damage dice string and calculate average and critical damage.
        :return: avg_damage, crit_damage
        """
        num_dice, dice_size, modifier = self.parse_damage_dice(self.damage_dice)
        avg_damage = (num_dice * (dice_size + 1) / 2) + modifier
        crit_damage = (num_dice * (dice_size + 1)) + modifier
        return avg_damage, crit_damage

    @staticmethod
    def parse_damage_dice(damage_dice):
        """
        Parse a damage dice string like '2d6+4'.
        :param damage_dice: Damage dice string
        :return: num_dice, dice_size, modifier
        """
        parts = damage_dice.split('d')
        num_dice = int(parts[0])
        if '+' in parts[1]:
            dice_size, modifier = map(int, parts[1].split('+'))
        elif '-' in parts[1]:
            dice_size, modifier = map(int, parts[1].split('-'))
            modifier = -modifier
        else:
            dice_size = int(parts[1])
            modifier = 0
        return num_dice, dice_size, modifier

    def calculate_hit_chance(self, target_ac):
        """
        Calculate the chance to hit and crit against a target.
        :param target_ac: Target's Armor Class
        :return: chance_to_hit, chance_to_crit
        """
        chance_to_hit = max(0, (21 - (target_ac - self.attack_bonus)) / 20)
        chance_to_crit = (21 - self.crit_range) / 20
        return chance_to_hit, chance_to_crit

    def calculate_accurate_average_damage(self, target_ac):
        """
        Calculate damage using the Accurate Average Damage Formula.
        :param target_ac: Target's Armor Class
        :return: Accurate average damage
        """
        avg_damage, avg_crit_damage = self.roll_damage()
        chance_to_hit, chance_to_crit = self.calculate_hit_chance(target_ac)

        accurate_avg_damage = (avg_damage * (chance_to_hit - chance_to_crit)) + (avg_crit_damage * chance_to_crit)
        return accurate_avg_damage

    def is_alive(self):
        """Check if the entity is still alive."""
        return self.hp > 0


def roll_initiative(entities):
    """
    Roll initiative for all entities.
    :param entities: List of Entity objects
    :return: List of Entity objects sorted by initiative
    """
    initiatives = []
    for entity in entities:
        initiative = random.randint(1, 20) + entity.attack_bonus
        initiatives.append((initiative, entity))
    initiatives.sort(reverse=True, key=lambda x: x[0])
    return [entity for _, entity in initiatives]


def run_combat(team_a, team_b):
    """
    Simulate combat between two teams.
    :param team_a: List of Entity objects (Team A)
    :param team_b: List of Entity objects (Team B)
    :return: Combat results as a list of strings
    """
    combat_log = []
    all_combatants = team_a + team_b
    all_combatants = roll_initiative(all_combatants)

    round_number = 1
    combat_log.append(f"⚔️ Combat Begins! Initiative Order: {[entity.name for entity in all_combatants]} ⚔️")

    while any(entity.is_alive() for entity in team_a) and any(entity.is_alive() for entity in team_b):
        combat_log.append(f"\n🛡️ --- Round {round_number} --- 🛡️")
        for attacker in all_combatants:
            if not attacker.is_alive():
                continue

            # Determine Target
            target_team = team_b if attacker in team_a else team_a
            living_targets = [t for t in target_team if t.is_alive()]
            if not living_targets:
                continue

            target = random.choice(living_targets)
            damage = attacker.calculate_accurate_average_damage(target.ac)
            target.hp -= damage

            combat_log.append(
                f"⚔️ {attacker.name} attacks {target.name} and deals {damage:.2f} damage! ({target.name} HP: {target.hp:.2f})"
            )

            if target.hp <= 0:
                combat_log.append(f"💀 {target.name} has fallen!")

        round_number += 1

        if not any(entity.is_alive() for entity in team_a):
            combat_log.append("\n🏆 Team B wins the battle!")
            break
        if not any(entity.is_alive() for entity in team_b):
            combat_log.append("\n🏆 Team A wins the battle!")
            break

    return combat_log


# Example Usage (Testing)
if __name__ == "__main__":
    team_a = [
        Entity("Hero1", attack_bonus=5, damage_dice="2d6+3", crit_range=20, ac=15, hp=50),
        Entity("Hero2", attack_bonus=6, damage_dice="1d8+4", crit_range=19, ac=16, hp=60),
    ]

    team_b = [
        Entity("Monster1", attack_bonus=4, damage_dice="2d10+2", crit_range=20, ac=14, hp=55),
        Entity("Monster2", attack_bonus=5, damage_dice="1d12+3", crit_range=19, ac=13, hp=65),
    ]

    # results = run_combat(team_a, team_b)
    # for line in results:
    #     print(line)


# Run the Combat Simulation
    results = run_combat(team_a, team_b)
    
    # Print Combat Log
    print("\n=== Combat Log ===")
    for line in results:
        print(line)

        