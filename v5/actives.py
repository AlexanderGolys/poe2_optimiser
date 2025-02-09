from v5.passives import *
import functools


class DamageConversion:
    def __init__(self, from_='Physical', to='Physical', value=0):
        self.from_ = from_
        self.to = to
        self.value = value

    def __call__(self, damage):
        dmg = deepcopy(damage)
        dmg[self.to] += dmg[self.from_] * self.value
        dmg[self.from_] *= 1 - self.value
        return dmg


class DamageGain:
    def __init__(self, element, value):
        self.element = element
        self.value = value

    def __call__(self, damage):
        dmg = deepcopy(damage)
        dmg[self.element] += dmg.sum() * self.value
        return dmg


class SkillGem:
    def __init__(self, *modifiers, mana_cost_mult=1, spirit_cost_add=0):
        self.modifiers = list(modifiers)
        self.mana_cost_mult = mana_cost_mult
        self.spirit_cost_add = spirit_cost_add


class ActiveSkill:
    def __init__(self, name, conversion, dmg_mult, speed_mult, mana_cost, level, quality=0, modifiers=[], gems=[], cooldown=0, spirit_cost=0,
                 mana_cost_per_new_level=[], dmg_mult_per_new_level=[]):
        self.conversion = conversion
        self.dmg_mult = dmg_mult
        self.speed_mult = speed_mult
        self.mana_cost_ = mana_cost
        self.spirit_cost_ = spirit_cost
        self.level = level
        self.quality = quality
        self.modifiers_ = modifiers
        self.gems = gems
        self.cooldown = cooldown
        self.name = name



        self.extra_level_dmg_mult = [dmg_mult]
        for mult in dmg_mult_per_new_level:
            self.extra_level_dmg_mult.append(self.extra_level_dmg_mult[-1] + mult)

        self.extra_level_cost = [mana_cost]
        for cost in dmg_mult_per_new_level:
            self.extra_level_cost.append(self.extra_level_cost[-1] + cost)

    @property
    def modifiers(self):
        return self.modifiers_ + sum([gem.modifiers for gem in self.gems], [])

    @property
    def mana_cost(self):
        return functools.reduce(lambda x, y: x * y, [gem.mana_cost_mult for gem in self.gems], self.mana_cost_)

    @property
    def spirit_cost(self):
        return sum([gem.spirit_cost_add for gem in self.gems], self.spirit_cost_)

    def get_damage_mult_for_level(self, extra_level):
        if extra_level >= len(self.extra_level_dmg_mult):
            return self.extra_level_dmg_mult[-1]
        return self.extra_level_dmg_mult[extra_level]


class ProjectileSkill(ActiveSkill):
    pass
