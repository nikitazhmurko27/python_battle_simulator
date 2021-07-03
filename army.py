"""Army class realization"""


class Army:
    """
    The class provide main properties and methods
    for army.
    """
    def __init__(self, name, squads):
        self.name = name
        self.squads = squads

    def get_army_health(self):
        """Get army health"""
        health = 0
        for squad in self.squads:
            if not squad.is_active():
                continue
            squad_health = squad.squad_health()
            health += squad_health
        return health

    def is_active(self):
        """Check if squad is alive"""
        squads_count = len(self.squads)
        dead_squads_count = 0
        for squad in self.squads:
            if squad.is_active():
                continue
            dead_squads_count += 1
        return squads_count > dead_squads_count

    def attack(self, enemies):
        """Attack the defender army"""
        attack_result = []
        for squad in self.squads:
            active_units = squad.get_active_units()
            if len(active_units) == 0:
                continue
            attack_result.append(squad.attack(enemies, self.name))
        return attack_result
