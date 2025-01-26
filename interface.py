from eclipseCpp_interface import *
import re

def solveBattle (battle_info):
    regex1 = re.search("(.*)(vs|VS|Vs|vS)(.*)" , battle_info)
    sides = [regex1[1], regex1[3]]

    ship_re = r"(\d+) +(int|cru|dre|sba|npc)"
    for i in range (14):
        ship_re += r" +(\d+)"

    # type conversion (because of legacy nomenclature)
    type_dico = {
        "int": "INT",
        "cru": "CRU",
        "dre": "DRE",
        "sba": "SBA",
        "npc": "INT"
    }

    attacker_ships = []
    defender_ships = []
    player_ships = [attacker_ships, defender_ships]
    attacker_modifiers = BattleModifier(False, False)
    defender_modifiers = BattleModifier(False, False)
    player_modifiers = [attacker_modifiers, defender_modifiers]

    for i in range (2):
        side = sides[i]
        ships = side.split('+')
        for ship in ships:
            regex = re.search(ship_re, ship) #number type init hull comp shield weapons

            if regex[2]=="npc":
                player_modifiers[i]._is_npc= True
            
            canons   = [int(regex[ 7]), int(regex[ 8]), int(regex[ 9]), int(regex[10]), int(regex[11])]
            missiles = [int(regex[12]), int(regex[13]), int(regex[14]), int(regex[15]), int(regex[16])]

            player_ships[i].append (Ship (int(regex[1]), type_dico[regex[2]], int(regex[3]), int(regex[4]), int(regex[5]), int(regex[6]), canons, missiles))

        
    # call C++ lib to solve battle
    battle = Battle (attacker_ships, attacker_modifiers, defender_ships, defender_modifiers)
    status = battle.solveBattle (timeout=60)
    result = battle.getResult ()

    dico = {
        "status": status,
        "winChance": float(result["attacker_win_chance"]),
        "attackShipsStillAlive" : [[float(i) for i in chance] for chance in result["attacker_ship_survival_chance"]],
        "defenseShipsStillAlive": [[float(i) for i in chance] for chance in result["defender_ship_survival_chance"]]
    }

    return dico
