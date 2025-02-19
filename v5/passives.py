from src.items import *


class PassiveSkill:
    def __init__(self, modifiers):
        self.modifiers = modifiers

    def __str__(self):
        return '\n'.join([str(mod) for mod in self.modifiers])





class PassiveSkillSet:
    def __init__(self, full=[], ws1=[], ws2=[], jewels=[], ascendancy=[]):
        self.full = list(full) + [j.passive_skill() for j in jewels] + list(ascendancy)
        self.ws1 = list(ws1)
        self.ws2 = list(ws2)

    @property
    def weapon_set1(self):
        return self.ws1 + self.full

    @property
    def weapon_set2(self):
        return self.ws2 + self.full

    def weapon_set(self, i):
        if i == 1:
            return self.weapon_set1
        return self.weapon_set2

    def all_modifiers(self, weapon_set):
        if weapon_set == 1:
            return sum([s.modifiers for s in self.ws1 + self.full], [])
        return sum([s.modifiers for s in self.ws2 + self.full], [])


class SinglePassiveSkill(PassiveSkill):
    def __init__(self, modifier):
        super().__init__([modifier])


class StrengthPassive(SinglePassiveSkill):
    def __init__(self):
        super().__init__(AddModifier(Strength, 5))


class DexterityPassive(SinglePassiveSkill):
    def __init__(self):
        super().__init__(AddModifier(Dexterity, 5))


class IntelligencePassive(SinglePassiveSkill):
    def __init__(self):
        super().__init__(AddModifier(Intelligence, 5))


class IncreasedDamagePassive(SinglePassiveSkill):
    def __init__(self, value):
        super().__init__(AllDamageIncreaseModifier(value))


class IncreaseAttackSpeedPassive(SinglePassiveSkill):
    def __init__(self, value):
        super().__init__(IncreaseModifier(AttackSpeed, value))


class Jewel(Jewellery):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def passive_skill(self):
        return PassiveSkill(self.mods())
