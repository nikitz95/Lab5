#!/usr/bin/python3

from map import places
from player import *
from items import *
from gameparser import *



def list_of_items(items):
    """This function takes a list of items (see items.py for the definition) and
    returns a comma-separated list of item names (as a string). For example:

    >>> list_of_items([item_pen, item_handbook])
    'a pen, a student handbook'

    >>> list_of_items([item_id])
    'id card'

    >>> list_of_items([])
    ''

    >>> list_of_items([item_money, item_handbook, item_laptop])
    'money, a student handbook, laptop'

    """
    string = ""
    for x in items:
        string = string + x["name"]
        if x != items[len(items) - 1]:
            string = string + ", "
    return string
    pass


def print_room_items(room):
    """This function takes a room as an input and nicely displays a list of items
    found in this room (followed by a blank line). If there are no items in
    the room, nothing is printed. See map.py for the definition of a room, and
    items.py for the definition of an item. This function uses list_of_items()
    to produce a comma-separated list of item names. For example:

    >>> print_room_items(places["Reception"])
    There is a pack of biscuits, a student handbook here.
    <BLANKLINE>

    >>> print_room_items(places["Office"])
    There is a pen here.
    <BLANKLINE>

    >>> print_room_items(places["Robs"])

    (no output)

    Note: <BLANKLINE> here means that doctest should expect a blank line.

    """
    if list_of_items(room["items"]) != "":
        print("There is " + list_of_items(room["items"]) + " here.")
        print("")
    pass


def print_inventory_items(items):
    """This function takes a list of inventory items and displays it nicely, in a
    manner similar to print_room_items(). The only difference is in formatting:
    print "You have ..." instead of "There is ... here.". For example:

    >>> print_inventory_items(inventory)
    You have id card, laptop, money.
    <BLANKLINE>

    """
    if len(items) > 0:
        print("You have " + list_of_items(items) + ".")
        print("")
    pass


def print_room(room):
    """This function takes a room as an input and nicely displays its name
    and description. The room argument is a dictionary with entries "name",
    "description" etc. (see map.py for the definition). The name of the room
    is printed in all capitals and framed by blank lines. Then follows the
    description of the room and a blank line again. If there are any items
    in the room, the list of items is printed next followed by a blank line
    (use print_room_items() for this). For example:

    >>> print_room(places["Office"])
    <BLANKLINE>
    THE GENERAL OFFICE
    <BLANKLINE>
    You are standing next to the cashier's till at
    30-36 Newport Road. The cashier looks at you with hope
    in their eyes. If you go west you can return to the
    Queen's Buildings.
    <BLANKLINE>
    There is a pen here.
    <BLANKLINE>

    >>> print_room(places["Reception"])
    <BLANKLINE>
    RECEPTION
    <BLANKLINE>
    You are in a maze of twisty little passages, all alike.
    Next to you is the School of Computer Science and
    Informatics reception. The receptionist, Matt Strangis,
    seems to be playing an old school text-based adventure
    game on his computer. There are corridors leading to the
    south and east. The exit is to the west.
    <BLANKLINE>
    There is a pack of biscuits, a student handbook here.
    <BLANKLINE>

    >>> print_room(places["Robs"])
    <BLANKLINE>
    ROBS' ROOM
    <BLANKLINE>
    You are leaning agains the door of the systems managers'
    room. Inside you notice Rob Evans and Rob Davies. They
    ignore you. To the north is the reception.
    <BLANKLINE>

    Note: <BLANKLINE> here means that doctest should expect a blank line.
    """
    # Display room name
    print()
    print(room["name"].upper())
    print()
    # Display room description
    print(room["description"])
    print()
    print_room_items(room)

    #
    # COMPLETE ME!
    #

def exit_leads_to(exits, direction):
    """This function takes a dictionary of exits and a direction (a particular
    exit taken from this dictionary). It returns the name of the room into which
    this exit leads. For example:

    >>> exit_leads_to(places["Reception"]["exits"], "south")
    "Robs' room"
    >>> exit_leads_to(places["Reception"]["exits"], "east")
    "your personal tutor's office"
    >>> exit_leads_to(places["Tutor"]["exits"], "west")
    'Reception'
    """
    return places[exits[direction]]["name"]


def print_exit(direction, leads_to):
    """This function prints a line of a menu of exits. It takes a direction (the
    name of an exit) and the name of the room into which it leads (leads_to),
    and should print a menu line in the following format:

    GO <EXIT NAME UPPERCASE> to <where it leads>.

    For example:
    >>> print_exit("east", "you personal tutor's office")
    GO EAST to you personal tutor's office.
    >>> print_exit("south", "Robs' room")
    GO SOUTH to Robs' room.
    """
    print("GO " + direction.upper() + " to " + leads_to + ".")


def print_menu(exits, room_items, inv_items):
    """This function displays the menu of available actions to the player. The
    argument exits is a dictionary of exits as exemplified in map.py. The
    arguments room_items and inv_items are the items lying around in the room
    and carried by the player respectively. The menu should, for each exit,
    call the function print_exit() to print the information about each exit in
    the appropriate format. The room into which an exit leads is obtained
    using the function exit_leads_to(). Then, it should print a list of commands
    related to items: for each item in the room print

    "TAKE <ITEM ID> to take <item name>."

    and for each item in the inventory print

    "DROP <ITEM ID> to drop <item name>."

    For example, the menu of actions available at the Reception may look like this:

    You can:
    GO EAST to your personal tutor's office.
    GO WEST to the parking lot.
    GO SOUTH to Robs' room.
    TAKE BISCUITS to take a pack of biscuits.
    TAKE HANDBOOK to take a student handbook.
    DROP ID to drop your id card.
    DROP LAPTOP to drop your laptop.
    DROP MONEY to drop your money.
    What do you want to do?

    """
    print()
    print("You can:")
    print()
    for direction in exits:
        print_exit(direction, exit_leads_to(exits, direction))
    for item in room_items:
        print("TAKE " + item["id"] + " to take " + item["name"] + ".")
    for item in inv_items:
        print("DROP " + item["id"] + " to drop " + item["name"] + ".")
    if current_place["battle"] == True:
        print("Explore the local area.")
    if current_place == places["Gym"]:
        print("Train strength, defence or speed.")
    print()
    print("What do you want to do?")


def is_valid_exit(exits, chosen_exit):
    """This function checks, given a dictionary "exits" (see map.py) and
    a players's choice "chosen_exit" whether the player has chosen a valid exit.
    It returns True if the exit is valid, and False otherwise. Assume that
    the name of the exit has been normalised by the function normalise_input().
    For example:

    >>> is_valid_exit(places["Reception"]["exits"], "south")
    True
    >>> is_valid_exit(places["Reception"]["exits"], "up")
    False
    >>> is_valid_exit(places["Parking"]["exits"], "west")
    False
    >>> is_valid_exit(places["Parking"]["exits"], "east")
    True
    """
    return chosen_exit in exits


def execute_go(direction):
    """This function, given the direction (e.g. "south") updates the current room
    to reflect the movement of the player if the direction is a valid exit
    (and prints the name of the room into which the player is
    moving). Otherwise, it prints "You cannot go there."

    """
    global current_place
    if is_valid_exit(current_place["exits"], direction) == True:
        current_place = move(current_place["exits"], direction)
    else:
        print("You cannot go there.")
    pass


def execute_take(item_id):
    """This function takes an item_id as an argument and moves this item from the
    list of items in the current room to the player's inventory. However, if
    there is no such item in the room, this function prints
    "You cannot take that."
    """
    for item in current_place["items"]:
        if item["id"] == item_id:
            print(stats["mass"])
            if (stats["mass"] + item["mass"]) <= (stats["strength"] / 5):
                stats["mass"] =+ item["mass"]
                inventory.append(item)
                current_place["items"].remove(item)
                return
            else:
                print("The weight is too much, try dropping someting.")
                return
    print("That isn't in the room.")
    pass
    

def execute_drop(item_id):
    """This function takes an item_id as an argument and moves this item from the
    player's inventory to list of items in the current room. However, if there is
    no such item in the inventory, this function prints "You cannot drop that."
    """
    for item in inventory:
        if item["id"] == item_id:
            stats["mass"] =- item["mass"] 
            current_place["items"].append(item)
            inventory.remove(item)
            return
    print("You don't have that to drop it.")
    pass

def execute_explore():
    #Random encounters for either battling or finding items.
    print("explore " + current_place["name"])
    
def execute_train(stat):
    print("train " + stat)
    #Train a stat at the gym, GET DENCH!

def execute_command(command):
    """This function takes a command (a list of words as returned by
    normalise_input) and, depending on the type of action (the first word of
    the command: "go", "take", or "drop"), executes either execute_go,
    execute_take, or execute_drop, supplying the second word as the argument.

    """
    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            execute_take(command[1])
        else:
            print("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print("Drop what?")
    elif command[0] == "explore":
        execute_explore()
    elif command[0] == "train":
        if len(command) > 1:
            execute_train(command[1])
        else:
            print("Train what?")
    else:
        print("This makes no sense.")


def menu(exits, room_items, inv_items):
    """This function, given a dictionary of possible exits from a room, and a list
    of items found in the room and carried by the player, prints the menu of
    actions using print_menu() function. It then prompts the player to type an
    action. The players's input is normalised using the normalise_input()
    function before being returned.

    """

    # Display menu
    print_menu(exits, room_items, inv_items)

    # Read player's input
    user_input = input("> ")

    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


def move(exits, direction):
    """This function returns the room into which the player will move if, from a
    dictionary "exits" of avaiable exits, they choose to move towards the exit
    with the name given by "direction". For example:

    >>> move(places["Reception"]["exits"], "south") == places["Robs"]
    True
    >>> move(places["Reception"]["exits"], "east") == places["Tutor"]
    True
    >>> move(places["Reception"]["exits"], "west") == places["Office"]
    False
    """

    # Next room to go to
    return places[exits[direction]]


# This is the entry point of our program
def main():

    # Main game loop
    while True:
        # Display game status (room description, inventory etc.)
        print_room(current_place)
        print_inventory_items(inventory)

        # Show the menu with possible actions and ask the player
        command = menu(current_place["exits"], current_place["items"], inventory)

        # Execute the player's command
        execute_command(command)
        print()
        print("--------------------------------------------------")



# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()

