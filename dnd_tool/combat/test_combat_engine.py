from combat_engine import Entity, run_combat

# Test Entities
attacker = Entity(
    name="Adult Red Dragon",
    hp=256,
    attacks=(
        "**Multiattack.** The dragon can use its Frightful Presence. It then makes three attacks: one with its bite and two with its claws. "
        "**Bite.** +14 to hit, Hit: 19 (2d10 + 8) piercing damage plus 7 (2d6) fire damage. "
        "**Claw.** +14 to hit, Hit: 15 (2d6 + 8) slashing damage. "
        "**Tail.** +14 to hit, Hit: 17 (2d8 + 8) bludgeoning damage."
    ),
    initiative=15
)

defender = Entity(
    name="Adult White Dragon",
    hp=200,
    attacks=(
        "**Multiattack.** The dragon makes three attacks: one with its bite and two with its claws. "
        "**Bite.** +12 to hit, Hit: 16 (2d10 + 6) piercing damage plus 5 (1d10) cold damage. "
        "**Claw.** +12 to hit, Hit: 12 (2d6 + 6) slashing damage."
    ),
    initiative=12
)

# Simulate Combat
if __name__ == "__main__":
    team_a = [attacker]
    team_b = [defender]

    winner, combat_log = run_combat(team_a, team_b)

    print("\n==== Combat Log ====\n")
    print(combat_log)
    print(f"\n🏆 Winner: {winner}")
