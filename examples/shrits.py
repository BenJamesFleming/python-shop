# -*- coding: utf-8 -*-
# © Ben Fleming, 2016
# Cup Shop Program
# Imports
from _base import *

# Public Variables
use_colors = True       # bool; If The CLI Can Support Colors
is_list = True          # bool; If The Shop Is A List Or Not
deliveryCosts = {       #
    '1':'5',            #
    '2':'8',            #
    '3':'10'            #
}                       # dic; Dictonary Of Delivery Costs
cost = 27.5             # Item Cost
itemType = "Shirt"      # Type Of Item
startMsg = "Hello, This is Ranibow Shirts, You Are Talking To "+str(Input("Please Enter Your Name"))+"; Can I Take Your Order?" # Start Msg, Before The Order
clientFeilds = "Full Name;string|Phone Number;number"   # Client Feilds To Get
items = [
    Item("Red", itemType, cost, deliveryCosts),     #
    Item("Orange", itemType, cost, deliveryCosts),  #
    Item("Yellow", itemType, cost, deliveryCosts),  #
    Item("Green", itemType, cost, deliveryCosts),   #
    Item("Blue", itemType, cost, deliveryCosts),    #
    Item("Indigo", itemType, cost, deliveryCosts),  #
    Item("Violet", itemType, cost, deliveryCosts),  #
]                                                   # arr; Array Of Items

# Start Item Shop
# list=True; Only Allow One Type Of Item In Each Order
# startMsg=startMsg; Run Start Msg
# clientFeilds=clientFeilds; Set The Wanted Client Feilds
# useColors=use_colors; Set If CLI Has Color Support
shop = Base(items, list=is_list, startMsg=startMsg, clientFeilds=clientFeilds, useColors=use_colors)
shop.run()
