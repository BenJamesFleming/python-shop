# -*- coding: utf-8 -*-
# © Ben Fleming, 2016
# Hat Shop Program
# Imports
from _base import *

# Public Variables
use_colors = False      # bool; If the CLI can support colors
items = [
    Item("Hat", None, 29, {'1':'6','2':'7','3':'8','4':'9','5':'10'})   #
]                                                                       # arr; Array Of Items

# Start Item Shop
shop = Base(items, useColors=use_colors)
shop.run()
