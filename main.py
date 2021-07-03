import json
from soldier import Soldier
from vehicle import Vehicle
from squad import Squad
from army import Army
from game import Game


with open("config.json") as config_file:
    config_object = json.load(config_file)
    config_file.close()


def create_armies(armies_list):
    armies_list_obj = []
    for army_obj in armies_list:
        army_name = army_obj["name"]
        army_squads_list = []
        army_squads = army_obj['squads']
        for army_squad in army_squads:
            strategy = army_squad['strategy']
            squad_units_list = []
            squad_units = army_squad['units']
            for squad_unit in squad_units:
                unit_type = squad_unit['unit']
                recharge = squad_unit['recharge']
                if unit_type == 'soldier':
                    squad_units_list.append(Soldier(recharge))
                    continue
                operators_count = squad_unit['operators']
                operators_list = []
                for operator in range(operators_count):
                    operators_list.append(Soldier(100))
                squad_units_list.append(Vehicle(operators_list, recharge))
            army_squads_list.append(Squad(squad_units_list, strategy))
        armies_list_obj.append(Army(army_name, army_squads_list))
    return armies_list_obj


armies = create_armies(config_object['armies'])
game = Game(armies)
game.start_game()
