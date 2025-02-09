from v5.stats import *


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
    def __init__(self, act, value, local=False, rounding=False, quality_tags=[]):
        self.value_ = value
        self.rounding = rounding
        self.magnitude = 1
        self.quality_tags = quality_tags
        super().__init__(act, local)

    @property
    def value(self):
        if self.rounding:
            return round(self.value_ * self.magnitude)
        return self.value_ * self.magnitude

    @value.setter
    def value(self, value):
        self.value_ = value
        if self.rounding:
            self.value_ = round(self.value_)

    def set_magnitude_from_quality(self, quality, quality_tag):
        if quality_tag in self.quality_tags:
            self.magnitude = 1 + quality
        else:
            self.magnitude = 1

    def inv_value(self):
        return -self.value_

    def __invert__(self):
        i = deepcopy(self)
        i.value_ = i.inv_value()
        return i

    def rebase_applied_magnitude(self):
        self.value_ = self.value_ / self.magnitude


class AddModifier(NumericalModifier):
    def __init__(self, stat_name, value, rounding=False):
        self.stat_name = stat_name

        def act(name, value):
            if self.stat_name == name or isinstance(name, SpecialisedStatName) and name.base == self.stat_name:
                return value.add(deepcopy(self.value))
            return value

        super().__init__(act, value, False, rounding)

    def __str__(self):
        return f'Adds +{self.value} to {self.stat_name}'


class LocalAddModifier(AddModifier):
    def __init__(self, stat_name, value, rounding=False):
        super().__init__(stat_name, value, rounding)
        self.local = True


class IncreaseModifier(NumericalModifier):
    def __init__(self, stat_name, value):
        self.stat_name = stat_name

        def act(name, value):
            if self.stat_name == name or isinstance(name, SpecialisedStatName) and name.base == self.stat_name:
                return value.increase_bonus(self.value)
            return value

        super().__init__(act, value, False, False)

    def __str__(self):
        return f'{self.value} increased {self.stat_name}'


class DamageIncreaseModifier(IncreaseModifier):
    def __init__(self, physical=0, fire=0, cold=0, lightning=0, chaos=0):
        super().__init__(Damage, Vector([physical, lightning, fire, cold, chaos]))


class AllDamageIncreaseModifier(DamageIncreaseModifier):
    def __init__(self, value):
        super().__init__(value, value, value, value, value)


class ElementalDamageIncrease(DamageIncreaseModifier):
    def __init__(self, value):
        super().__init__(0, value, value, value, 0)


class PhysicalDamageIncrease(DamageIncreaseModifier):
    def __init__(self, value):
        super().__init__(value, 0, 0, 0, 0)


class AddPhysicalDamage(AddModifier):
    def __init__(self, v0, v1):
        super().__init__(Damage, Vector([Vector([v0, v1]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0])]))


class AddLightningDamage(AddModifier):
    def __init__(self, v0, v1):
        super().__init__(Damage, Vector([Vector([0, 0]), Vector([v0, v1]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0])]))


class AddFireDamage(AddModifier):
    def __init__(self, v0, v1):
        super().__init__(Damage, Vector([Vector([0, 0]), Vector([0, 0]), Vector([v0, v1]), Vector([0, 0]), Vector([0, 0])]))


class AddColdDamage(AddModifier):
    def __init__(self, v0, v1):
        super().__init__(Damage, Vector([Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([v0, v1]), Vector([0, 0])]))


class AddChaosDamage(AddModifier):
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


class LocalIncreaseModifier(IncreaseModifier):
    def __init__(self, stat_name, value):
        super().__init__(stat_name, value)
        self.local = True


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


class AddFireResistance(AddResistance):
    def __init__(self, value):
        super().__init__('Fire', value)


class AddColdResistance(AddResistance):
    def __init__(self, value):
        super().__init__('Cold', value)


class AddChaosResistance(AddResistance):
    def __init__(self, value):
        super().__init__('Chaos', value)


class AddMana(AddModifier):
    def __init__(self, value):
        super().__init__(Mana, value)


class AddLife(AddModifier):
    def __init__(self, value):
        super().__init__(Life, value)


class AddRarity(AddModifier):
    def __init__(self, value):
        super().__init__(Rarity, value)


class AddSpirit(AddModifier):
    def __init__(self, value):
        super().__init__(Spirit, value)


class AddStrength(AddModifier):
    def __init__(self, value):
        super().__init__(Strength, value)


class AddDexterity(AddModifier):
    def __init__(self, value):
        super().__init__(Dexterity, value)


class AddIntelligence(AddModifier):
    def __init__(self, value):
        super().__init__(Intelligence, value)


class IncreaseAilmentMagnitude(MultiIncreaseModifier):
    def __init__(self, value):
        super().__init__([IgniteMagnitude, ShockMagnitude, PoisonMagnitude, BleedingMagnitude, ChillMagnitude], value)


class AddAccuracy(AddModifier):
    def __init__(self, value):
        super().__init__(Accuracy, value)


class AddAllAttributes(MultiAddModifier):
    def __init__(self, value):
        super().__init__([Strength, Dexterity, Intelligence], value)


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
        super().__init__(ManaPerKill, value)


class AddLifePerKill(AddModifier):
    def __init__(self, value):
        super().__init__(LifePerKill, value)


class AddEvasion(AddModifier):
    def __init__(self, value):
        super().__init__(Evasion, value)


class AddEnergyShield(AddModifier):
    def __init__(self, value):
        super().__init__(EnergyShield, value)


class IncreasedManaRegen(IncreaseModifier):
    def __init__(self, value):
        super().__init__(ManaRegenerationRate, value)
