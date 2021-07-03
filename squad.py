"""Squad class realization"""
import time
from statistics import geometric_mean
from unit import custom_rand


def get_strongest_squad(squads):
    """Get the strongest squad from the list"""
    max_health = 0
    strongest_squad = ''
    for squad in squads:
        squad_health = squad.squad_health()
        if max_health == 0:
            max_health = squad_health
            strongest_squad = squad
            continue
        if squad_health <= max_health:
            continue
        max_health = squad_health
        strongest_squad = squad
    return strongest_squad


def get_weakest_squad(squads):
    """Get the weakest squad from the list"""
    min_health = 0
    weakest_squad = []
    for squad in squads:
        squad_health = squad.squad_health()
        if min_health == 0:
            min_health = squad_health
            weakest_squad = squad
            continue
        if squad_health >= min_health:
            continue
        min_health = squad_health
        weakest_squad = squad
    return weakest_squad


def get_random_squad(squads):
    """Get random squad from the list"""
    return custom_rand.choice(squads)


SQUAD_STRATEGIES = {
                    "strongest": get_strongest_squad,
                    "weakest": get_weakest_squad,
                    "random": get_random_squad,
                    }


class Squad:
    """
    The class provide main properties and methods
    for squad.
    """
    def __init__(self, units, strategy='random'):
        self.units = units
        self.strategy = strategy

    def is_active(self):
        """Check if squad is alive"""
        for unit in self.units:
            if unit.is_alive():
                return True
        return False

    def squad_health(self):
        """Get squad health"""
        health = 0
        alive_units = self.get_alive_units()
        for alive_unit in alive_units:
            health += alive_unit.health
        return health

    def get_alive_units(self):
        """Get list of alive units"""
        alive_units = []
        for unit in self.units:
            if not unit.is_alive():
                continue
            alive_units.append(unit)
        return alive_units

    def get_active_units(self):
        """Get list of alive and active (ready to attack) units"""
        alive_units = self.get_alive_units()
        active_units = []
        for alive_unit in alive_units:
            if not alive_unit.ready_to_attack():
                continue
            active_units.append(alive_unit)
        return active_units

    def calc_squad_attack_success(self):
        """Calculate squad attack success"""
        attack_success_list = []
        active_units = self.get_active_units()
        if len(active_units) == 0:
            return 0
        for unit in active_units:
            a_s = unit.calc_attack_success()
            attack_success_list.append(a_s)
        return geometric_mean(attack_success_list)

    def calc_squad_damage(self):
        """Calculate squad damage"""
        damage = 0
        active_units = self.get_active_units()
        for unit in active_units:
            damage += unit.calc_damage()
        return damage

    def take_damage(self, damage):
        """Take damage from attacker squad"""
        alive_units = self.get_alive_units()
        units_count = len(alive_units)
        if units_count == 0:
            return
        damage_for_unit = damage / units_count
        for unit in alive_units:
            unit.take_damage(damage_for_unit)

    def update_soldier_experience(self):
        """Update soldier experience"""
        active_units = self.get_active_units()
        for unit in active_units:
            unit.update_experience()

    def update_units_time_last_attack(self):
        """Update last time unit attack"""
        active_units = self.get_active_units()
        for unit in active_units:
            unit.time_last_attack = int(round(time.time() * 1000))

    def attack(self, enemy_squads_list, army_name):
        """Attack the defender squad"""
        enemy = SQUAD_STRATEGIES[self.strategy](enemy_squads_list)
        attacker_success = self.calc_squad_attack_success()
        attacker_damage = self.calc_squad_damage()

        enemy_success = enemy.calc_squad_attack_success()
        print(f'{army_name} attack_success = {attacker_success} - enemy attack_success = {enemy_success}')
        if attacker_success <= enemy_success:
            return {
                "success": 'lost',
                "damage": 0,
            }
        enemy.take_damage(attacker_damage)
        self.update_soldier_experience()
        self.update_units_time_last_attack()
        print(f'{army_name} caused damage = {attacker_damage}, enemy squad health = {enemy.squad_health()}')
        return {
            "success": 'win',
            "damage": attacker_damage,
        }
