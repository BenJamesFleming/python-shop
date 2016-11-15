# -*- coding: utf-8 -*-
# © Ben Fleming, 2016
# Umbrella Shop Program
# Imports
from _base import *

# Clear CLI
clear()

# Public Variables
use_colors = True
is_list = True
clientFeilds = "all"
startMsg = GetColor("confirm", useColors=use_colors)+">> Hello, This Is The Umbrella Shop; You Are Talking To "+Input("Please Enter Your Name")+"\n>> Note: Only 10 Items Per Client"+GetColor("default", useColors=use_colors)
maxItems = 10
items = [
	Item("Red", "Umbrella", 39.00, {'1':'4','2':'7','3':'7','4':'13'}),
	Item("Blue", "Umbrella", 39.00, {'1':'4','2':'7','3':'7','4':'13'}),
	Item("Light Green", "Umbrella", 39.00, {'1':'4','2':'7','3':'7','4':'13'}),
	Item("Orange", "Umbrella", 39.00, {'1':'4','2':'7','3':'7','4':'13'}),
	Item("Dark Gray", "Umbrella", 39.00, {'1':'4','2':'7','3':'7','4':'13'}),
	Item("Clear", "Umbrella", 39.00, {'1':'4','2':'7','3':'7','4':'13'}),
]
# Start Umbrella Shop
# clientFeilds=clientFeilds; Set The Wanted Client Feilds
shop = Base(items, list=is_list, clientFeilds=clientFeilds, useColors=use_colors, maxItems=maxItems, startMsg=startMsg)
shop.run()
