"""Soldier(type of unit) class realization"""
from unit import Unit
from statistics import geometric_mean


class Vehicle(Unit):
    """
    The class provide main properties and methods
    for vehicle type of unit.
    """
    def __init__(self, operators, recharge):
        super().__init__(100, recharge)
        self.operators = operators

    @property
    def total_health(self):
        """
        Get vehicle health
        includes health of operators
        """
        return self.health + self.operators_health()

    def operators_health(self):
        """Get health of vehicle operators"""
        count = len(self.operators)
        health = 0
        for operator in self.operators:
            if not operator.is_alive():
                continue
            health += operator.health
        return health / count

    def operators_attack_success(self):
        """Get attack success of vehicle operators"""
        attack_success_list = []
        for operator in self.operators:
            if not operator.is_alive():
                continue
            attack_success_list.append(operator.calc_attack_success())
        return geometric_mean(attack_success_list)

    def operators_experience(self):
        """Get experience of vehicle operators"""
        exp = 0
        for operator in self.operators:
            if not operator.is_alive():
                continue
            exp += operator.experience
        return exp

    def update_experience(self):
        """Update experience of vehicle operators"""
        for operator in self.operators:
            if not operator.is_alive():
                continue
            if not operator.ready_to_attack():
                continue
            operator.update_experience()

    def calc_attack_success(self):
        return 0.5 * \
               (1 + self.health / 100) * \
               self.operators_attack_success()

    def calc_damage(self):
        return 0.1 + self.operators_experience() / 100

    def kill_operators(self):
        for operator in self.operators:
            operator.health = 0

    def take_damage(self, damage):
        self.health -= 0.6 * damage
        if self.health <= 0:
            self.kill_operators()
            return
        if len(self.operators) == 3:
            r_operator = self.custom_random.choice(self.operators)
            r_operator.health -= 0.2 * damage
            r_operator_index = self.operators.index(r_operator)
            for operator in self.operators:
                operator_index = self.operators.index(operator)
                if operator_index == r_operator_index:
                    continue
                operator.take_damage(0.1 * damage)
            return

        if len(self.operators) == 2:
            for operator in self.operators:
                operator.take_damage(0.2 * damage)
            return

        if len(self.operators) == 1:
            for operator in self.operators:
                operator.take_damage(0.4 * damage)
            return
