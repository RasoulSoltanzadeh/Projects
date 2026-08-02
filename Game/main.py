# In The Name Of God
# Studernt Name: Rasoul Soltanzadeh
# Student ID: 40413160281816
# Teacher Name: Dr. Afrabandpay
# University: University Of Mazandaran 
# Field Of Study: Computer Engineerung 
# Term: 2
# Course: Advanced Programing
# Project Name: Miniproject_40413160281816
# Project Type: Practical Task
# Task count: 4
# Starting Date: 1405/3/20/12:00 - 2026/6/10/12:00
# Modify Date: 1405/3/22/11:40 - 2026/6/12/11:40
# Enviroment: Visual Studio 2026
# Language Version: Python 3.11 (64-bit) 
# Subject: Game

from game import Person, bcolors
from magic import Spell
from inventory import Item
from random import randint

# Create Magic
fire = Spell("Fire", 25, 600)
thunder = Spell("Thunder", 25, 600)
blizzard = Spell("Blizzard", 25, 600)
meteor = Spell("Meteor", 40, 1200)

# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of player", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor]
player_items = [{"item": potion, "quantity": 15}, {"item": elixer, "quantity": 5}, {"item": grenade, "quantity": 5}]

# Instantiate People
player1 = Person("Homayun", 3260, 132, 300, player_spells, player_items)
player2 = Person("Amin", 3260, 132, 300, player_spells, player_items)
player3 = Person("Rasoul", 3089, 174, 300, player_spells, player_items)
players = [player1, player2, player3]

enemy1 = Person("Enemy_1", 11200, 701, 525, [], [])
enemy2 = Person("Enemy_2", 1250, 701, 525, [], [])
enemy3 = Person("Enemy_3", 1250, 701, 525, [], [])
enemies = [enemy1, enemy2, enemy3]

def select_target(enemies : list, player : Person) -> Person: 
    target = player.choose_target(enemies)
    assert target >= 0 and target < len(enemies), "Invalid target! Choose a correct value for target (from 1 to " + str(len(enemies)) + ")."
    return enemies[target]

running = True
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("=============================")
    print("\n\n")
    print("NAME                     HP                                      MP")

    for player in players: player.get_stats()  

    print("\n")

    for enemy in enemies: enemy.get_enemy_stats()
    
    for i in range(len(players)):
        player = players[i]
        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1
        
        if index > 2 or index < 0:  raise ValueError("Invalid action! Choose a correct value for action (from 1 to 3).")
        
        if index == 0:
            enemy = select_target(enemies, player)
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            print(player.name ,"attacked for", dmg, "points of damage.")

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) - 1

            if magic_choice > 3 or magic_choice < 0:  raise ValueError("Invalid magic! Choose a correct value for magic (from 1 to 4).")
        
            enemy = select_target(enemies, player)
            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)
            enemy.take_damage(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage" + bcolors.ENDC)
    
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice > 2 or item_choice < 0:  raise ValueError("Invalid item! Choose a correct value for item (from 1 to 3).")
        
            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1
        
            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
        
            elif item.type == "elixer":
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            
            elif item.type == "attack":
                enemy = select_target(enemies, player)
                enemy.take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage" + bcolors.ENDC)
    
    enemies = [enemy for enemy in enemies if enemy.get_hp() != 0]    
    if enemies.__len__() == 1:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        break;

    for enemy in enemies:
        enemy_dmg = enemy.generate_damage()
        player = players[randint(0, len(players) - 1)]
        player.take_damage(enemy_dmg)
        print(f"{enemy.name} attacks {player.name} for {enemy_dmg}")
    
    players = [player for player in players if player.get_hp() != 0]
    if players.__len__() == 1:
        print(bcolors.FAIL + "Your enemy has defeated your team!" + bcolors.ENDC)
        break;

    