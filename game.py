
from map import places
from player import *
from items import *
from gameparser import *
from enemies import *
import random
import os
import time
import io
import sys

player_turns = 0 #Variables needed for it to work out if those rooms have been visited and to keep track of player turns.
Gut_room = False
Knight_room = False

class players: #Used for scoreboard
    score = ""
    name = ""

scores = []

def list_of_items(items): #Make a list of items into a string seperated by comma's
    string = ""
    for x in items:
        string = string + x["name"]
        if x != items[len(items) - 1]:
            string = string + ", "
    return string
    pass


def print_room_items(room): # print all the items in a room if there are any
    if list_of_items(room["items"]) != "":
        print("There is " + list_of_items(room["items"]) + " here.")
        print("")
    pass


def print_room(room): #print the name of the room and the description.
    
    print()
    print(room["name"].upper())
    print()
    
    if current_place != places["Knight"] or Knight_room == True: #Seperate descriptions for Knight/Gut room if they haven't
        if current_place != places["Gut"] or Gut_room == True:   #been visited yet.
            print(room["description"])
            print()
    if room == places["Leaderboard"]: #If leaderboard room then prints scoreboard
        print_score()
        print()
    print_room_items(room) #Print all items in the room.

    

def exit_leads_to(exits, direction): #return list of possible exits

    return places[exits[direction]]["name"]


def print_exit(direction, leads_to): #Prints exits

    print("GO " + direction.upper() + " to " + leads_to + ".")


def print_menu(exits, room_items): #Prints the menu
    
    global current_place #Makes globale variables assignable in the function
    if current_place == places["Lair"]: #If you are in the lair it fights Kraken automatically.
        kraken_fight()  
        current_place = places["Home"]
        print_menu(current_place["exits"], current_place["items"])
        return
    if current_place == places["Gut"] and Gut_room == False: #If you are in Gut room for first time it fights the stranger
        if Gutroom() == False:
            current_place = places["Home"]
            print_menu(current_place["exits"], current_place["items"])
            return
    if current_place == places["Knight"] and Knight_room == False:#If you are in Knight room for first time it fights the Knight.
        if Knight_Fight() == False:
            current_place = places["Home"]
            print_menu(current_place["exits"], current_place["items"])
            return
    print()
    print("You can:")
    print()

    for direction in exits: #prints exits
        print_exit(direction, exit_leads_to(exits, direction))
    if current_place["battle"] == True: #prints if you can battle or not
        print("Explore the local area.")
    if current_place == places["Gym"]: #prints if you can train
        print("Train strength, defence or speed for a cost of 25 gold per stat?")
    if current_place == places["Weapons"] or current_place == places["Armour"]: #prints items for buy and sale and their power
        for item in room_items:
            if item["type"] == "W":
                print("BUY " + item["id"] + " for " + str(item["value"]) + " with " + str(item["damage"]) + " damage.")
            else:
                print("BUY " + item["id"] + " for " + str(item["value"]) + " with " + str(item["defence"]) + " defence.")
        if weapon[0] != weapon_nothing:
            value = (weapon[0]["value"] * 0.6) % 1
            print("SELL " + weapon[0]["id"] + " with " + str(weapon[0]["damage"]) + " damage for " + str(int((weapon[0]["value"] * 0.6) - value)) + ".")
        if armour[0] != armour_nothing:
            value = (armour[0]["value"] * 0.6) % 1
            print("SELL " + armour[0]["id"] + " with " + str(armour[0]["defence"]) + " defence for " + str(int((armour[0]["value"] * 0.6) - value)) + ".")
    if current_place == places["Battle"]: #prints arena option
        print("Fight the next Arena opponent!")
    print()
    print("What do you want to do?")

def Knight_Fight(): #runs the Knight room fight if you haven't been there before.

    print("Following the winding burnt stone walls of the cave you come to ") 
    print("an opening with large bones scattered across the floor. The bones look") 
    print("human. Looking deeper into the opening there is a large dragon skeleton")
    print("in the centre of the cave. Upon closer inspection of the skeleton you") 
    print("find a fallen knight in full royal armour. The knight climbs to his feet") 
    print("and draws his sword.")
    print("")
    global Knight_room
    if fight_monster(enemy_knight) == True:
        print("You kill the knight that had somehow managed to slay the dragon.")
        stats["money"] = stats["money"] + enemy_knight["money"]
        Knight_room = True
        return True
    else:
        print("You wake up a bit disorientated in your own bed.")
        print("You have a message that reads 'I found you passed out and bleeding, I looked after you but took payment for this from your possesions.")
        stats["money"] = 0
        return False

def Gutroom(): #Runs the Gut room fight if you haven't been there before.
    global Gut_room
    if stats["speed"] > 45 and stats["defence"] > 45:
        print("You follow your gut feeling down the hall, feeling more and more on edge.")
        print("You hear a noise behind you and manage to turn in time to see an assailant.")
        print("You take one hit from him but after brushing it off you tackle him to the floor.")
        print("He runs off but not before dropping 50 gold pieces.")
        stats["money"] = stats["money"] + 50
        Gut_room = True
        return True
    else:
        print("Your gut feeling is starting to feel a little bit off.")
        print("As you walk deeper and deeper into the cave it gets even more dark.")
        print("You are now in complete darkness.")
        print("You should probably go back to to the main entrance but as soon as you turn")
        print("around a shadowed figure hits you across the head, knocking you unconscious.")
        print("")
        print("You wake up in your own bed hating yourself for being so stupid.")
        stats["money"] = 0
        return False

def kraken_fight(): #Runs the kraken fight with win condition if you end.
    if fight_monster(enemy_kraken) == True:
        print("                             _____   ___    ")
        print("\         / | |\   | |\   | |       |   \  |")
        print(" \   ^   /  | | \  | | \  | |___    |___/  |")
        print("  \ / \ /   | |  \ | |  \ | |       |   \  |")
        print("   V   V    | |   \| |   \| |_____  |    \ .")
        print("")
        print("")
        print("You managed to win the game in only " + str(player_turns) + " fights. Try and do it in less next time.")
        input("> ")
        os.system('cls' if os.name == 'nt' else 'clear')
        sys.exit()
    else:
        print("")
        print("You wake up a bit disorientated in your own bed with a vague memory of fighting the Kraken.")
        print("You find a note that reads 'Don't be so stupid in future, leave the leviathon alone'.")
        stats["money"] = 0
        current_place = places["Home"]




def is_valid_exit(exits, chosen_exit): #Checks if valid exit.
    
    return chosen_exit in exits


def execute_go(direction): #moves you between rooms.
    
    global current_place
    if is_valid_exit(current_place["exits"], direction) == True:
        current_place = move(current_place["exits"], direction)
    else:
        print("You cannot go there.")
    pass


def execute_take(item_id): #lets you buy and sell items in the shops if you have enough money and they don't weight too much
                           #and if you don't have a weapon/armour already equipped.
    for item in current_place["items"]:
        if item["id"] == item_id:
            if stats["money"] >= item["value"]:
                if item["type"] == "W":
                    if weapon[0] != weapon_nothing:
                        print("You need to sell your current weapon first.")
                        return
                    else:
                        weapon_update(item_id, item)
                        return
                else:
                    if armour[0] != armour_nothing:
                        print("You need to sell your current armour first.")
                        return
                    else:
                        armour_update(item_id, item)
                        return
            else:
                print("You don't have enough money for that.")
                return
    print("That isn't in the room.")
    pass

def weapon_update(item_id, item): #Equips new weapon and sorts out money.
    global weapon
    if (stats["mass"] + item["mass"]) <= (stats["strength"] / 5):                
        stats["mass"] =+ item["mass"]
        stats["money"] = stats["money"] - item["value"]
        weapon[0] = item
        current_place["items"].remove(item)
        print("You now have " + str(stats["money"]) + " money.")
        return
    else:
        print("The weight is too much, try dropping someting.")
        return


def armour_update(item_id, item): #Equips new armour and sorts out money.
    global armour
    if (stats["mass"] + item["mass"]) <= (stats["strength"] / 5):                
        stats["mass"] =+ item["mass"]
        stats["money"] = stats["money"] - item["value"]
        armour[0] = item
        current_place["items"].remove(item)
        print("You now have " + str(stats["money"]) + " money.")
        return
    else:
        print("The weight is too much, try dropping someting.")
        return

def execute_drop(item_id): #Allows you to sell your items back to the shops for 60% of the value.
    
    global weapon
    global armour
    if weapon[0]["id"] == item_id:
        stats["mass"] =- weapon[0]["mass"] 
        value = (weapon[0]["value"] * 0.6) % 1
        stats["money"] = stats["money"] + int((weapon[0]["value"] * 0.6) - value)
        current_place["items"].append(weapon[0])
        weapon[0] = weapon_nothing
        print("You now have " + str(stats["money"]) + " money.")
        return
    elif armour[0]["id"] == item_id:
        stats["mass"] =- armour[0]["mass"]  # removes the mass from you
        value = (armour[0]["value"] * 0.6) % 1 
        stats["money"] = stats["money"] + int((armour[0]["value"] * 0.6) - value) #works out your money back as a whole number.
        current_place["items"].append(armour[0]) #puts item in shop
        armour[0] = armour_nothing #gives you no item.
        print("You now have " + str(stats["money"]) + " money.")
        return
    else:
        print("You don't have that to drop it.")
    pass

def execute_explore(): #allows you to battle random enemies
    global current_place
    global player_turns
    print("explore " + current_place["name"])
    if random.randrange(1, 16, 1) < 15: #sometimes find items instead of enemies.
        enemy = enemy_calculator() #works out your enemy
        print("You encounter a random " + enemy["name"]) 
        result = fight_monster(enemy) # fights the enemy.
        print("")
        print("You had " + str(stats["money"]) + " gold.")
        player_turns = player_turns + 1 #adds one to turns taken.
        if result == True: #if you win it gives you some of enemies money.
            print("You slay the " + enemy["name"] + " and take some money you find near it.")
            stats["money"] = stats["money"] + random.randrange(1, enemy["money"], 1)
        else: #if you lose you lose your money and sends you home.
            print("You wake up a bit disorientated in your own bed.")
            print("You have a message that reads 'I found you passed out and bleeding, I looked after you but took payment for this from your possesions.")
            stats["money"] = 0
            current_place = places["Home"]
    else:
        item = items_list[random.randrange(1, 7, 1)] #Gives you random item
        print("You find a random " + item["name"] + ".")
        random_item(item)


    print("You now have " + str(stats["money"]) + " gold.")

def random_item(item): #works out if player wants to keep random item or not.
    global weapon
    global armour
    if item["type"] == "W":
        while True:
            print("The item has " + str(item["damage"]) + " damage and your item has " + str(weapon[0]["damage"]) + " do you want to swap? Y/N")
            answer = input("> ")
            if answer == "Y" or answer == "y":
                stats["mass"] = stats["mass"] - weapon[0]["mass"] + item["mass"]
                weapon[0] = item
                return
            elif answer == "N" or answer == "n":
                return
    else:
        while True:
            print("The item has " + str(item["defence"]) + " defence and your item has " + str(armour[0]["defence"]) + " do you want to swap? Y/N")
            answer = input("> ")
            if answer == "Y" or answer == "y":
                stats["mass"] = stats["mass"] - armour[0]["mass"] + item["mass"]
                armour[0] = item
                return
            elif answer == "N" or answer == "n":
                return


def enemy_calculator(): #calculates enemy depending on your room
    if current_place == places["Stream"]:
        enemy = enemy_list[random.randrange(1, 7, 1)]
    elif current_place == places["Forest"]:
        enemy = enemy_list[random.randrange(6, 15, 1)]
    elif current_place == places["Lake"]:
        enemy = enemy_list[random.randrange(6, 28, 1)]
    elif current_place == places["Caves"]:
        enemy = enemy_list[random.randrange(15, 28, 1)]
    elif current_place == places["Deeper"]:
        enemy = enemy_list[random.randrange(41, 50, 1)]
    elif current_place == places["Gut"]:
        enemy = enemy_list[random.randrange(28, 41, 1)]
    elif current_place == places["Knight"]:
        enemy = enemy_list[random.randrange(15, 41, 1)]
    elif current_place == places["Goblin"]:
        enemy = enemy_list[random.choice([15, 25, 28])]
    return enemy

def execute_train(stat): #Trains your stats for the cost of 25
    if stats["money"] >= 25:
        stats["money"] = stats["money"] - 25 
        stats[stat] = stats[stat] + 1
        print("You now have " + str(stats[stat]) + " " + stat + " and " + str(stats["money"]) + " money.")
    else:
        print("You don't have enough gold, get out of here.")

def execute_command(command): #works out which command to do
    
    global arena_level
    global player_turns
    if len(command) < 1:
        return
    elif command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "buy":
        if len(command) > 1:
            execute_take(command[1])
        else:
            print("buy what?")

    elif command[0] == "sell":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print("sell what?")
    elif command[0] == "explore" and current_place["battle"] == True: #Fights
        execute_explore()
    elif command[0] == "train" and current_place == places["Gym"]: #Trains stats
        if len(command) > 1:
            execute_train(command[1])
        else:
            print("Train what?")
    elif command[0] == "fight" and current_place == places["Battle"]: #Runs arena Fights
        if arena_level < 50:
            player_turns = player_turns + 1
            if fight_monster(enemy_list[arena_level]) == True:
                print("Congratulations you killed your next opponent.")
                arena_level = arena_level + 1
                stats["money"] = stats["money"] + 10
            else:
                print("They drag you out bleeding and patch you up. Thankfully you lost no money, just a whole lot of pride.")
        else:
            print("Noone wants to fight you, you are already the champion. Perhaps you should prove your worth by killing the Kraken?")
    else:
        print("That makes no sense, try another input.")

def fight_monster(enemy): #Function to fight the monsters
    e_health = enemy["health"]
    p_health = stats["health"]
    counter = 0
    p_counter = 0
    e_counter = 0
    while e_health > 0 and p_health > 0:
        enemy_speed = random.randrange(enemy["speed"], enemy["speed"] * 2, 1) #randomises a number based on persons speed, whoever has higher
        player_speed = random.randrange(stats["speed"], stats["speed"] * 2, 1)#speed gets the attack off.
        counter = counter + 1
        if enemy_speed > player_speed:
            e_counter = e_counter + 1
            damage = enemy["strength"] - stats["defence"] - armour[0]["defence"]
            if damage > 0:
                p_health = p_health - damage
                print(enemy["name"] + " hits you for " + str(damage) + " damage. You have " + str(p_health) + " health remaining.")
            else:
                print("The enemy hits you but you are too well protected and take no damage.")
        else:
            p_counter = p_counter + 1
            damage = (stats["strength"] - enemy["defence"] + weapon[0]["damage"])
            if damage > 0:
                e_health = e_health - damage
                print("You hit the enemy for " + str(damage) + " damage. The enemy has " + str(e_health) + " health remaining.")   
            else:
                print("You hit the enemy but he is too well protected and takes no damage.")
        if counter == 101:
            print("The fight takes it's toll on both of you and you just lie there bleeding out, but who will bleed out quicker?")
            if p_counter > e_counter:
                return(True)
            else:
                return(False)
    if e_health > 0:
        return(False)
    else:
        return(True)




def menu(exits, room_items): #the menu and clears the screen every time you do it again
    
    print_menu(exits, room_items)

    
    user_input = input("> ")

    
    normalised_user_input = normalise_input(user_input)

    os.system('cls' if os.name == 'nt' else 'clear')

    return normalised_user_input


def move(exits, direction):

    
    return places[exits[direction]] 

def print_game_menu(): #prints our main menu
    print()
    print()
    print()
    print('{:^80}'.format("Start Game - Press 1"))
    print()
    print('{:^80}'.format("Score Board - Press 2"))
    print()
    print('{:^80}'.format("How to play - Press 3"))
    print()
    print('{:^80}'.format("Exit - Press 4"))
    print()
    user_choice = input("Press a Number and hit ENTER . . . ")
    return user_choice

def print_score_board(): #prints scoreboard out
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print('{:^80}'.format("Here is the score board"))
    print()
    print_score()
    user_choice = input("Press key to return to menu . . . ")
    return

def print_rules(): #prints Rules out
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print('{:^80}'.format("Here are the rules"))
    print()
    print('{:^80}'.format("You are an adventurer in a world filled with adventurers."))
    print('{:^80}'.format("Your goal is to go down in history as the legend you are supposed to me."))
    print('{:^80}'.format("Use the on screen instructions to maneuvre your way around the world."))
    print('{:^80}'.format("Kill creatures to gain gold."))
    print('{:^80}'.format("Use to buy weapons and armour as well as to increase your stats."))
    print('{:^80}'.format("Try not to die and perhaps try fighting at the stream to start."))
    user_choice = input("Press key to return to menu . . . ")
    return

def exit_game(): #Exits from game
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print('{:^80}'.format("GOOD BYE"))
    print()
    time.sleep(1)
    return

def read_score(): #reads the score out of the file
    content = []
    with open("scores.txt", "r+") as f:
        content = f.readlines()
    for line in content:
        score = ""
        user = ""
        flag = False
        for ch in line:
            if ch == ':':
                flag = True
            else:
                if flag == True: 
                    user = user + ch
                else: 
                    score = score + ch
        current_player = players()
        current_player.score = score
        current_player.name = user
        scores.append(current_player)

def print_score(): #prints score out from the memory
    for pl in scores:
        print('{:^80}'.format(pl.score + "  -  " + pl.name))



def main():

    read_score() #reads score at start for later reference

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        option = print_game_menu()
        if option == "1":
            break;
        if option == "2": 
            print_score_board()
        if option == "3": 
            print_rules()
        if option == "4": 
            exit_game()
            return


    os.system('cls' if os.name == 'nt' else 'clear') #after doing the menu it clears screen and starts game

    
    while True:
        
        print_room(current_place)

        
        command = menu(current_place["exits"], current_place["items"])

        
        execute_command(command)




if __name__ == "__main__":
    main()

