import random
import os
import platform

from hero import Hero
from monster import Monster
import functions

# Print system info (Requirement 9 & 10)
print("Operating System:", os.name)
print("Python Version:", platform.python_version())

# Define Dice and Data
small_dice_options = list(range(1, 7))
big_dice_options = list(range(1, 21))
weapons = ["Fist", "Knife", "Club", "Gun", "Bomb", "Nuclear Bomb"]
loot_options = ["Health Potion", "Poison Potion", "Secret Note", "Leather Boots", "Flimsy Gloves"]
monster_powers = {"Fire Magic": 2, "Freeze Time": 4, "Super Hearing": 6}
belt = []

# Create hero and monster objects
hero = Hero()
monster = Monster()

# Input loop for combat strength override (still allows user input)
i = 0
while i < 5:
    try:
        combat_strength = int(input("Enter your combat Strength (1-6): "))
        m_combat_strength = int(input("Enter the monster's combat Strength (1-6): "))
        if 1 <= combat_strength <= 6 and 1 <= m_combat_strength <= 6:
            hero.combat_strength = combat_strength
            monster.combat_strength = m_combat_strength
            break
        else:
            print("Please enter values between 1 and 6 only.")
    except ValueError:
        print("Invalid input. Please enter numeric values.")
    i += 1

# Roll weapon
input("Roll the dice for your weapon (Press enter)")
weapon_roll = random.choice(small_dice_options)
hero.combat_strength = min(6, hero.combat_strength + weapon_roll)
print("    |    The hero's weapon is " + str(weapons[weapon_roll - 1]))
functions.adjust_combat_strength(hero.combat_strength, monster.combat_strength)

# Weapon Analysis
input("Analyze the Weapon roll (Press enter)")
if weapon_roll <= 2:
    print("--- You rolled a weak weapon, friend")
elif weapon_roll <= 4:
    print("--- Your weapon is meh")
else:
    print("--- Nice weapon, friend!")

if weapons[weapon_roll - 1] != "Fist":
    print("--- Thank goodness you didn't roll the Fist...")

# Health rolls
input("Roll the dice for your health points (Press enter)")
hero.health_points = random.choice(big_dice_options)
print("Hero health:", hero.health_points)

input("Roll the dice for the monster's health points (Press enter)")
monster.health_points = random.choice(big_dice_options)
print("Monster health:", monster.health_points)

# Collect Loot
print("!!You find a loot bag!! You look inside to find 2 items:")
input("Roll for first item (enter)")
loot_options, belt = functions.collect_loot(loot_options, belt)
input("Roll for second item (enter)")
loot_options, belt = functions.collect_loot(loot_options, belt)
belt.sort()
print("Your belt:", belt)

# Use Loot
belt, hero.health_points = functions.use_loot(belt, hero.health_points)

# Dream Levels (with try-except validation)
while True:
    try:
        num_dream_lvls = int(input("How many dream levels do you want to go down? (Enter a number 0-3): "))
        if 0 <= num_dream_lvls <= 3:
            break
        else:
            print("Number must be between 0 and 3.")
    except ValueError:
        print("Invalid input. Enter an integer between 0 and 3.")

if num_dream_lvls > 0:
    hero.health_points -= 1
    crazy_level = functions.inception_dream(num_dream_lvls)
    hero.combat_strength += crazy_level
    print("combat strength:", hero.combat_strength)
    print("health points:", hero.health_points)

# Monster power boost
input("Roll for Monster's Magic Power (Press enter)")
power = random.choice(list(monster_powers.keys()))
monster.combat_strength += monster_powers[power]
monster.combat_strength = min(6, monster.combat_strength)
print(f"Monster's combat strength is now {monster.combat_strength} using {power} power")

# FIGHT SEQUENCE
print("You meet the monster. FIGHT!!")
num_stars = 0
while monster.health_points > 0 and hero.health_points > 0:
    input("Roll to see who strikes first (Press enter)")
    attack_roll = random.choice(small_dice_options)
    if attack_roll % 2 != 0:
        input("You strike (Press enter)")
        hero.hero_attacks(monster)
        if monster.health_points == 0:
            num_stars = 3
            break
        input("Monster strikes (Press enter)")
        monster.monster_attacks(hero)
        if hero.health_points == 0:
            num_stars = 1
            break
        num_stars = 2
    else:
        input("Monster strikes (Press enter)")
        monster.monster_attacks(hero)
        if hero.health_points == 0:
            num_stars = 1
            break
        input("Hero strikes (Press enter)")
        hero.hero_attacks(monster)
        if monster.health_points == 0:
            num_stars = 3
            break
        num_stars = 2

# Get hero name
tries = 0
while tries < 5:
    hero_name = input("Enter your Hero's name (in two words): ")
    name_parts = hero_name.split()
    if len(name_parts) == 2 and all(part.isalpha() for part in name_parts):
        short_name = name_parts[0][:2] + name_parts[1][0]
        print(f"I'm going to call you {short_name} for short.")
        break
    else:
        print("Please enter a valid two-part name using only letters.")
        tries += 1

# Save game with monster kill tracking
def get_total_kills():
    try:
        with open("save.txt", "r") as f:
            lines = f.readlines()
            return sum(1 for line in lines if "has killed a monster" in line)
    except FileNotFoundError:
        return 0

total_kills = get_total_kills()
winner = "Hero" if monster.health_points <= 0 else "Monster"

if winner == "Hero":
    total_kills += 1

# Display results
print(f"Hero {short_name} gets {'*' * num_stars} stars")

with open("save.txt", "a") as f:
    if winner == "Hero":
        f.write(f"Hero {short_name} has killed a monster and gained {num_stars} stars.\n")
    else:
        f.write("Monster has killed the hero previously\n")
    f.write(f"Total monsters killed (across all games): {total_kills}\n")
