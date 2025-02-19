from v5.actives import *
import functools

forced_quest_mods_endgame = [
    AddResistance('Lightning', .1),
    AddResistance('Fire', .1),
    AddResistance('Cold', .1),
    AddModifier(Spirit, 30),
    AddModifier(Spirit, 30),
    AddModifier(Spirit, 40),
    AddModifier(Life, 20),
    IncreaseModifier(Life, .08)]


class Class:
    def __init__(self, name, base_strength, base_dexterity, base_intelligence, class_specific_stats=set()):
        self.name = name
        self.base_attributes = {Strength: base_strength, Dexterity: base_dexterity, Intelligence: base_intelligence}
        self.class_specific_stats = class_specific_stats


Ranger = Class('Ranger', 7, 15, 7, {ProjectileSpeed, ExtraProjectiles, PierceChance, CloseRangeAccuracy, FarAwayDamage,
                                    PierceExtraTargets})
Mercenary = Class('Mercenary', 11, 11, 7,
                  {GranadeDamage, GranadeAreaOfEffect, GranadeExtraProjectiles, FuseDuration, ExtraCooldownUses,
                   GranadeCooldownRecoveryRate, ProjectileSpeed, ExtraProjectiles, ReloadTime, PierceChance})
Monk = Class('Monk', 7, 11, 11)
Witch = Class('Witch', 7, 7, 15)
Sorcerer = Class('Sorcerer', 7, 7, 15, {CastSpeed})
Warrior = Class('Warrior', 15, 7, 7)

possible_classes = [Ranger, Mercenary, Monk, Witch, Sorcerer, Warrior]


class Player:
    class_specific_stats = functools.reduce(lambda x, y: x.union(y), [c.class_specific_stats for c in possible_classes], set())

    blocks = (

        [Damage,
         AttackSpeed,
         CastSpeed,
         CritChance,
         CritBonus,
         Accuracy,
         ReloadTime,
         AreaOfEffect,
         ExtraProjectileSkillLevel],

        [GranadeDamage,
         GranadeAreaOfEffect,
         GranadeExtraProjectiles,
         FuseDuration,
         ExtraCooldownUses,
         CooldownRecoveryRate,
         GranadeCooldownRecoveryRate,
         ],

        [Strength,
         Dexterity,
         Intelligence],

        [MovementSpeed,
         Rarity],

        [Resistances,
         Armour,
         Evasion,
         EnergyShield,
         MaxResistances,
         StunThreshold,
         ThornsDamage],

        [Life, LifeRegenerationRate, LifePerKill, LifePerHit, PhysicalLifeLeech],

        [Mana, ManaRegenerationRate, ManaPerKill, ManaPerHit],

        [IgniteMagnitude,
         IgniteDuration,
         IgniteChance,
         ShockMagnitude,
         ShockDuration,
         ShockChance,
         PoisonMagnitude,
         PoisonDuration,
         PoisonChance,
         BleedingDuration,
         BleedingMagnitude,
         BleedingChance,
         ElementalPenetration],

        [PierceChance,
         PierceExtraTargets,
         BlindChance,
         MaimChance,
         ProjectileSpeed,
         CloseRangeAccuracy,
         FarAwayDamage,
         FarAwayCritChance,
         DamageAgainstLowLife,
         DamageAgainstElementalAilments,
         SkillEffectDuration,
         BuffDuration,
         MovementSpeedIfKilledRecently,
         AttackSpeedIfKilledRecently
         ],

        [ManaRecoveryFromFlask,
         LifeRecoveryFromFlask,
         ManaFlaskRecoveryRate,
         LifeFlaskRecoveryRate,
         LifeFlaskCharges,
         ManaFlaskCharges,
         LifeFlaskChargesCost,
         ManaFlaskChargesCost,
         LifeFlaskChargesRecoveryPerSecond,
         ManaFlaskChargesPerSecond,
         ChanceForManaFlaskChargePerKill,
         ChanceForLifeFlaskChargePerKill,
         ManaFlaskChargesGain,
         LifeFlaskChargesGain,
         ChanceToNotConsumeFlaskCharges],

        [CharmCost,
         CharmDuration,
         CharmCharges,
         CharmChargesGain,
         CharmSlots],
    )

    DEFAULT_BASE_STATS = {
        ManaFlaskChargesGain: 1,
        LifeFlaskChargesGain: 1,
        MaxResistances: ResistanceVector([Percent(.75), Percent(.75), Percent(.75), Percent(.75)]),
        Rarity: Percent(0),
        CooldownRecoveryRate: 1,
        AreaOfEffect: 1,
        FuseDuration: 1,
        IgniteDuration: 4,
        IgniteMagnitude: .2,
        ShockDuration: 4,
        ShockMagnitude: .2,
        BleedingDuration: 5,
        BleedingMagnitude: .15,
        PoisonDuration: 2,
        PoisonMagnitude: .2,
        ChillDuration: 2,
        ChillMagnitude: 1,
        FreezeDuration: 4,
        ElectrocuteDuration: 5,
        ElementalPenetration: ResistanceVector([Percent(0), Percent(0), Percent(0), Percent(0)]),
        CharmSlots: 1,
        CritBonus: Percent(1),
        ProjectileSpeed: 1,
        PoisonChance: Percent(0),
        ShockChance: PerAilmentThreshold(.01),
        IgniteChance: PerAilmentThreshold(.01),
        BleedingChance: Percent(0),
        ChanceToNotConsumeFlaskCharges: Percent(0),
        SkillEffectDuration: Percent(1),
        BuffDuration: Percent(1),
        ElectrocuteBuildup: 0,
        FreezeBuildup: 0,
        BlindChance: Percent(0),
    }

    def __init__(self, classname, level, inventory, passive_skills, quest_mods_chosen, quest_mods_forced=forced_quest_mods_endgame, base_stats={}, active_skills=[]):
        self.classname = classname
        self.level = level
        self.inventory = inventory
        self.base_stats = base_stats
        self.quest_mods = quest_mods_chosen + quest_mods_forced
        self.passive_skills = passive_skills
        self.wss = 1
        self.active_skills = active_skills

        for stat, default in self.DEFAULT_BASE_STATS.items():
            if stat not in self.base_stats:
                self.base_stats[stat] = default

        for attr in self.classname.base_attributes.keys():
            self.base_stats[attr] = self.classname.base_attributes[attr]

        self.base_stats[Life] = 16 + 12 * level + 2 * self.get_stat(Strength).value()
        self.base_stats[Mana] = 30 + 4 * level + 2 * self.get_stat(Intelligence).value()
        self.base_stats[Accuracy] = 5 * self.get_stat(Dexterity).value()
        self.base_stats[ManaRegenerationRate] = .04 * self.get_stat(Mana).value()

    def get_base(self, stat_name):
        if stat_name == MovementSpeed:
            return StatValue(1).less_bonus(self.inventory.movement_speed_penalty())
        if stat_name in self.base_stats:
            return StatValue(self.base_stats[stat_name])
        if isinstance(stat_name, SpecialisedStatName):
            return self.get_base(stat_name.base)
        return stat_name.neutral_value

    def global_mods(self):
        return self.quest_mods + self.passive_skills.all_modifiers(self.wss) + self.inventory.global_mods(self.wss)

    def get_stat(self, stat_name, recursion_break=False):
        val = self.get_base(stat_name)
        for item in self.inventory:
            v = item.get_stat(stat_name)
            if isinstance(v, StatValue):
                v = v.value()
            val = val.add(v)
        for mod in self.global_mods():
            if isinstance(mod, DependentModifier):
                if recursion_break:
                    continue
                mod = mod(self)

            val = mod(stat_name, val)
        if stat_name == Resistances:
            val = val.bound(self.get_stat(MaxResistances).value())
        return val

    def stat_changed(self, stat_name):
        a = self.get_stat(stat_name)
        if stat_name in self.DEFAULT_BASE_STATS:
            if self.get_stat(stat_name).value() == self.DEFAULT_BASE_STATS[stat_name]:
                return False
        if stat_name in self.class_specific_stats:
            if stat_name not in self.classname.class_specific_stats:
                return False
        if isinstance(stat_name, SpecialisedStatName):
            return self.get_stat(stat_name).value() != self.get_stat(stat_name.base).value()
        return self.get_stat(stat_name).value() != stat_name.neutral_value.value()

    def __str__(self):
        return '\n\n'.join(['\n'.join([f'{stat}: {self.get_stat(stat).value():.{stat.prec}f}' for stat in block if self.stat_changed(stat)]) for block in self.blocks])

    def active_skill_damage(self, skill):
        player_dmg = self.get_stat(Damage)
        extra_lvl = self.get_stat(ExtraProjectileSkillLevel).value()
        dmg_mult = skill.get_damage_mult_for_level(extra_lvl)

        flat = self.get_stat(Damage).flat
        converted_value = skill.conversion(flat)
        for mod in skill.modifiers:
            if isinstance(mod, DamageGain):
                converted_value = mod(converted_value)
        converted = DamageStatValue(converted_value, player_dmg.increase, player_dmg.more)
        for mod in skill.modifiers:
            if not isinstance(mod, DamageGain):
                converted = mod(Damage, converted)
        return round(converted.value() * dmg_mult)

    def damageEV(self, dmg, crit):
        if LightningRodModifier() in self.global_mods() and not crit:
            return dmg['Physical'].mean() + dmg['Lightning'].lucky_mean() + dmg['Fire'].mean() + dmg['Cold'].mean() + dmg['Chaos'].mean()
        if crit:
            return dmg.sum().mean() * (1 + self.get_stat(CritBonus).value().value)
        return dmg.sum().mean()

    def modified_dps_stats(self, skill):
        as_stat = self.get_stat(AttackSpeed)
        cc = self.get_stat(CritChance)
        for mod in skill.modifiers:
            if isinstance(mod, Modifier):
                as_stat = mod(AttackSpeed, as_stat)
                cc = mod(CritChance, cc)
        return self.active_skill_damage(skill), as_stat.more_bonus(skill.speed_mult - 1), cc

    def active_skill_dps(self, skill):
        dmg, as_, cc = self.modified_dps_stats(skill)
        c = cc.value().value
        return as_.value() * (c * self.damageEV(dmg, crit=True) + (1 - c) * self.damageEV(dmg, crit=False))

    def equip(self, item, slot=1):
        self.inventory.equip(item, ws=self.wss, slot=slot)
