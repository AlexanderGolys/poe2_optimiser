from v5.modifiers import *


LIGHTNING_QUALITY = 'Lightning'
FIRE_QUALITY = 'Fire'
COLD_QUALITY = 'Cold'
CHAOS_QUALITY = 'Chaos'
PHYSICAL_QUALITY = 'Physical'
DEFENCE_QUALITY = 'Defence'
ATTACK_QUALITY = 'Attack'
SPEED_QUALITY = 'Speed'
ATTRIBUTE_QUALITY = 'Attribute'
MANA_QUALITY = 'Mana'
LIFE_QUALITY = 'Life'


class ArmourQualityModifier(NumericalModifier):
    def __init__(self, value):
        self.value_ = value

        def act(name, v):
            if name in [Armour, Evasion, EnergyShield]:
                return v.more_bonus(self.value)
            return v

        super().__init__(act, value, True, False)

    def inv_value(self):
        return 1 / (1 + self.value_) - 1

    def __invert__(self):
        i = deepcopy(self)
        i.value_ = i.inv_value()
        return i

    def __str__(self):
        if self.value == 0:
            return f'No effect from Quality'
        return f'{self.value:.2%} more Armour, Evasion, and Energy Shield from Quality'


class WeaponQualityModifier(NumericalModifier):
    def __init__(self, value):
        self.value_ = value
        self.rounding = True

        def act(name, value):
            if name == Damage:
                return value.more_bonus(self.value)
            return value

        super().__init__(act, value, True, False)

    def inv_value(self):
        return 1 / (1 + self.value_) - 1

    def __str__(self):
        if self.value == 0:
            return f'No effect from Quality'
        return f'{self.value:.2%} more Physical Damage from Quality'
