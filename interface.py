from eclipseCpp_interface import *
import re

def solveBattle (battle_info):
    regex1 = re.search("(.*)(vs|VS|Vs|vS)(.*)" , battle_info)
    sides = [regex1[1], regex1[3]]

    ship_re = r"(\d+) +(int|cru|dre|sba|npc)"
    for i in range (14):
        ship_re += r" +(\d+)"

    # type conversion (because of legacy nomenclarure)
    type_dico = {
        "int": "INT",
        "cru": "CRU",
        "dre": "DRE",
        "sba": "SBA",
        "npc": "INT"
    }

    attacker_ships = []
    defender_ships = []
    player_ships = attacker_ships
    for side in sides:
        ships = side.split('+')
        for ship in ships:
            #TODO npc
            
            regex = re.search(ship_re, ship) #number type init hull comp shield weapons
            
            canons   = [int(regex[ 7]), int(regex[ 8]), int(regex[ 9]), int(regex[10]), int(regex[11])]
            missiles = [int(regex[12]), int(regex[13]), int(regex[14]), int(regex[15]), int(regex[16])]

            player_ships.append (Ship (int(regex[1]), type_dico[regex[2]], int(regex[3]), int(regex[4]), int(regex[5]), int(regex[6]), canons, missiles))

        player_ships = defender_ships #switch to def for the second list
    # call C++ lib to solve battle
    battle = Battle (attacker_ships, BattleModifier(), defender_ships, BattleModifier())
    print(battle.solveBattle (timeout=60))
    result = battle.getResult ()

    # TODO? change frontend to take result directly
    dico = {
        "winChance": float(result["attacker_win_chance"]),
        "attackShipsStillAlive" : [[float(i) for i in chance] for chance in result["attacker_ship_survival_chance"]],
        "defenseShipsStillAlive": [[float(i) for i in chance] for chance in result["defender_ship_survival_chance"]]
    }

    return dico
