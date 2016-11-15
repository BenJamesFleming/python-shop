# python-shop
A python program for call centers.
> Made For A School Project

# Requirments:

 - Python 3.5 Installed
 - Windows Computer

# How To Setup:

 - **Edit 'run.py'**
 
 - **How To Change Shop Type**
 
 **Note:** Use Advanced List As Default
 
 > Advanced List lets the user pick more than one type of item.
 
 > *Standard* List only lets the ser pick one item.
 
 ```
  is_list =  False
  is_advanced_list = True
 ```
 
 - **How To Add Items**
 ```
 items = [
    Item("Red", "Umbrella", 39.00, {'1':'4','2':'7','3':'7','4':'13'}),
    Item("Blue", "Umbrella", 39.00, {'1':'4','2':'7','3':'7','4':'13'}),
    Item("Light Green", "Umbrella", 39.00, {'1':'4','2':'7','3':'7','4':'13'}),
    Item("Orange", "Umbrella", 39.00, {'1':'4','2':'7','3':'7','4':'13'}),
    Item("Dark Gray", "Umbrella", 39.00, {'1':'4','2':'7','3':'7','4':'13'}),
    Item("Clear", "Umbrella", 39.00, {'1':'4','2':'7','3':'7','4':'13'}),
 ]
 ```
 
 - **How To Chage Max Items**
 ```
 maxItems = [10,10,10,10,10,10]
 ```
 **Warning:** Make sure that the indexs of the Max Items Array and the Item Array Match
 
 - **How To Chage The Client Feilds**
 
 *"{Client Attribute};{Attribute Type}:{Attribute Format}|{Client Attribute 2};{Attribute 2 Type}:{Attribute 2 Format}|..."*
 ```
 clientFeilds = "Full Name;string:>,0|Phone Number;number|Post Code;number:=,4"
 ```
 
 - **How To Chage The Client Feild Formats**
 
 *"[[{Attribute Visable Bool}, {Attribute Format}], [{Attribute 2 Visable Bool}, {Attribute 2 Format}],...]]"*
 ```
 [True, "~"]     # Show Item Normally
 [False, "~"]    # Hide Item, But Dont Format It
 [True, "~ __4"] # Show Item And Append Item 4 To The End
 ```
 ```
 clientFieldFormats = [[True, "~"], [True, "~"], [True, "~"], [True, "~ __4"], [False, "~"]]
 ```
 
# How To Use:

 - Double Click On 'start.bat'

**Warning:** Orders WILL Be Lost Once The Programme Has Been Quit!
