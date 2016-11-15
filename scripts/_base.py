# -*- coding: utf-8 -*-
# © Ben Fleming, 2016
# Item Shop Program

# Imports
import os
import sys
import msvcrt
import collections
import copy
import json

# Item Class
# Used As A Container For All Items
# e.g.
#          Name   Type        Cost   Devlivery Cost Structure
# new Item("Red", "Umbrella", 39.00, {'1':'4','2':'7','3':'7','4':'13'})
class Item:
    name = ""		# str; Name
    itemType = ""	# str; Item Type
    fullName = ""	# str; Full Name
    cost = 0		# float; Cost
    count = 0		# int; Count
    devlivery = []	# arr; Devlivery
	
	# Item Loading Function
	# Load Item Info Into Item
    def __init__(self, itemName, itemType, itemCost, itemDelivery):
		
		# Set Variabes
        self.name = itemName
        self.itemType = itemType
        self.cost = itemCost
        self.delivery = itemDelivery
		
		# Full Name Variable Logic
        if itemType is not None:
            self.fullName = itemName+" "+itemType
        else:
            self.fullName = itemName
	
	# Item Count Setter Function
	# Sets self.count as Int
    def AddCount(self, count):
        self.count = count
        return self

# Client Class
# Used As A Container To Hold All Information For Each Clients Order
# Only Used As Internal Class
class Client:
    order_num = 0       # int; Order Number
    items = []          # arr; Items
    fields = []         # arr; Fields
    deliveryCost = 0    # int; Delivery Cost

    # Add Client Info Field To The Client
    # Variables;
    # self as obj;
    # field as arr; ["Full Name", "string"]
    def AddField(self, field):

        # Build Input Msg
        usr_input = Input("What Is Your "+field[0]+"?", format=field[1], formatError="Please Enter A Vaild "+field[0]+"!")

        # Add Field To Client
        self.fields.append([field[0], usr_input])
	
	# Clear Current Client Feilds From Client, To Start Again
    def ClearFields(self):
        del self.fields[:]
        self.fields = []

# Private Variables
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear') # fuc; Clear Command Line
clear_last = "\033[F"   # str; Remove Last Line

confirm = "n"           # str; Confirmed
confirmY = {"y", "yes"} # obj; Accepted Yes Answers
confirmN = {"n", "no"}  # obj; Accepted No Answers

use_colors = False              # bool; Use Color in The CLI
colors = {                      # obj; Object of Avliable Colors
    "default": "\033[0;30;47m", # str; Default Color
    "confirm": "\033[0;34;47m", # str; Confirm Color
    "error": "\033[0;31;47m",   # str; Error Color
    "bold": "\033[1;30;47m"     # str; Bold Default Text
}

defaultFormatLength = 20        # int; Format Length


##
## Helper Functions
##

# Get Color With Selector
# Variables
# selector as str; {"default", "confirm", "error", "bold"}
# useColors as bool;
# e.g. GetColor(selector, useColors=True)
def GetColor(selector, **kwargs):
    if kwargs.get("useColors", use_colors) == True:
        return colors[selector] if colors[selector] != None else colors["default"]
    else:
        return ""

# Get Client Fields With Selector
# Variables
# selector as str; {"all", "*", "none", "", "Full Name;string|Phone Number;number|Street Address;none|City;string|Post Code;number:4"}
# e.g. GetClientFields(selector)
def GetClientFields(selector):
    if selector == "all" or selector == "*":
        return [["Full Name", "string:>,0", True], ["Phone Number", "number", True], ["Street Address", "none:>,0",  True], ["City", "string:>,0", True], ["Post Code", "number:=,4", False]]
    elif selector == "none" or selector == "":
        return []
    else:
        fields = [field.split(";") for field in selector.split("|")]
        return fields

# Get Client Fields With Selector
# Variables
# shop as Base;
# selectorArr as arr; {None, [[True, "~ 1"], [False, "~"]...]}
# e.g. GetClientFieldFormats(shop, selectorArr)
def GetClientFieldFormats(shop, selectorArr):
    if type(selectorArr) is None:
        return [[True, "~"] for x in len(shop.ClientFields)]
    else:
        return selectorArr #[(val if type(val) is not None else [True, "~"]) for i, val in enumerate(selectorArr)]
        
# Get Item Count With Variables
# Variables;
# maxItems as int;
# item as obj;
# orderItems as list;
# selectedIndex as int;
def GetItemCount(maxItems, item, orderItems, selectedIndex):

    # Check That maxItems Is vaild
    if type(maxItems) is int:
        if maxItems == 0: return int(Input("How many "+item.fullName+"s would you like?", preMsg="\n", format="number", error="Please Enter A Vaild Number!!"))

    # Loop Until Vaild Input Is Given
    while True:
        if type(maxItems) is int:

            # Get Total Item For Client
            totalItemCount = sum([ x.count for x in orderItems])

            # Get User Input
            itemCount = int(Input("How many "+item.fullName+"s would you like? "+GetColor("error")+"\n>> Warning: Only "+str(maxItems-totalItemCount)+" Item Choices Left! "+GetColor("default"), preMsg="\n", format="number", error="Please Enter A Vaild Number!!"))

            totalItemCount += itemCount
            if totalItemCount <= maxItems:
                return itemCount
                break
            else:
                Print("Error: Max Item Count Per Client Is "+str(maxItems)+" You Have "+str(totalItemCount)+" Total Items!", color="error", format=False)

        elif type(maxItems) is list:

            # Get User Input
            itemCount = int(Input("How many "+item.fullName+"s would you like? "+GetColor("error")+"\n>> Warning: Only "+str(maxItems[selectedIndex])+" "+item.fullName+" Per Client! "+GetColor("default"), preMsg="\n", format="number", error="Please Enter A Vaild Number!!"))

            if itemCount <= maxItems[selectedIndex]:
                return itemCount
                break
            else:
                Print("Error: Max "+item.fullName+"s Per Client Is "+str(maxItems[selectedIndex])+" You Entered :"+str(itemCount)+"!", color="error", format=False)

# Format Given String To Look Good On CLI
# Variables
# string as str;
# e.g. FormatString(string)
def FormatString(string, **kwargs):

    string = string.lower().title()

    try:
        if string.index(':') < (len(string)-1):
            return string[:string.index(':')]+(" "*(kwargs.get("formatLength", defaultFormatLength) - len(string[:string.index(':')])))+string[string.index(':'):]
        else:
            return string
    except:
        return string

# Format Given String To Look Good On CLI
# Variables
# client as Client;
# formatArr as arr;
# value as str;
# e.g. FormatClientFields(client, formatArr, value)
def FormatClientFields(client, formatArr, value):
    if formatArr[0] == False:
        return ""
    else:
        string = formatArr[1]
        string = string.replace("~", value)
        
        for i, val in enumerate(client.fields):
            string = string.replace("__"+str(i), val[1])
            
        return str(string)

# Format Input With Variables
# Variables;
# num as float;
# e.g. FormatCost(num)
def FormatCost(num):
    return "{0:.2f}".format(num)

# Format Input With Variables
# Variables;
# itemCount as int;
# itemCost as float;
# item as obj;
# e.g. FormatCostPrint(itemCount, itemCost, item)
def FormatCostPrint(itemCount, itemCost, item):
    itemCost = int(itemCost)
    msg = itemCount+"  "+item.fullName+" : $"+FormatCost(itemCost)
    if int(itemCount) > 1:
        msg = itemCount+"  "+item.fullName+"s : $"+FormatCost(itemCost)
    if str(itemCount) == str(sorted(item.delivery.keys())[-1]):
        msg = itemCount+"+ "+item.fullName+"s : $"+FormatCost(itemCost)
    return msg

# Format Input With Variables
# Variables;
# msg as str;
# color as str; {"default", "confirm", "error"}
# preMsg as str;
# format as str; {"number", "string", "confirm"}
# formatError as str;
# e.g. Input(msg, color="", preMsg="", format="", formatError="")
def Input(msg, **kwargs):
    msg = GetColor(kwargs.get("color", "default"))+kwargs.get("preMsg", "")+">> "+str(FormatString(msg, formatLength=kwargs.get("formatLength", defaultFormatLength)))+("\n>>" if kwargs.get("expectInput", True) else "")+GetColor("default")
    failed = False
    error_msg = ""
    while True:
        usr_input = ""

        # If Format Failed Change Msg
        if failed == True:
            msg = GetColor("error")+kwargs.get("preMsg", "")+">> "+str("Error: "+error_msg)+"\n>> "+GetColor("default")

        # Get User Input
        try:
			# For Older Python Versions <2.7
            usr_input = raw_input(u"{0}".format(msg))
        except NameError:
			# For Newer Python Versions >3.0
            usr_input = input(u"{0}".format(msg)),
        except:
			# Fail If No Input Methods Work
            sys.exit("Unhandled Input Error!")
		
		# Change Variable Type Returned From Input | Raw_Input
		# For Consistence
        if isinstance(usr_input, tuple):
            usr_input = usr_input[0]
		
		# Assign Default Variable If No Input Variable Is Given
		# Or Input Is Skipped By User
        if len(usr_input) == 0:
            usr_input = ""

        # Check If Format Has Been Defined
		# If So, Check Formatting
        if kwargs.get("format", None) is not None:

            input_format = kwargs.get("format").split(":")
			
			# Foramts
            # Function To Check That The Input length Is Correct
            if len(input_format) >= 2:
                input_format[1] = input_format[1].split(",")
                if input_format[1][0] == "=":
                    if str(len(usr_input)) != str(input_format[1][1]):
                        error_msg = kwargs.get("formatError1", "Input Must Be "+str(input_format[1][1])+" Characters Long!")
                        failed = True
                        continue
                elif input_format[1][0] == ">":
                    if str(len(usr_input)) < str(input_format[1][1]):
                        error_msg = kwargs.get("formatError1", "Input Must Be More Than "+str(input_format[1][1])+" Characters Long!")
                        failed = True
                        continue
                elif input_format[1][0] == "<":
                    if str(len(usr_input)) > str(input_format[1][1]):
                        error_msg = kwargs.get("formatError1", "Input Must Be Less Than "+str(input_format[1][1])+" Characters Long!")
                        failed = True
                        continue
           
            # No Format
			# Return If Format Is Defined As "none"
            if input_format[0] == "none":
                return usr_input
                break
                
            # Number Only
			# Function To Check That The Input Only Contains Numbers
            if input_format[0] == "number":
                if all(char.isdigit() or char.isspace() for char in usr_input) == True:
                    return usr_input
                    break
                else:
                    error_msg = kwargs.get("formatError", "Input only Numbers!")
                    failed = True
                    continue

            # Letter Only
			# Function To Check That The Input Only Contains Letters
            if input_format[0] == "string":
                if all(char.isalpha() or char.isspace() for char in usr_input) == True:
                    return usr_input
                    break
                else:
                    failed = True
                    error_msg = kwargs.get("formatError", "Input only Letters!")
                    continue

            # Is A Valid Confirm
			# Function To Check That The Input Is A Valid Confim Variable
            if input_format[0] == "confirm":
                if usr_input.lower() in confirmY or usr_input.lower() in confirmN:
                    return usr_input.lower()
                    break
                else:
                    failed = True
                    error_msg = kwargs.get("formatError", "Enter A Vaild Confirm Statment! [confim] yes / no")
                    continue

        else:
            return usr_input
            break

# Format Print Message With Variables
# Variables;
# msg as str;
# color as str; {"default", "confirm", "error"}
# preMsg as str;
# foramt as bool:
# e.g. Print(msg, preMsg="", color="", format=False)
def Print(msg, **kwargs):
    # Build msg
    msg_out = GetColor(kwargs.get("color", "default"))+kwargs.get("preMsg", "")+">>"+(" " if kwargs.get("space", True) else "")+str(FormatString(msg))
    if kwargs.get("format", True) == False:
        msg_out = GetColor(kwargs.get("color", "default"))+kwargs.get("preMsg", "")+">>"+(" " if kwargs.get("space", True) else "")+str(msg)

    # Print msg
    try:
        print(u"{0}".format(msg_out))
        return True
    except:
        sys.exit("Unhandled Print Error!")


# Format Large Print Message With Variables
# Variables;
# msg as str;
# color as str; {"default", "confirm", "error"}
# e.g. PrintLarge(["", ""], color="")
def PrintLarge(msg, **kwargs):
    for m in msg:
        temp_msg = GetColor(kwargs.get("color", "default"))+">> "+str(FormatString(m, formatLength=kwargs.get("formatLength", defaultFormatLength)))
        # Print msg
        try:
            print(u"{0}".format(temp_msg))
        except:
            sys.exit("Unhandled Print Error!")

class Base():

    startMsg = ""           # str; Printed When The Order Starts
    clientFields = []       # arr; All Client Fields
    shop_type_list = False  # bool; Make The Shop A List
    shop_type_advanced_list = False # bool; Make The Shop An Advanced List
    selectedItem = None     # obj; The Selected Item, Only Used If Shop Type = List
    maxItems = 0            # int; The Max Number Of Items
    items = []              # arr; Items in The Shop
    
    debug = False            # bool; If The Program Is in Debug Mode Or Not

    order_num = 0           # int; Order Number
    orders = []             # arr; Array of Complete Orders

    def __init__(self, items, **kwargs):

        global use_colors
        use_colors = kwargs.get("useColors", False)

        self.items = items

        self.shop_type_list = kwargs.get("list", False)
        self.shop_type_advanced_list = kwargs.get("advancedList", False)
        self.startMsg = kwargs.get("startMsg", "")
        self.clientFields = GetClientFields(kwargs.get("clientFields", "*"))
        self.clientFieldFormats = GetClientFieldFormats(self, kwargs.get("clientFieldFormats", None))
        self.maxItems = kwargs.get("maxItems", 0)
        self.debug = kwargs.get("debugMode", False)
        
        if self.debug == True:
            self.clientFields = "none"

    def run(self):

        order_num = 0

        # Start Order Loop
        while True:

            # Set BG Color
            print(GetColor("default"))

            # Clear CLI
            clear()

            # Create Client
            client = Client()
            order_num += 1

            # Print Order Info
            Print("Order Started! #"+str(order_num)+" \n", preMsg="\n", format=False)

            # If Start Msg Is Vaild; Print It
            if self.startMsg != "":
                Print(self.startMsg+"\n", preMsg="\n", format=False)

            # Get User Variables
            # Variables;
            # itemCount as int;
            # deliveryCost as int;
            while True:

                # Create Order
                OrderItems = []
                deliveryCost = 0
                msg = None

                # Run Code Block If 'SHOP_TYPE' == List
                if self.shop_type_list:

                    # Set Up Variables For List Show
                    selectedIndex = 0
                    selected = False
                    formatLength = defaultFormatLength

                    # Get User Variables
                    # Variables;
                    # selectedIndex as int;
                    # selectedItem as Item;
                    while True:

                        # Run Code Block Only If 'selected' == false
                        if selected == False:

                            # Start To Build Msg
                            msg = ">> Order Started! #"+str(order_num)
                            # If Start Msg Is Vaild; Add It To Msg
                            if self.startMsg != "":
                                msg += "\n\n"+self.startMsg
                            msg += "\n\n>> Choose An Item To Order"

                            # Get Format Length
                            for item in self.items:
                                formatLength = max(formatLength, len(str("\n>> "+item.fullName+" : ")))

                            # For Loop To Build Msg
                            forIndex = 0
                            for item in self.items:

                                msg += FormatString("\n>> "+item.fullName+" : ", formatLength=formatLength)

                                # Check If Current Item == Selected Item
                                if forIndex == selectedIndex:
                                    msg += "[■]"
                                else:
                                    msg += "[ ]"

                                # Increase For Loop Index By 1
                                forIndex += 1

                            # Clear The CLI
                            clear()

                            # Print List
                            print(msg+"\n\r")

                            # Get User Input
                            while True:
                                key=msvcrt.getch()
                                if key == b'\r': # Enter Keys
                                    # Break List Loop
                                    selected = True
                                    break
                                elif key == b'\xe0': # Special Keys (arrows, f keys, ins, del, etc.)
                                    key = msvcrt.getch()
                                    if key == b'P': # Down Arrow
                                        # Change Selected Item
                                        selectedIndex = max(0, min(len(self.items)-1, selectedIndex+1))
                                        break
                                    elif key == b'H': # Up Arrow
                                        # Change Selected Item
                                        selectedIndex = max(0, min(len(self.items)-1, selectedIndex-1))
                                        break
                        else:
                            break

                    # Set Selected Item
                    self.selectedItem = self.items[selectedIndex]

                    # Print User Info
                    Print("Delivery Cost", preMsg="\n")
                    formatLength = len(str(sorted(self.selectedItem.delivery.keys())[-1])+"+ "+self.selectedItem.fullName+"s : ")
                    PrintLarge([FormatCostPrint(itemCount, itemCost, self.selectedItem) for itemCount, itemCost in collections.OrderedDict(sorted(self.selectedItem.delivery.items())).items()], formatLength=formatLength)

                    # Get User Input; itemCount as int;
                    itemCount = GetItemCount(self.maxItems, self.selectedItem, OrderItems, selectedIndex)

                    # If itemCount Is More Than 0 get deliveryCost
                    if itemCount > 0:
                        # Get Deliviery Cost For Current Item
                            # deliveryCost as int;
							# uses 'item.delivery'
							# uses 'itemCount'
							# uses 'delivieryCost' // As The Last Worked Out Cost
                        deliveryCost = max(int(self.selectedItem.delivery[str(min(itemCount, int(sorted(self.selectedItem.delivery.keys())[-1])))]), deliveryCost)

                    # Set Message To Array
                    msg = []

                    # Build Msg
                    msg.append(self.selectedItem.fullName+" Count    : "+str(itemCount)+" @ $"+FormatCost(self.selectedItem.cost)+" each")
                    msg.append(": $"+FormatCost((self.selectedItem.cost * itemCount)))
                    formatLength = max(formatLength, len(str(self.selectedItem.fullName+" Count    : ")))

                    # Add Item To Order
                    OrderItems.append(Item(self.selectedItem.name, self.selectedItem.itemType, self.selectedItem.cost, self.selectedItem.delivery).AddCount(itemCount))
                
				# Run Code Block If 'SHOP_TYPE' == Advanced List
                elif self.shop_type_advanced_list:
                    while True:
                        # Set Up Variables For List Show
                        selectedIndex = 0
                        selected = False
                        formatLength = defaultFormatLength

                        # Get User Variables
                        # Variables;
                        # selectedIndex as int;
                        # selectedItem as Item;
                        while True:

                            # Check If The Item Has Already Been Selected
                            if selected == False:

                                # Start To Build Msg
                                msg = ">> Order Started! #"+str(order_num)
                                # If Start Msg Is Vaild; Add It To Msg
                                if self.startMsg != "":
                                    msg += "\n\n"+self.startMsg
                                msg += "\n\n>> Choose An Item To Order"

                                # Get Format Length
                                for item in self.items:
                                    formatLength = max(formatLength, len(str("\n>> "+item.fullName+" : ")))

                                # For Loop To Build Msg
                                forIndex = 0
                                for item in self.items:

                                    msg += FormatString("\n>> "+item.fullName+" : ", formatLength=formatLength)

                                    # Check If Current Item == Selected Item
                                    if forIndex == selectedIndex:
                                        msg += "[■]"
                                    else:
                                        msg += "[ ]"

                                    # Increase For Loop Index By 1
                                    forIndex += 1

                                # Clear The CLI
                                clear()

                                # Print List
                                print(msg+"\n\r")

                                # Get User Input
                                while True:
                                    key=msvcrt.getch()
                                    if key == b'\r': # Enter Keys
                                        # Break List Loop
                                        selected = True
                                        break
                                    elif key == b'\xe0': # Special Keys (arrows, f keys, ins, del, etc.)
                                        key = msvcrt.getch()
                                        if key == b'P': # Down Arrow
                                            # Change Selected Item
                                            selectedIndex = max(0, min(len(self.items)-1, selectedIndex+1))
                                            break
                                        elif key == b'H': # Up Arrow
                                            # Change Selected Item
                                            selectedIndex = max(0, min(len(self.items)-1, selectedIndex-1))
                                            break
                            else:
                                break

                        # Set Selected Item
                        self.selectedItem = self.items[selectedIndex]

                        # Print User Info
                        Print("Delivery Cost", preMsg="\n")
                        formatLength = len(str(sorted(self.selectedItem.delivery.keys())[-1])+"+ "+self.selectedItem.fullName+"s : ")
                        PrintLarge([FormatCostPrint(itemCount, itemCost, self.selectedItem) for itemCount, itemCost in collections.OrderedDict(sorted(self.selectedItem.delivery.items())).items()], formatLength=formatLength)

                        # Get User Input; itemCount as int;
                        itemCount = GetItemCount(self.maxItems, self.selectedItem, OrderItems, selectedIndex)

                        # If itemCount Is More Than 0 get deliveryCost
                        if itemCount > 0:
                            # Get Deliviery Cost For Current Item
                            # deliveryCost as int;
							# uses 'item.delivery'
							# uses 'itemCount'
							# uses 'delivieryCost' // As The Last Worked Out Cost
                            deliveryCost = max(int(self.selectedItem.delivery[str(min(itemCount, int(sorted(self.selectedItem.delivery.keys())[-1])))]), deliveryCost)
                        else:
                            continue
                        
                        Print(str(itemCount)+" "+self.selectedItem.fullName+"s Added!", preMsg="\n")
                        confirm = Input("[confirm] y / n", color="confirm", format="confirm", formatError="Please Enter A Valid Yes/No Value!")

                        # If data is Confirmed, Add it to the order; else loop
                        if confirm in confirmY:
                            # Add Item To Order
                            OrderItems.append(Item(self.selectedItem.name, self.selectedItem.itemType, self.selectedItem.cost, self.selectedItem.delivery).AddCount(itemCount))
                        else:
                            continue
                            
                        clear()
                        confirm = Input("Finished Adding Items? \n>> [confirm] y / n", color="confirm", format="confirm", formatError="Please Enter A Valid Yes/No Value!")
                        
                        if confirm in confirmY:
                            break
                        
                else:
                
                    # Set Message To Array
                    msg = []
                    formatLength = defaultFormatLength

                    for index, item in enumerate(self.items):

                        # Print Each Items Details
                        Print(item.fullName+" Cost: $"+FormatCost(item.cost), preMsg="\n")
                        Print("Delivery Cost")
                        PrintLarge([FormatCostPrint(itemCount, itemCost, item) for itemCount, itemCost in collections.OrderedDict(sorted(item.delivery.items())).items()])

                        # Get User Input; itemCount as int;
                        itemCount = GetItemCount(self.maxItems, item, OrderItems, index)

                        # If itemCount Is More Than 0 get deliveryCost
                        if itemCount > 0:
							# Get Deliviery Cost For Current Item
                            # deliveryCost as int;
							# uses 'item.delivery'
							# uses 'itemCount'
							# uses 'delivieryCost' // As The Last Worked Out Cost
                            deliveryCost = max(int(item.delivery[str(min(itemCount, int(sorted(item.delivery.keys())[-1])))]), deliveryCost)

                        # Build Msg
                        msg.append(item.fullName+" Count    : "+str(itemCount)+" @ $"+FormatCost(item.cost)+" each")
                        formatLength = max(formatLength, len(str(item.fullName+" Count    : ")))

                        # Add Item To Order
                        OrderItems.append(Item(item.name, item.itemType, item.cost, item.delivery).AddCount(itemCount))
                
                # Clear CLI
                clear()
                
                # Confirm Data
                Print("Order Details:", preMsg="\n", format=False)
                
                # Set Message To Array
                msg = []
                
                # Build Msg
                for item in OrderItems:
                    msg.append(item.fullName+" Count    : "+str(item.count)+" @ $"+FormatCost(item.cost)+" each")
                    msg.append(": $"+FormatCost((item.cost * item.count)))
                    formatLength = max(formatLength, len(str(item.fullName+" Count    : ")))
                
                # Build Msg
                msg.append("Sub Total Cost: $"+FormatCost((sum([item.cost * item.count for item in OrderItems]))))
                msg.append("Total Delivery Cost: $"+FormatCost(deliveryCost))
                msg.append("Grand Total Cost : $"+FormatCost(float(sum([item.cost * item.count for item in OrderItems])+deliveryCost)))
                
                # Print Msg
                PrintLarge(msg, formatLength=formatLength)
                confirm = Input("[confirm] y / n", color="confirm", format="confirm", formatError="Please Enter A Valid Yes/No Value!")

                # If data is Confirmed, Add it to the order; else loop
                if confirm in confirmY:
                    client.items = OrderItems
                    client.order_num = order_num
                    client.deliveryCost = deliveryCost
                    OrderItems = []
                    break
                else:
                    OrderItems = []
            
            # Get User Vairables
            # Variables;
            # full_name as str;
            # phone_number as str;
            # street_address as str;
            # city as str;
            # postcode as str;
            while True:
                
                if self.clientFields != "none" and self.clientFields != "":
                
                    # Clear All Client Info Fields
                    client.ClearFields()

                    # Format The CLI
                    Print("\n", format=False)

                    # Get User Info
                    for felid in self.clientFields:
                        client.AddField(felid)

                    # Check If There Are Any Fields
                    if len(client.fields) > 0:

                        # Print Details Check
                        Print("Check Details:", preMsg="\n", format=False)
                        msg = []
                        for i, val in enumerate(client.fields):
                            if self.clientFieldFormats[i][0] == True:
                                msg.append(str(val[0])+" : "+FormatClientFields(client, self.clientFieldFormats[i], str(val[1])))
                        PrintLarge(msg)

                        # Confirm Data
                        confirm = Input("[confirm] y / n", color="confirm", format="confirm", formatError="Please Enter A Valid Yes/No Value!")

                        # if data is confirmed break; else loop
                        if confirm in confirmY:
                            Print("Order Complete!\n", preMsg="\n", format=False)
                            break

                    else:

                        # Finish Order and break
                        Print("Order Complete!\n", preMsg="\n", format=False)
                        break
                
                else:
                    break
            # Add current order to saved self.orders
            self.orders.append(copy.copy(client))

            # Check if user wants to place another order
            start_again = Input("Place Another Order? [confirm] y / n", color="confirm", format="confirm", formatError="Please Enter A Valid Yes/No Value!")

            # if no, break; else loop
            if start_again in confirmN:
                Print("Thanks For Ordering!\n", preMsg="\n", format=False)
                break

        # Clear CLI & Variables
        clear()
        totalItemsSold = 0
        formatLength = defaultFormatLength

        # Print Out Each Order
        Print("All Orders!")
        for order in self.orders:

            temp_items = order.items

            totalCost = float(sum([item.cost * item.count for item in temp_items])+order.deliveryCost)
            totalItemsSold += int(sum([item.count for item in temp_items]))

            # Build Order Msg
            msg = []
            for i, val in enumerate(client.fields):
                if self.clientFieldFormats[i][0] == True:
                    msg.append(str(val[0])+" : "+FormatClientFields(client, self.clientFieldFormats[i], str(val[1])))
            msg.append("Order")
            for item in temp_items:
                msg.append(item.fullName+"s Bought : "+str(item.count)+" @ $"+FormatCost(item.cost)+" Each")
                formatLength = max(formatLength, len(str(item.fullName+"s Bought : ")))

            msg.append("Sub Total         : $"+FormatCost(sum([item.cost * item.count for item in temp_items])))
            msg.append("Delivery Cost     : $"+FormatCost(order.deliveryCost))
            msg.append("Grand Total Cost  : $"+FormatCost(totalCost))

            # Print Order Msg
            Print("Order #"+str(order.order_num)+"!\n")
            PrintLarge(msg, formatLength=formatLength)
            Print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n", preMsg="\n", space=False)

        # Build Totals Msg
        msg = []
        formatLength = defaultFormatLength
        for item in self.items:
            msg.append("Total "+item.fullName+"s Sold: "+str(sum([sum([(temp_item.count if item.name == temp_item.name else 0) for temp_item in order.items]) for order in self.orders])))
            formatLength = max(formatLength, len(str("Total "+item.fullName+"s Sold : ")))
        msg.append("Total Items Sold: "+str(totalItemsSold))
        msg.append("Total Orders Made: "+str(len(self.orders)))

        # Print Out Totals
        Print("Totals!\n")
        PrintLarge(msg, formatLength=formatLength)

        Input("Press Enter To Continue", color="confirm", preMsg="\n", expectInput=False)
