# -*- coding: utf-8 -*-
# © Ben Fleming, 2016
# Cup Shop Program
# Imports
from _base import *

# Public Variables
# use_colors = False      # bool; If the CLI can support colors !! In Development !!
items = [
    Item("HIS", "Cup", 11, {'1':'3','2':'5','3':'7'}),      #
    Item("HER", "Cup", 11, {'1':'3','2':'5','3':'7'})       #
]                                                           # arr; Array Of Items

# Start Item Shop
shop = Base(items)
shop.run()
