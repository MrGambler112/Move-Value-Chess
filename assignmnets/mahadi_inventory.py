#Name: Mahadi Masuduzzaman
#Date: 05/27/2026
#Program Name: Gear Inventory Manager
#Description: This program manages an inventory of camping gear.
#             It loads items from a file or user input, then lets
#             the user display, add to, or subtract from each item.


#Loading gear into Inventory

def add_items() :

    #create empty list to hold all gear
    camping_inventory = []

    #ask user if they want to load from file or input manually
    load_choice = input ("Do you want to load from inventory.txt? (y/n): ")

    #loading information from inventory.txt
    if load_choice == "y" :
        print ("\nLoading inventory from inventory.txt...")
        load_from_file(camping_inventory)

    #inputting user information manually
    else :
        load_from_input(camping_inventory)

    return camping_inventory

#loading from input manually
def load_from_input(camping_inventory) :

    #prompt user to enter all item info on one line
    print ("\nEnter items below. Format: name code amount max_amount")
    print ("Press Enter with nothing typed to stop.\n")

    #prompt for the item in proper format
    item_line = input ("What is the item? ")

    #aslong as the user does not press enter, continue.
    while item_line != "" :

        #split the entered line into its 4 parts
        item_parts = item_line.split()

        #check that the user entered exactly 4 parts
        if len(item_parts) == 4 :

            #allocating information to proper variables
            item_name = item_parts[0]
            item_code = item_parts[1]
            amount_input = item_parts[2]
            max_amount_input = item_parts[3]

            #validate the item, if invalid, skip description prompt
            if validate_item(item_name, item_code, amount_input, max_amount_input) :

                #get description from user
                gear_description = input ("What is the description? ")

                #trim description to 100 characters if needed
                if len(gear_description) > 100 :
                    gear_description = gear_description[:100]

                #finally adding all item information to the inventory list
                camping_inventory.append([item_name, item_code, int(amount_input),
                                  int(max_amount_input), gear_description])

        #repeat if user does not provide proper formatted info
        else :
            print ("Error: Please enter all 4 fields on one line.")
            print ("Format: name code amount max_amount")

        item_line = input ("What is the item? ")

#loading from txt file
def load_from_file(camping_inventory) :

    #open inventory.txt in read mode
    inventory_file = open("inventory.txt", "r")
    item_line = inventory_file.readline().strip() #read the line and remove whitespace

    #aslong as the line is not empty, continue
    while item_line != "" :

        #read the description line regardless of validation result
        gear_description = inventory_file.readline().strip()

        #split the item line into its 4 parts
        item_parts = item_line.split()

        #check that the line has exactly 4 parts
        if len(item_parts) == 4 :

            #allocating information to proper variables
            item_name = item_parts[0]
            item_code = item_parts[1]
            amount_input = item_parts[2]
            max_amount_input = item_parts[3]

            #validate before adding to inventory
            if validate_item(item_name, item_code, amount_input, max_amount_input) :

                #trim description to 100 characters if needed
                if len(gear_description) > 100 :
                    gear_description = gear_description[:100]

                #adding all item information to the inventory list
                camping_inventory.append([item_name, item_code, int(amount_input),
                                          int(max_amount_input), gear_description])

        else :
            print ("Error: Invalid line in file, expected 4 fields.")

        item_line = inventory_file.readline().strip()

    inventory_file.close()

#validations for proper format
def validate_item(item_name, item_code, amount_input, max_amount_input) :

    is_valid = True

    #check if item name length is 15 characters or less
    if is_valid :
        if len(item_name) > 15 :
            print ("Error: Item name must be 15 characters or less.")
            is_valid = False

    #check if the item code is exactly 2 characters
    if is_valid :
        if len(item_code) != 2 :
            print ("Error: Item code must be exactly 2 characters.")
            is_valid = False

    #check that amount is a whole number
    if is_valid :
        if not is_whole_number(amount_input) :
             print ("Error: Amount must be a whole number.")
             is_valid = False

    #check amount is in range 0 to 999
    if is_valid :
        if not 0 <= int(amount_input) <= 999 :
            print ("Error: Amount must be between 0 and 999.")
            is_valid = False

    #check that max amount is a whole number
    if is_valid :
        if not is_whole_number(max_amount_input) :
            print ("Error: Max amount must be a whole number.")
            is_valid = False

    #check max amount is in range 1 to 999
    if is_valid :
        if not 1 <= int(max_amount_input) <= 999 :
            print ("Error: Max amount must be between 1 and 999.")
            is_valid = False

    #check amount does not exceed max amount
    if is_valid :
        if int(amount_input) > int(max_amount_input) :
            print ("Error: Amount cannot be greater than max amount.")
            is_valid = False

    return is_valid

#Whole number validator
def is_whole_number (input_number) :

    is_valid = True

    if not input_number.isdigit(): #validate it is whole
        is_valid = False

    return is_valid 
    


#Search item
#provided whole list and item code
def find_item(camping_inventory, item_code_input) : 

    #search inventory for a matching item code, return -1 if not found
    item_position = -1
    i = 0

    while i < len(camping_inventory) and item_position == -1 :
        if camping_inventory[i][1] == item_code_input :
            item_position = i #stop the loop
        i = i + 1 #stop the loop

    return item_position

#Managing the inventory
def manage_inventory(camping_inventory) :

    print ("\nManage Inventory")
    print ("Enter an item code to manage it, or x to quit.\n")

    #prompt user for item code to search
    item_code_input = input ("What is the item code? ")

    #aslong as user does not enter x, continue
    while item_code_input != "x" :

        #find the item in the inventory
        item_position = find_item(camping_inventory, item_code_input)

        if item_position == -1 :
            print ("Error: Item code not found.")

        #if found then provide user for the following actions
        else :

            print ("Input the designated letters for the following:\n", 
                   "d for description, a for adding to the amount,\n", 
                   "s for subtracting from the amount.")
            action_choice = input ("(d/a/s)? ")

            #display item info
            if action_choice == "d" :
                #new variable consisting of the item position
                gear_item = camping_inventory[item_position]
                print_item(gear_item)

            #add to item amount
            elif action_choice == "a" :

                change_amount_input = input ("How much would you like to add? ")

                #validate that it is a whole number
                if not change_amount_input.isdigit() :
                    print ("Error: Please enter a whole number.")

                #if it is a whole number continue with adding
                else :

                    change_amount = int(change_amount_input)
                    new_amount = camping_inventory[item_position][2] + change_amount

                    #check new amount does not exceed max amount
                    if new_amount > camping_inventory[item_position][3] :
                        print ("Cannot add: would exceed the maximum amount.")

                    else :
                        camping_inventory[item_position][2] = new_amount

            #subtract from item amount
            elif action_choice == "s" :

                change_amount_input = input ("How much would you like to subtract? ")

                #validate that it is a whole number
                if not change_amount_input.isdigit() :
                    print ("Error: Please enter a whole number.")

                #if it is a whole number continue with subtracting
                else :

                    change_amount = int(change_amount_input)
                    new_amount = camping_inventory[item_position][2] - change_amount

                    #check new amount does not go below zero
                    if new_amount < 0 :
                        print ("Cannot subtract: would go below zero.")

                    else :
                        camping_inventory[item_position][2] = new_amount

            else :
                print ("Error: Invalid action. Please enter d for the description, ")
                print ("a for adding to the amount, or s for subtracting from the amount.")

        item_code_input = input ("What is the item code? ")

#displaying information
def print_item(gear_item) : #gear_item is the item position in the inventory list

    #reinstate the item information into variables
    item_name = gear_item[0]
    item_code = gear_item[1]
    current_amount = gear_item[2]
    gear_description = gear_item[4]

    #build the left part of the display line
    display_left = "    " + item_name + " " + item_code + " " + str(current_amount)

    #description wraps at 30 characters in a column starting at position 50
    DESCR_START_COL = 50
    DESCR_WRAP_WIDTH = 30

    #split description into 30-character chunks, one character at a time
    #initailize variables for the loop
    descr_chunks = [] #chunks that contain 30 chars
    current_chunk = "" 
    char_count = 0
    char_index = 0

    #loop through each character in the description
    while char_index < len(gear_description) : 
        current_chunk = current_chunk + gear_description[char_index]
        char_count = char_count + 1
        char_index = char_index + 1

        #when chunk is full, save it and start a new one
        if char_count == DESCR_WRAP_WIDTH :
            descr_chunks.append(current_chunk)
            current_chunk = ""
            char_count = 0

    #save any leftover characters as the last chunk
    if current_chunk != "" :
        descr_chunks.append(current_chunk)

    if len(gear_description) == 0 :
        #no description, just print the left side
        print (display_left)

    else :
        #calculate how many spaces to add to reach column 50
        spaces_needed = DESCR_START_COL - len(display_left)
        
        #if the left side is already longer than 50, just add one space
        if spaces_needed < 1 :
            spaces_needed = 1
            
        padding = " " * spaces_needed

        #left part padded to column 50, then first description chunk
        print (display_left + padding + descr_chunks[0])

        #remaining description chunks each indented to column 50
        chunk_index = 1
        while chunk_index < len(descr_chunks) :
            print (" " * DESCR_START_COL + descr_chunks[chunk_index])
            chunk_index = chunk_index + 1

#main function to run the program
def main() :

    print ("The Inventory") #title
    print ("Manage your camping gear inventory\n") #description


#loading inventory

    print ("Loading Inventory")

    camping_inventory = add_items()

    print ("\nInventory loaded with", len(camping_inventory), "item(s).")

#managing inventory

    manage_inventory(camping_inventory)

    print ("\nGood Camping")


main()

input ()