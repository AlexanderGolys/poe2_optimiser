from v5.stats import *
from v5.qualities import *


class Modifier:
    def __init__(self, action, local=False):
        self.action = action
        self.local = local

    def __call__(self, name, value):
        return self.action(name, value)


class LightningRodModifier(Modifier):
    def __init__(self):
        super().__init__(lambda name, value: value, False)

    def __str__(self):
        return f'Non-critical lightning damage is Lucky'

    def __eq__(self, other):
        return isinstance(other, LightningRodModifier)


class DependentModifier:
    def __init__(self, init):
        self.init = init

    def __call__(self, player):
        return self.init(player)


wisdom_dex = DependentModifier(lambda player: AttackSpeedIncrease(0.03 * (int(player.get_stat(Dexterity, True).value()) // 25)))
widom_int = DependentModifier(lambda player: AddLightningDamage(int(player.get_stat(Intelligence, True).value()) // 10, 10 * (int(player.get_stat(Intelligence, True).value()) // 10)))
feathered_fletching = DependentModifier(lambda player: AllDamageIncreaseModifier(player.get_stat(ProjectileSpeed, True).increase - 1))


class NumericalModifier(Modifier):
    def __init__(self, act, value, local=False, rounding=False, qualities=[]):
        self.value_ = value
        self.rounding = rounding
        self.magnitude = 1
        self.applicable_qualities = qualities
        super().__init__(act, local)

    @property
    def value(self):
        if self.rounding:
            return round(self.value_)
        return self.value_

    @value.setter
    def value(self, value):
        self.value_ = value

    def magnify_to(self, magnitude):
        self.value *= magnitude/self.magnitude
        self.magnitude = magnitude


    def inv_value(self):
        return -self.value_

    def __invert__(self):
        i = deepcopy(self)
        i.value_ = i.inv_value()
        return i



class AddModifier(NumericalModifier):
    def __init__(self, stat_name, value, rounding=False, qualities=[]):
        self.stat_name = stat_name

        def act(name, value):
            if self.stat_name == name or isinstance(name, SpecialisedStatName) and name.base == self.stat_name:
                return value.add(deepcopy(self.value))
            return value

        super().__init__(act, value, False, rounding, qualities)

    def __str__(self):
        return f'Adds +{self.value} to {self.stat_name}'


class LocalAddModifier(AddModifier):
    def __init__(self, stat_name, value, rounding=False):
        super().__init__(stat_name, value, rounding)
        self.local = True


class IncreaseModifier(NumericalModifier):
    def __init__(self, stat_name, value, qualities=[]):
        self.stat_name = stat_name

        def act(name, value):
            if self.stat_name == name or isinstance(name, SpecialisedStatName) and name.base == self.stat_name:
                return value.increase_bonus(self.value)
            return value

        super().__init__(act, value, False, False, qualities=qualities)

    def __str__(self):
        return f'{self.value} increased {self.stat_name}'


class LocalIncreaseModifier(IncreaseModifier):
    def __init__(self, stat_name, value):
        super().__init__(stat_name, value)
        self.local = True


class DamageIncreaseModifier(IncreaseModifier):
    def __init__(self, physical=0, fire=0, cold=0, lightning=0, chaos=0):
        super().__init__(Damage, Vector([physical, lightning, fire, cold, chaos]),
                         qualities=[ATTACK_QUALITY])


class AllDamageIncreaseModifier(DamageIncreaseModifier):
    def __init__(self, value):
        super().__init__(value, value, value, value, value)


class ElementalDamageIncrease(DamageIncreaseModifier):
    def __init__(self, value):
        super().__init__(0, value, value, value, 0)


class PhysicalDamageIncrease(DamageIncreaseModifier):
    def __init__(self, value):
        super().__init__(value, 0, 0, 0, 0)
        self.applicable_qualities += [PHYSICAL_QUALITY]


class AddPhysicalDamage(AddModifier):
    def __init__(self, v0, v1):
        super().__init__(Damage, Vector([Vector([v0, v1]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0])]))
        self.applicable_qualities += [PHYSICAL_QUALITY]


class AddLightningDamage(AddModifier):
    def __init__(self, v0, v1):
        super().__init__(Damage, Vector([Vector([0, 0]), Vector([v0, v1]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0])]))
        self.applicable_qualities += [LIGHTNING_QUALITY]


class AddFireDamage(AddModifier):
    def __init__(self, v0, v1):
        super().__init__(Damage, Vector([Vector([0, 0]), Vector([0, 0]), Vector([v0, v1]), Vector([0, 0]), Vector([0, 0])]))
        self.applicable_qualities += [FIRE_QUALITY]


class AddColdDamage(AddModifier):
    def __init__(self, v0, v1):
        super().__init__(Damage, Vector([Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([v0, v1]), Vector([0, 0])]))
        self.applicable_qualities += [COLD_QUALITY]


class AddChaosDamage(AddModifier):
    def __init__(self, v0, v1):
        super().__init__(Damage, Vector([Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([v0, v1])]))
        self.applicable_qualities += [CHAOS_QUALITY]


class LocalAddPhysicalDamage(LocalAddModifier):
    def __init__(self, v0, v1):
        super().__init__(Damage, Vector([Vector([v0, v1]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0])]))


class LocalAddLightningDamage(LocalAddModifier):
    def __init__(self, v0, v1):
        super().__init__(Damage, Vector([Vector([0, 0]), Vector([v0, v1]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0])]))


class LocalAddFireDamage(LocalAddModifier):
    def __init__(self, v0, v1):
        super().__init__(Damage, Vector([Vector([0, 0]), Vector([0, 0]), Vector([v0, v1]), Vector([0, 0]), Vector([0, 0])]))


class LocalAddColdDamage(LocalAddModifier):
    def __init__(self, v0, v1):
        super().__init__(Damage, Vector([Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([v0, v1]), Vector([0, 0])]))


class LocalAddChaosDamage(LocalAddModifier):
    def __init__(self, v0, v1):
        super().__init__(Damage, Vector([Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([v0, v1])]))


class MultiIncreaseModifier(NumericalModifier):
    def __init__(self, stats, value):
        self.stats = stats

        def act(name, value):
            if name in self.stats or isinstance(name, SpecialisedStatName) and name.base in self.stats:
                return value.increase_bonus(self.value)
            return value

        super().__init__(act, value, False, False)


class MultiAddModifier(NumericalModifier):
    def __init__(self, stats, value):
        self.stats = stats

        def act(name, value):
            if name in self.stats or isinstance(name, SpecialisedStatName) and name.base in self.stats:
                return value.add(self.value)
            return value

        super().__init__(act, value, False, False)


class IncreasePhysicalDamage(IncreaseModifier):
    def __init__(self, value):
        super().__init__(Damage, Vector([value, 0, 0, 0, 0]))


class IncreaseLightningDamage(IncreaseModifier):
    def __init__(self, value):
        super().__init__(Damage, Vector([0, value, 0, 0, 0]))


class IncreaseFireDamage(IncreaseModifier):
    def __init__(self, value):
        super().__init__(Damage, Vector([0, 0, value, 0, 0]))


class IncreaseColdDamage(IncreaseModifier):
    def __init__(self, value):
        super().__init__(Damage, Vector([0, 0, 0, value, 0]))


class IncreaseChaosDamage(IncreaseModifier):
    def __init__(self, value):
        super().__init__(Damage, Vector([0, 0, 0, 0, value]))


class LocalMultiIncreaseModifier(MultiIncreaseModifier):
    def __init__(self, stats, value):
        super().__init__(stats, value)
        self.local = True


class LocalDefenceIncrease(LocalMultiIncreaseModifier):
    def __init__(self, value):
        super().__init__([Armour, Evasion, EnergyShield], value)


class LocalPhysicalDamageIncrease(LocalIncreaseModifier):
    def __init__(self, value):
        super().__init__(Damage, Vector([value, 0, 0, 0, 0]))


class MoreModifier(NumericalModifier):
    def __init__(self, stat_name, value):
        self.stat_name = stat_name
        self.value_ = value

        def act(name, v):
            if name == self.stat_name or isinstance(name, SpecialisedStatName) and name.base == self.stat_name:
                return v.more_bonus(self.value)
            return v

        super().__init__(act, value, False, False)

    def __str__(self):
        return f'{self.value} more {self.stat_name}'

    def inv_value(self):
        return 1 / (1 + self.value_) - 1


# AddResistance = lambda res, value: AddModifier(Resistances, ResistanceVector(**{res: value}))
class AddResistance(AddModifier):
    def __init__(self, res, value):
        super().__init__(Resistances, ResistanceVector(**{res: value}))


class AddElementalResistances(AddModifier):
    def __init__(self, value):
        super().__init__(Resistances, ResistanceVector([value, value, value, 0]))


class AddLightningResistance(AddResistance):
    def __init__(self, value):
        super().__init__('Lightning', value)
        self.applicable_qualities += [LIGHTNING_QUALITY]


class AddFireResistance(AddResistance):
    def __init__(self, value):
        super().__init__('Fire', value)
        self.applicable_qualities += [FIRE_QUALITY]


class AddColdResistance(AddResistance):
    def __init__(self, value):
        super().__init__('Cold', value)
        self.applicable_qualities += [COLD_QUALITY]


class AddChaosResistance(AddResistance):
    def __init__(self, value):
        super().__init__('Chaos', value)
        self.applicable_qualities += [CHAOS_QUALITY]


class AddMana(AddModifier):
    def __init__(self, value):
        super().__init__(Mana, value, qualities=[MANA_QUALITY])


class AddLife(AddModifier):
    def __init__(self, value):
        super().__init__(Life, value, qualities=[LIFE_QUALITY])


class AddRarity(AddModifier):
    def __init__(self, value):
        super().__init__(Rarity, value)


class AddSpirit(AddModifier):
    def __init__(self, value):
        super().__init__(Spirit, value)


class AddStrength(AddModifier):
    def __init__(self, value):
        super().__init__(Strength, value, qualities=[ATTRIBUTE_QUALITY])


class AddDexterity(AddModifier):
    def __init__(self, value):
        super().__init__(Dexterity, value, qualities=[ATTRIBUTE_QUALITY])


class AddIntelligence(AddModifier):
    def __init__(self, value):
        super().__init__(Intelligence, value, qualities=[ATTRIBUTE_QUALITY])


class IncreaseAilmentMagnitude(MultiIncreaseModifier):
    def __init__(self, value):
        super().__init__([IgniteMagnitude, ShockMagnitude, PoisonMagnitude, BleedingMagnitude, ChillMagnitude], value)


class AddAccuracy(AddModifier):
    def __init__(self, value):
        super().__init__(Accuracy, value, qualities=[ATTACK_QUALITY])


class AddAllAttributes(MultiAddModifier):
    def __init__(self, value):
        super().__init__([Strength, Dexterity, Intelligence], value)
        self.applicable_qualities = [ATTRIBUTE_QUALITY]


class MovementSpeedIncrease(IncreaseModifier):
    def __init__(self, value):
        super().__init__(MovementSpeed, value)


class AttackSpeedIncrease(IncreaseModifier):
    def __init__(self, value):
        super().__init__(AttackSpeed, value)


class ProjectileSpeedIncrease(IncreaseModifier):
    def __init__(self, value):
        super().__init__(ProjectileSpeed, value)


class SkillSpeedIncrease(MultiIncreaseModifier):
    def __init__(self, value):
        super().__init__([CastSpeed, AttackSpeed], value)


class AddElementalPenetration(AddModifier):
    def __init__(self, value):
        super().__init__(ElementalPenetration, ResistanceVector([value, value, value, 0]))


class AddLightningPenetration(AddModifier):
    def __init__(self, value):
        super().__init__(ElementalPenetration, ResistanceVector([value, 0, 0, 0]))


class AilmentChanceIncrease(MultiIncreaseModifier):
    def __init__(self, value):
        super().__init__([IgniteChance, ShockChance, PoisonChance, BleedingChance], value)


class AddPierceChance(AddModifier):
    def __init__(self, value):
        super().__init__(ExtraProjectiles, value)


class FlaskRecoveryIncrease(MultiIncreaseModifier):
    def __init__(self, value):
        super().__init__([ManaRecoveryFromFlask, LifeRecoveryFromFlask], value)


class AddManaPerKill(AddModifier):
    def __init__(self, value):
        super().__init__(ManaPerKill, value, qualities=[MANA_QUALITY])


class AddLifePerKill(AddModifier):
    def __init__(self, value):
        super().__init__(LifePerKill, value, qualities=[LIFE_QUALITY])


class AddEvasion(AddModifier):
    def __init__(self, value):
        super().__init__(Evasion, value, qualities=[DEFENCE_QUALITY])


class AddEnergyShield(AddModifier):
    def __init__(self, value):
        super().__init__(EnergyShield, value, qualities=[DEFENCE_QUALITY])


class IncreasedManaRegen(IncreaseModifier):
    def __init__(self, value):
        super().__init__(ManaRegenerationRate, value, qualities=[MANA_QUALITY])
