# python-shop
A python program for call centers.

# Requirments:

 - Python 3.5 Installed
 - Windows Computer

# How To Setup:

 - **Edit 'run.py'**
 
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
 
 **Warning** Make sure that the indexs of the Max Items Array and the Item Array Match
 
 - **How To Chage The Client Feilds**
 
 *"{Client Attribute};{Attribute Type}:{Attribute Format}|{Client Attribute 2};{Attribute 2 Type}:{Attribute 2 Format}|..."*
 ```
 clientFeilds = "Full Name;string:>,0|Phone Number;number|Post Code;number:=,4"
 ```
 
# How To Use:

 - Double Click On 'start.bat'

**Warning** Orders WILL Be Lost Once The Programme Has Been Quit!
