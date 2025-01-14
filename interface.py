from eclipseCpp import BattleBuilder
import re

def solveBattle (battle_info):

    battle_builder = BattleBuilder ()
    regex1 = re.search("(.*)(vs|VS|Vs|vS)(.*)" , battle_info)
    sides = [regex1[1], regex1[3]]

    ship_re = r"(\d+) +(int|cru|dre|sba|npc)"
    for i in range (14):
        ship_re += r" +(\d+)"

    ship_side = "ATT" # first list is attack
    for side in sides:
        ships = side.split('+')
        for ship in ships:
            print (ship)
            
            regex = re.search(ship_re, ship) #number type init hull comp shield weapons
            print (regex)
            
            canons   = [int(regex[ 7]), int(regex[ 8]), int(regex[ 9]), int(regex[10]), int(regex[11])]
            missiles = [int(regex[12]), int(regex[13]), int(regex[14]), int(regex[15]), int(regex[16])]

            battle_builder.addShip (ship_side, int(regex[1]), "INT", int(regex[3]), int(regex[4]), int(regex[5]), int(regex[6]), canons, missiles)

        ship_side = "DEF" #switch to def for the second list
    # call C++ lib to solve battle
    battle_builder.solveBattle (timeout=60)
    result = battle_builder.getResult ()

    # TODO? change frontend to take result directly
    dico = {
        "winChance": result["attacker_win_chance"],
        "attackShipsStillAlive" : result["attacker_ship_survival_chance"],
        "defenseShipsStillAlive": result["defender_ship_survival_chance"]
    }

    return dico
