from eclipse import *
import re

def solveBattle (battle_info):
    regex1 = re.search("(.*)(vs|VS|Vs|vS)(.*)" , battle_info)
    sides = [regex1[1], regex1[3]]

    ship_re = r"(\d+) +(int|cru|dre|sba|npc)"
    for i in range (14):
        ship_re += r" +(\d+)"

    ship_list_list = []
    ship_counter = 1
    for side in sides:
        ships = side.split('+')
        ship_list = []
        for ship in ships:
            
            regex = re.search(ship_re, ship) #number type init hull comp shield weapons
            
            canons = [int(regex[ 7]), int(regex[ 8]), int(regex[ 9]), int(regex[10]), int(regex[11])]
            missis = [int(regex[12]), int(regex[13]), int(regex[14]), int(regex[15]), int(regex[16])]

            ship = Ship(regex[2], int(regex[1]), int(regex[3]), int(regex[4]), int(regex[5]), int(regex[6]), canons, missis)
            ship_list.append(ship)
        ship_list_list.append(ship_list)
        ship_counter += 1

    att_ships = ship_list_list[0]
    def_ships = ship_list_list[1]

    addCanonsIfNoCannons (att_ships, def_ships)

    response = "**Attacker:\n**"
    for ship in att_ships:
        response += ship.toString() + "\n"
    response+= "**Defender:\n**"
    for ship in def_ships:
        response += ship.toString() + "\n"

    battle = BattleWinChances (att_ships, def_ships, remaining_ships=True)

    dico = {
        "winChance": battle.initial_win_chance,
        "attackShipsStillAlive" : battle.att_still_alive,
        "defenseShipsStillAlive": battle.def_still_alive
    }

    return dico

def addCanonsIfNoCannons (att_ships, def_ships):
    """ this function adds a pseudo canon to defense ships if neither attacker nor defender has canons"""
    nb_canons = 0
    for ship in att_ships + def_ships:
        for i in range (5):
            nb_canons+=ship.canon_array[i]
    if nb_canons == 0:
        for ship in def_ships:
            ship.canon_array[0]+=1
        

