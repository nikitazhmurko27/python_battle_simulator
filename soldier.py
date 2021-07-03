"""Soldier(type of unit) class realization"""
from unit import Unit


class Soldier(Unit):
    """
    The class provide main properties and methods
    for soldier type of unit.
    """
    def __init__(self, recharge, experience=0, ):
        super().__init__(100, recharge)
        self._experience = experience

    @property
    def experience(self):
        """Get soldier experience"""
        return self._experience

    def update_experience(self):
        """Set soldier experience"""
        if self._experience == 50:
            return
        self._experience += 1

    def calc_attack_success(self):
        return 0.5 * \
               (1 + self.health / 100) * \
               self.custom_random.randint(50 + self.experience, 100) / 100

    def calc_damage(self):
        return round(
            (0.05 + self.experience / 100),
            2
        )

    def take_damage(self, damage):
        self.health -= damage
