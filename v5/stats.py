from copy import deepcopy

import numpy as np
from src.custom_units import *


class StatValue:
    def __init__(self, base, increase=1, more=1, maximum=None):
        self.flat = base
        self.increase = increase
        self.more = more
        self.prec = 2
        self.maximum = maximum

    def value(self):
        if self.maximum is not None:
            return minimum(self.flat * self.increase * self.more, self.maximum)
        return self.flat * self.increase * self.more

    def add(self, bonus):
        return self.__class__(self.flat + bonus, self.increase, self.more, self.maximum)


    def increase_bonus(self, bonus):
        return self.__class__(self.flat, self.increase + bonus, self.more, self.maximum)

    def more_bonus(self, bonus):
        return self.__class__(self.flat, self.increase, self.more * (1 + bonus), self.maximum)

    def less_bonus(self, bonus):
        return self.__class__(self.flat, self.increase, self.more * (1 - bonus), self.maximum)

    def __str__(self):
        if self.more == 1:
            if self.increase == 1:
                return f'{self.value():.{self.prec}f}'
            return f'{self.value():.{self.prec}f} \n\t({self.flat:.{self.prec}f} \t +{self.increase * 100 - 100:.0f}%)'
        return f'{self.value():.{self.prec}f} \n\t({self.flat:.{self.prec}f} \t +{self.increase * 100 - 100:.0f}% x{self.more:.2f})'

    def __repr__(self):
        return self.__str__()

    def bound(self, maximum):
        return self.__class__(self.flat, self.increase, self.more, maximum)


class IntStatValue(StatValue):
    def __init__(self, base, increase=1, more=1, maximum=None):
        super().__init__(base, increase, more, maximum)
        self.prec = 0




DMG0_LST = [Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0])]


class DamageStatValue(StatValue):
    def __init__(self, base=DamageTypeVector(DMG0_LST), increase=Vector([1, 1, 1, 1, 1]), more=Vector([1, 1, 1, 1, 1])):
        if isinstance(increase, (int, float)):
            increase = Vector([increase, increase, increase, increase, increase])
        if isinstance(more, (int, float)):
            more = Vector([more, more, more, more, more])
        super().__init__(base, increase, more)

    def add(self, bonus):
        return DamageStatValue(self.flat + bonus, self.increase, self.more)

    def increase_bonus(self, bonus):
        if isinstance(bonus, (int, float)):
            bonus = Vector([bonus, bonus, bonus, bonus, bonus])
        return DamageStatValue(self.flat, self.increase + bonus, self.more)

    def more_bonus(self, bonus):
        new_more = self.more
        if isinstance(bonus, (int, float)):
            new_more *= 1 + bonus
        else:
            if isinstance(bonus[0], (int, float)):
                new_more = Vector([m * (1 + b) for m, b in zip(self.more, bonus)])
            if isinstance(bonus[0], Vector):
                new_more = Vector([(Vector([1]*len(bonus[0])) + b)*m for m, b in zip(self.more, bonus)])
        return DamageStatValue(self.flat, self.increase, new_more)

    def less_bonus(self, bonus):
        return self.more_bonus(bonus * -1)

    def __str__(self):
        inc = Vector([Percent(self.increase[i] - 1) for i in range(5)])
        if self.more == Vector([1, 1, 1, 1, 1]):
            return f'{self.value():.0f} \t {self.value().sum():.0f} \t {self.value().sum().mean():.0f} \n\t({self.flat} \t +{inc})'
        return f'{self.value():.0f} \t {self.value().sum():.0f} \t {self.value().sum().mean():.0f} \n\t({self.flat:.0f} \t +{inc:.0f}% x{self.more:.2f})'


class StatName:
    def __init__(self, name, neutral_base=0, int_valued=False, maximum=None, prec=None):
        self.name = name
        if isinstance(neutral_base, DamageStatValue):
            self.neutral_value = neutral_base
            self.prec = 0
        elif int_valued:
            self.neutral_value = IntStatValue(neutral_base, maximum=maximum)
            self.prec = 0
        else:
            self.neutral_value = StatValue(neutral_base, maximum=maximum)
            self.prec = 2
            # self.neutral_value = 0
        self.prec = prec if prec is not None else self.prec

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name




class IntStatName(StatName):
    def __init__(self, name, neutral_base=0, maximum=None):
        super().__init__(name, neutral_base, True, maximum=maximum)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return self.__str__()


class StatSpecialisation:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


Granade = StatSpecialisation('Granade')
CloseRange = StatSpecialisation('Close Range (0-2m)')
FarAway = StatSpecialisation('Far Away (7m+)')
LowLifeEnemy = StatSpecialisation('Agains Enemies on Low Life')
LowLifePlayer = StatSpecialisation('On Low Life')
KilledRecently = StatSpecialisation('If Killed Recently (<4s)')
AgainstElementalAilments = StatSpecialisation('Against Enemies under Elemental Ailments')


class SpecialisedStatName(StatName):
    def __init__(self, base, specialisation, maximum=None):
        super().__init__(f'{specialisation.name} {base.name}', base.neutral_value, maximum=maximum)
        self.specialisation = specialisation
        self.base = base

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


AttackSpeed = StatName('Attack Speed', prec=3)
CastSpeed = StatName('Cast Speed')

Damage = StatName('Damage', DamageStatValue())
ThornsDamage = StatName('Thorns Damage', DamageStatValue())

Life = IntStatName('Life')
LifeRegenerationRate = StatName('Life Regeneration Per Second')
LifePerKill = IntStatName('Life per Kill')
LifePerHit = IntStatName('Life per Hit')
PhysicalLifeLeech = StatName('Physical Damage Leeched as Life', Percent(0))

Mana = IntStatName('Mana')
ManaPerKill = IntStatName('Mana per Kill')
ManaPerHit = IntStatName('Mana per Hit')
ManaRegenerationRate = StatName('Mana Regeneration Rate')

Spirit = IntStatName('Spirit')
Accuracy = IntStatName('Accuracy')
Strength = IntStatName('Strength')
Dexterity = IntStatName('Dexterity')
Intelligence = IntStatName('Intelligence')
ReloadTime = StatName('Reload Time')
MovementSpeed = StatName('Movement Speed')
Rarity = StatName('Rarity of Items Found', Percent(0), prec=0)
CritChance = StatName('Crit Chance', Percent(0))
CritBonus = StatName('Crit Bonus', Percent(0), prec=0)
Armour = IntStatName('Armour')
Evasion = IntStatName('Evasion')
EnergyShield = IntStatName('Energy Shield')

CooldownRecoveryRate = StatName('Cooldown Recovery Rate')
AreaOfEffect = StatName('Area Of Effect')
SkillEffectDuration = StatName('Skill Effect Duration', Percent(0))
BuffDuration = StatName('Buff Duration (on you)', Percent(0))

ExtraCooldownUses = IntStatName('Extra Cooldown Uses')
ExtraProjectiles = IntStatName('Extra Projectiles')
ProjectileSpeed = StatName('Projectile Speed')
FuseDuration = StatName('Fuse Duration')
ExtraProjectileSkillLevel = IntStatName('Extra Projectile Skill Level')

Resistances = StatName('Resistances', ResistanceVector([Percent(0), Percent(0), Percent(0), Percent(0)]))
MaxResistances = StatName('Max Resistances', ResistanceVector([Percent(0), Percent(0), Percent(0), Percent(0)]), maximum=ResistanceVector([Percent(0.9), Percent(0.9), Percent(0.9), Percent(0.9)]))
ElementalPenetration = StatName('Elemental Penetration', ResistanceVector([Percent(0), Percent(0), Percent(0), Percent(0)]), maximum=ResistanceVector([Percent(1), Percent(1), Percent(1), Percent(0)]))

StunThreshold = IntStatName('Stun Threshold')

ManaRecoveryFromFlask = StatName('Mana Recovery from Flask')
LifeRecoveryFromFlask = StatName('Life Recovery from Flask')
ManaFlaskRecoveryRate = StatName('Mana Flask Recovery Rate')
LifeFlaskRecoveryRate = StatName('Life Flask Recovery Rate')
LifeFlaskCharges = IntStatName('Life Flask Charges')
ManaFlaskCharges = IntStatName('Mana Flask Charges')
LifeFlaskChargesCost = IntStatName('Life Flask Charges Cost')
ManaFlaskChargesCost = IntStatName('Mana Flask Charges Cost')
LifeFlaskChargesRecoveryPerSecond = StatName('Life Flask Charges Recovery per Second')
ManaFlaskChargesPerSecond = StatName('Mana Flask Charges Recovery per Second')
ChanceForManaFlaskChargePerKill = StatName('Chance to Gain Mana Flask Charge on Kill')
ChanceForLifeFlaskChargePerKill = StatName('Chance to Gain Life Flask Charge on Kill')
ManaFlaskChargesGain = StatName('Mana Flask Charges Gain Multiplier')
LifeFlaskChargesGain = StatName('Life Flask Charges Gain Multiplier')
ChanceToNotConsumeFlaskCharges = StatName('Chance for Flask to Not Consume Flask Charges on Use', Percent(0))

IgniteMagnitude = StatName('Ignite Magnitude')
ShockMagnitude = StatName('Shock Magnitude')
PoisonMagnitude = StatName('Poison Magnitude')
BleedingMagnitude = StatName('Bleeding Magnitude')
ChillMagnitude = StatName('Chill Magnitude')

ShockDuration = StatName('Shock Duration')
IgniteDuration = StatName('Ignite Duration')
PoisonDuration = StatName('Poison Duration')

PoisonChance = StatName('Chance to Poison on Hit', Percent(0), prec=0)
ShockChance = StatName('Chance to Shock on Hit', PerAilmentThreshold(0))
ElectrocuteBuildup = StatName('Electrocute Buildup')
FreezeBuildup = StatName('Freeze Buildup')
BleedingChance = StatName('Chance to inflict Bleeding', Percent(0), prec=0)
IgniteChance = StatName('Chance to Ignite on Hit', PerAilmentThreshold(0), prec=0)
PierceChance = StatName('Pierce Chance on Hit', Percent(0), prec=0)
PierceExtraTargets = IntStatName('Pierce Additional Targets')

BlindChance = StatName('Chance to Blind on Hit', Percent(0), prec=0)
MaimChance = StatName('Chance to Maim on Hit', Percent(0), prec=0)

BleedingDuration = StatName('Bleeding Duration')
ChillDuration = StatName('Chill Duration')
FreezeDuration = StatName('Freeze Duration')
ElectrocuteDuration = StatName('Electrocute Duration')

CharmChargesGain = StatName('Charm Charges Gain Multiplier')
CharmSlots = IntStatName('Charm Slots')
CharmDuration = StatName('Charm Duration')
CharmCharges = IntStatName('Charm Charges')
CharmCost = IntStatName('Charm Usage Charges Cost')


GranadeDamage = SpecialisedStatName(Damage, Granade)
GranadeAreaOfEffect = SpecialisedStatName(AreaOfEffect, Granade)
GranadeCooldownRecoveryRate = SpecialisedStatName(CooldownRecoveryRate, Granade)
GranadeExtraProjectiles = SpecialisedStatName(ExtraProjectiles, Granade)

CloseRangeAccuracy = SpecialisedStatName(Accuracy, CloseRange)

FarAwayDamage = SpecialisedStatName(Damage, FarAway)
FarAwayCritChance = SpecialisedStatName(CritChance, FarAway)

DamageAgainstLowLife = SpecialisedStatName(Damage, LowLifeEnemy)

MovementSpeedIfKilledRecently = SpecialisedStatName(MovementSpeed, KilledRecently)
AttackSpeedIfKilledRecently = SpecialisedStatName(AttackSpeed, KilledRecently)

DamageAgainstElementalAilments = SpecialisedStatName(Damage, AgainstElementalAilments)
