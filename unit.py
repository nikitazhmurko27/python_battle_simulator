"""Unit class realization"""
import json
import time
import random as custom_rand
from abc import ABCMeta, abstractmethod

with open("config.json") as config_file:
    config_object = json.load(config_file)
    config_file.close()

seed_value = config_object['seed']
custom_rand.seed(seed_value)


class Unit(metaclass=ABCMeta):
    """
    The class provide main properties and methods for game units.
    """

    def __init__(self, health=100, recharge=100, custom_random=custom_rand):
        self.health = health
        self.recharge = recharge
        self.time_last_attack = 0
        self.custom_random = custom_random

    @property
    def health(self):
        """Get unit health"""
        return self._health

    @health.setter
    def health(self, value):
        """Set unit health"""
        if value > 100:
            raise ValueError("health should be less than 100")
        self._health = value

    @property
    def recharge(self):
        """Get unit recharge"""
        return self._recharge

    @recharge.setter
    def recharge(self, value):
        """Set unit recharge"""
        if value > 2000:
            raise ValueError("recharge should be less than 2000")
        self._recharge = value

    @property
    def time_last_attack(self):
        """Get time of unit last attack"""
        return self._time_last_attack

    @time_last_attack.setter
    def time_last_attack(self, value):
        """Set time of unit last attack"""
        self._time_last_attack = value

    def is_alive(self):
        """Check if unit is alive"""
        return self.health > 0

    def ready_to_attack(self):
        """Check if unit ready to attack"""
        time_next_attack = self.time_last_attack + self.recharge
        current_time = int(round(time.time() * 1000))
        if self.time_last_attack == 0:
            return True
        return time_next_attack <= current_time

    @abstractmethod
    def calc_attack_success(self):
        """Calculate unit attack success"""

    @abstractmethod
    def calc_damage(self):
        """Calculate unit damage"""

    @abstractmethod
    def take_damage(self, damage):
        """Take damage from attacker unit"""
