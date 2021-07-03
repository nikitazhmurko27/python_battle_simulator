"""Game class realization"""
import json
import time


class Game:
    """
    The class provide main properties and methods
    for game.
    """
    def __init__(self, armies):
        self.armies = armies
        self.log_data = {'data': []}

    def get_armies_health(self):
        """Get armies health (for logs)"""
        health_dict = {}
        for army in self.armies:
            army_health = army.get_army_health()
            health_dict[army.name] = army_health
        return health_dict

    def add_log(self, data):
        """Add log after army attack"""
        armies_health = self.get_armies_health()
        if len(data['attack_res']) == 0:
            self.log_data['data'].append({
                f"round_{data['round']}": {
                    "attacker": data['attacker'],
                    "attacker_success": "lost",
                    "attacker_damage": 0,
                    "armies_health": armies_health
                }
            })
            return
        for res in data['attack_res']:
            self.log_data['data'].append({
                f"round_{data['round']}": {
                    "attacker": data['attacker'],
                    "attacker_success": res['success'],
                    "attacker_damage": res['damage'],
                    "armies_health": armies_health
                }
            })

    def write_logs(self):
        """"Write logs to the file"""
        with open('logs.json', 'w') as logs_file:
            json.dump(self.log_data, logs_file)
            logs_file.close()

    def active_armies(self):
        """Check if one army is alive"""
        count = 0
        for army in self.armies:
            if not army.is_active():
                continue
            count += 1
        return count > 1

    def get_enemy_squads(self, attacker_index):
        """Get enemy squads list"""
        enemy_armies = []
        for army in self.armies:
            if not army.is_active():
                continue
            defender_index = self.armies.index(army)
            if attacker_index == defender_index:
                continue
            enemy_armies.append(army)

        enemy_squads_list = []
        for enemy_army in enemy_armies:
            army_squads = enemy_army.squads
            for army_squad in army_squads:
                if not army_squad.is_active():
                    continue
                enemy_squads_list.append(army_squad)
        return enemy_squads_list

    def start_game(self):
        """
        Start game until one army is alive
        """
        count = 1
        while self.active_armies():
            time.sleep(0.100)
            print(f'round = {count}')
            for army in self.armies:
                if not army.is_active():
                    continue
                army_index = self.armies.index(army)
                enemies = self.get_enemy_squads(army_index)
                attack_res = army.attack(enemies)
                log_data = {
                    "round": count,
                    "attacker": army.name,
                    "attack_res": attack_res
                }
                self.add_log(log_data)
            count += 1
        print("Game end")
        self.write_logs()
        for army in self.armies:
            if not army.is_active():
                print(f'{army.name} - lose')
                continue
            print(f'{army.name} - won')
