import random

class Entity:
    def __init__(self, name, hp, ac, initiative, attack_bonus, damage, team):
        self.name = name
        self.hp = hp
        self.ac = ac
        self.initiative = initiative
        self.attack_bonus = attack_bonus
        self.damage = damage
        self.team = team

    @classmethod
    def from_db_object(cls, obj):
        return cls(
            name=obj.name,
            hp=obj.hit_points or 0,
            ac=obj.armor_class or 0,
            initiative=obj.dexterity or 10,
            attack_bonus=obj.strength or 0,
            damage=10,  # Example fixed damage
            team=None
        )

def run_combat(team_a, team_b):
    combat_log = []
    all_combatants = team_a + team_b
    all_combatants.sort(key=lambda x: x.initiative, reverse=True)
    
    while any(entity.hp > 0 for entity in team_a) and any(entity.hp > 0 for entity in team_b):
        for entity in all_combatants:
            if entity.hp <= 0:
                continue
            
            target_team = team_b if entity in team_a else team_a
            target = next((t for t in target_team if t.hp > 0), None)
            
            if target:
                target.hp -= entity.damage
                combat_log.append(f"{entity.name} attacked {target.name} for {entity.damage} damage. {target.name} has {target.hp} HP left.")
                
                if target.hp <= 0:
                    combat_log.append(f"{target.name} has fallen!")
    
    winner = "Team A" if any(entity.hp > 0 for entity in team_a) else "Team B"
    combat_log.append(f"🏆 {winner} wins the battle!")
    return combat_log
