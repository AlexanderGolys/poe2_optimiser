from v5.runes import *


class Item:
    def __init__(self, base_stats, implicits=[], affixes=[], quality=0, quality_class=None, max_quality=.2, sockets=0, runes=[], item_level=80, corrupted=False):
        self.base_stats = {name: StatValue(value) for name, value in base_stats.items()}
        self.implicits = implicits
        self.affixes = affixes
        self.runes = runes
        self.quality_ = quality
        self.quality_class_ = quality_class
        self.max_quality = max_quality

    def rune_mods(self):
        if isinstance(self, Weapon):
            return [r.weapon_modifier for r in self.runes]
        return [r.armour_modifier for r in self.runes]

    @property
    def quality(self):
        return self.quality_

    @quality.setter
    def quality(self, value):
        self.quality_ = round(value, 2)

    @property
    def quality_class(self):
        return self.quality_class_

    def quality_mods(self):
        if self.quality_class is None:
            return []
        return [self.quality_class(self.quality)] if self.quality > 0 else []

    def mods(self):
        return self.implicits + self.affixes + self.rune_mods() + self.quality_mods()

    def local_mods(self):
        return list(filter(lambda x: isinstance(x, Modifier) and x.local, self.mods()))

    def global_mods(self):
        return list(filter(lambda x: isinstance(x, DependentModifier) or not x.local, self.mods()))

    def get_base(self, stat_name):
        if isinstance(stat_name, SpecialisedStatName):
            return self.get_base(stat_name.base)
        if stat_name in self.base_stats:
            return deepcopy(self.base_stats[stat_name])
        return deepcopy(stat_name.neutral_value)

    def get_stat(self, stat_name):
        base = deepcopy(self.get_base(stat_name))
        for mod in self.local_mods():
            base = mod(stat_name, base)
        return base

    def __str__(self):
        return f'{self.base_stats}' + '\n' + '\n'.join([str(mod) for mod in self.local_mods()]) + '\n' + '\n'.join([str(mod) for mod in self.global_mods()])


class Weapon(Item):
    def __init__(self, base_stats, implicits=[], affixes=[], quality=0, sockets=2, runes=[], item_level=80, corrupted=False, local_mods_applied=False):
        if local_mods_applied:
            physical_damage = base_stats[Damage].flat['physical']
            physical_damage /= 1 + quality
            local_inc = 1
            local_add = Vector([0, 0])
            for mod in affixes:
                if isinstance(mod, LocalIncreaseModifier) and mod.stat_name == Damage:
                    if isinstance(mod.value, (int, float)):
                        local_inc += mod.value
                    else:
                        local_inc += mod.value[0]
                if isinstance(mod, LocalAddModifier) and mod.stat_name == Damage:
                    local_add += mod.value['physical']
            physical_damage /= local_inc
            physical_damage -= local_add
            base_stats[Damage].flat['physical'] = physical_damage

        super().__init__(base_stats, implicits, affixes, quality, quality_class=WeaponQualityModifier, max_quality=.2, sockets=sockets, runes=runes, item_level=item_level, corrupted=corrupted)


class Bow(Weapon):
    def __init__(self, dmg, attack_speed, crit_chance, implicits=[], affixes=[], quality=0, sockets=2, runes=[], item_level=80, corrupted=False, local_mods_applied=False):
        super().__init__({Damage: dmg, AttackSpeed: attack_speed, CritChance: crit_chance},
                         implicits, affixes, quality, sockets, runes, item_level, corrupted, local_mods_applied)


class Crossbow(Weapon):
    def __init__(self, dmg, attack_speed, crit_chance, reload_time, implicits=[], affixes=[], quality=0, sockets=2, runes=[], item_level=80, corrupted=False, local_mods_applied=False):
        super().__init__({Damage: dmg, AttackSpeed: attack_speed, CritChance: crit_chance, ReloadTime: reload_time},
                         implicits, affixes, quality, sockets, runes, item_level, corrupted, local_mods_applied)

class OffHand(Item):
    def __init__(self, implicits=[], affixes=[], item_level=80, corrupted=False):
        super().__init__({}, implicits, affixes, quality=0, quality_class=None, max_quality=0, sockets=0, runes=[], item_level=item_level, corrupted=corrupted)

class ArmourItem(Item):
    def __init__(self, armour=0, evasion=0, energy_shield=0, implicits=[], affixes=[], quality=0, sockets=1, runes=[], item_level=80, corrupted=False, local_mods_applied=False):
        if local_mods_applied:
            armour /= 1 + quality
            evasion /= 1 + quality
            energy_shield /= 1 + quality
            armour_inc = 1
            evasion_inc = 1
            energy_shield_inc = 1
            armour_add = 0
            evasion_add = 0
            energy_shield_add = 0
            for mod in affixes:
                if isinstance(mod, LocalIncreaseModifier):
                    if mod.stat_name == Armour:
                        armour_inc += mod.value
                    if mod.stat_name == Evasion:
                        evasion_inc += mod.value
                    if mod.stat_name == EnergyShield:
                        energy_shield_inc += mod.value
                if isinstance(mod, LocalAddModifier):
                    if mod.stat_name == Armour:
                        armour_add += mod.value
                    if mod.stat_name == Evasion:
                        evasion_add += mod.value
                    if mod.stat_name == EnergyShield:
                        energy_shield_add += mod.value
            armour /= armour_inc
            evasion /= evasion_inc
            energy_shield /= energy_shield_inc
            armour = round(armour - armour_add)
            evasion = round(evasion - evasion_add)
            energy_shield = round(energy_shield - energy_shield_add)

        super().__init__({Armour: armour, Evasion: evasion, EnergyShield: energy_shield},
                         implicits, affixes, quality, quality_class=ArmourQualityModifier, max_quality=.2, sockets=sockets, runes=runes, item_level=item_level, corrupted=corrupted)


class Boots(ArmourItem):
    pass


class Gloves(ArmourItem):
    pass


class Helmet(ArmourItem):
    pass


class BodyArmour(ArmourItem):
    pass


class Jewellery(Item):
    def __init__(self, implicits=[], affixes=[], quality=0, quality_tag=None, item_level=80, corrupted=False):
        super().__init__({}, implicits, affixes, quality, quality_class=quality_tag, sockets=0, runes=[], item_level=item_level, corrupted=corrupted)


class ManaFlask(Item):
    def __init__(self, mana_recovery, time, charges, cost, affixes=[], implicits=[], quality=0, item_level=80, corrupted=False, local_mods_applied=False):
        if local_mods_applied:
            mana_recovery /= 1 + quality
            for mod in affixes:
                if isinstance(mod, LocalIncreaseModifier) and mod.stat_name == ManaRecoveryFromFlask:
                    mana_recovery /= 1 + mod.value
        super().__init__({ManaRecoveryFromFlask: mana_recovery, ManaFlaskRecoveryRate: 1 / time, ManaFlaskCharges: charges, ManaFlaskChargesCost: cost, ManaFlaskChargesPerSecond: 0},
                         affixes=affixes, implicits=implicits, quality=quality, quality_class=None, sockets=0, runes=[], item_level=item_level, corrupted=corrupted)


class LifeFlask(Item):
    def __init__(self, life_recovery, time, charges, cost, affixes=[], implicits=[], quality=0, item_level=80, corrupted=False, local_mods_applied=False):
        if local_mods_applied:
            life_recovery /= 1 + quality
            for mod in affixes:
                if isinstance(mod, LocalIncreaseModifier) and mod.stat_name == LifeRecoveryFromFlask:
                    life_recovery /= 1 + mod.value
        super().__init__({LifeRecoveryFromFlask: life_recovery, LifeFlaskRecoveryRate: 1 / time, LifeFlaskCharges: charges, LifeFlaskChargesCost: cost, LifeFlaskChargesRecoveryPerSecond: 0},
                         affixes=affixes, implicits=implicits, quality=quality, quality_class=None, sockets=0, runes=[], item_level=item_level, corrupted=corrupted)


class Charm(Item):
    def __init__(self, duration, charges, cost, effect, affixes=[], implicits=[], quality=0, item_level=80, corrupted=False, local_mods_applied=False):
        if local_mods_applied:
            for mod in affixes:
                if isinstance(mod, LocalIncreaseModifier) and mod.stat_name == CharmDuration:
                    duration /= 1 + mod.value
        super().__init__({CharmDuration: duration, CharmCharges: charges, CharmCost: cost},
                         affixes=affixes, implicits=implicits, quality=quality, quality_class=None, sockets=0, runes=[], item_level=item_level, corrupted=corrupted)
        self.effect = effect


class AmuletOrRing(Jewellery):

    @property
    def quality_class(self):
        return self.quality_class_

    @quality_class.setter
    def quality_class(self, tag):
        self.quality_class_ = tag
        for mod in self.affixes:
            mod.set_magnitude_from_quality(self.quality, tag)

    @property
    def quality(self):
        return self.quality_

    @quality.setter
    def quality(self, value):
        self.quality_ = round(value, 2)
        for mod in self.affixes:
            mod.set_magnitude_from_quality(self.quality_, self.quality_class_)

    def quality_mods(self):
        return []

    def reverse_local_mods(self):
        for mod in self.affixes:
            mod.rebase_applied_magnitude()


class AllocatedPassiveSkill(Modifier):
    def __init__(self, passive_skill):
        self.passive_skill = passive_skill

        def act(name, value):
            for mod in self.passive_skill.modifiers:
                value = mod(name, value)
            return value

        super().__init__(act, False)

    def __str__(self):
        return f'Allocated Passive Skill: {self.passive_skill}'


class Amulet(AmuletOrRing):
    def __init__(self, implicits, affixes=[], quality=0, quality_tag=None, item_level=80, corrupted=False, allocated_passive=None):
        super().__init__(implicits, affixes, quality, quality_tag, item_level, corrupted)
        if allocated_passive is not None:
            self.implicits.append(AllocatedPassiveSkill(allocated_passive))

    @property
    def allocated_passive(self):
        for mod in self.implicits:
            if isinstance(mod, AllocatedPassiveSkill):
                return mod.passive_skill
        return None

    @allocated_passive.setter
    def allocated_passive(self, passive_skill):
        for mod in self.implicits:
            if isinstance(mod, AllocatedPassiveSkill):
                mod.passive_skill = passive_skill
                return
        self.implicits.append(AllocatedPassiveSkill(passive_skill))


class Ring(AmuletOrRing):
    pass


class Belt(Jewellery):
    def __init__(self, implicits, affixes=[], item_level=80, corrupted=False):
        super().__init__(implicits, affixes, item_level=item_level, corrupted=corrupted)


class Inventory:
    def __init__(self, boots=None, gloves=None, helmet=None, body=None,
                 weapon1=None, weapon2=None, offhand=None, offhand2=None,
                 amulet=None, ring1=None, ring2=None, belt=None, charm1=None,
                 charm2=None, charm3=None, flask_life=None, flask_mana=None):
        self.boots = boots
        self.gloves = gloves
        self.helmet = helmet
        self.body = body
        self.weapon1 = weapon1
        self.weapon2 = weapon2
        self.offhand1 = offhand
        self.offhand2 = offhand2
        self.amulet = amulet
        self.ring1 = ring1
        self.ring2 = ring2
        self.belt = belt
        self.charm1 = charm1
        self.charm2 = charm2
        self.charm3 = charm3
        self.flask_life = flask_life
        self.flask_mana = flask_mana

    def items(self, ws=1):
        s = {'Boots': self.boots,
             'Gloves': self.gloves,
             'Helmet': self.helmet,
             'Body Armour': self.body,
             'Weapon': self.weapon1,
             'Off-hand': self.offhand1,
             'Amulet': self.amulet,
             'Ring 1': self.ring1,
             'Ring 2': self.ring2,
             'Belt': self.belt,
             'Charm': self.charm1,
             'Charm 2': self.charm2,
             'Charm 3': self.charm3,
             'Life Flask': self.flask_life,
             'Mana Flask': self.flask_mana}
        if ws == 2:
            s['Weapon'] = self.weapon2
            s['Off-hand'] = self.offhand2
        return s

    def global_mods(self, ws=1):
        return sum([item.global_mods() for item in self.items(ws).values() if item is not None], [])

    def __getitem__(self, item):
        return self.items(1)[item]

    def __setitem__(self, key, value, slot=1):
        if key == 'Boots':
            self.boots = value
        elif key == 'Gloves':
            self.gloves = value
        elif key == 'Helmet':
            self.helmet = value
        elif key == 'Body Armour':
            self.body = value
        elif key == 'Weapon' and slot == 1:
            self.weapon1 = value
        elif key == 'Weapon 2' or key == 'Weapon' and slot == 2:
            self.weapon2 = value
        elif key == 'Amulet':
            self.amulet = value
        elif key == 'Ring 1' or key == 'Ring' and slot == 1:
            self.ring1 = value
        elif key == 'Ring 2' or key == 'Ring' and slot == 2:
            self.ring2 = value
        elif key == 'Belt':
            self.belt = value
        elif key == 'Charm 1' or key == 'Charm' and slot == 1:
            self.charm1 = value
        elif key == 'Charm 2' or key == 'Charm' and slot == 2:
            self.charm2 = value
        elif key == 'Charm 3' or key == 'Charm' and slot == 3:
            self.charm3 = value
        elif key == 'Life Flask':
            self.flask_life = value
        elif key == 'Mana Flask':
            self.flask_mana = value
        elif key == 'Off-hand' and slot == 1 or key == 'Off-hand 1':
            self.offhand1 = value
        elif key == 'Off-hand' and slot == 2 or key == 'Off-hand 2':
            self.offhand2 = value

    def __iter__(self):
        return iter([item for item in self.items(1).values() if item is not None])

    def movement_speed_penalty(self):
        if self.body is None:
            return 0
        if self.body.get_stat(Armour).value() == 0:
            return .03
        if self.body.get_stat(Evasion).value() == 0 and self.body.get_stat(EnergyShield).value() == 0:
            return .05
        return 0.04

    def equip(self, item, slot=1, ws=1):
        if isinstance(item, Weapon):
            if ws == 1:
                self.weapon1 = item
            else:
                self.weapon2 = item
        elif isinstance(item, BodyArmour):
            self.body = item
        elif isinstance(item, Helmet):
            self.helmet = item
        elif isinstance(item, Gloves):
            self.gloves = item
        elif isinstance(item, Boots):
            self.boots = item
        elif isinstance(item, Amulet):
            self.amulet = item
        elif isinstance(item, Ring):
            if slot == 1:
                self.ring1 = item
            else:
                self.ring2 = item
        elif isinstance(item, Belt):
            self.belt = item
        elif isinstance(item, Charm):
            if slot == 1:
                self.charm1 = item
            elif slot == 2:
                self.charm2 = item
            else:
                self.charm3 = item
        elif isinstance(item, LifeFlask):
            self.flask_life = item
        elif isinstance(item, ManaFlask):
            self.flask_mana = item
        elif isinstance(item, OffHand):
            if ws == 1:
                self.offhand1 = item
            else:
                self.offhand2 = item


# Item Class: Crossbows
# Rarity: Rare
# Glyph Core
# Bombard Crossbow
# --------
# Physical Damage: 12-47
# Lightning Damage: 2-49 (augmented)
# Critical Hit Chance: 6.45% (augmented)
# Attacks per Second: 1.65
# Reload Time: 0.75
# --------
# Requirements:
# Level: 33
# Str: 43
# Dex: 43
# --------
# Item Level: 35
# --------
# Grenade Skills Fire an additional Projectile (implicit)
# --------
# Adds 2 to 49 Lightning Damage
# +121 to Accuracy Rating
# +1.45% to Critical Hit Chance
# +17% to Critical Damage Bonus
#
#
#
# Item Class: Crossbows
# Rarity: Rare
# Beast Core
# Alloy Crossbow
# --------
# Quality: +20% (augmented)
# Physical Damage: 25-76 (augmented)
# Elemental Damage: 14-22 (augmented), 3-43 (augmented)
# Critical Hit Chance: 7.43% (augmented)
# Attacks per Second: 1.89 (augmented)
# Reload Time: 0.70 (augmented)
# --------
# Requirements:
# Level: 26
# Str: 34
# Dex: 34
# --------
# Sockets: S S
# --------
# Item Level: 32
# --------
# Adds 14 to 22 Fire Damage (rune)
# --------
# Adds 10 to 21 Physical Damage
# Adds 3 to 43 Lightning Damage
# +52 to Accuracy Rating
# +2.43% to Critical Hit Chance
# +11% to Critical Damage Bonus
# 11% increased Attack Speed


# Item Class: Body Armours
# Rarity: Rare
# Loath Ward
# Hexer's Robe
# --------
# Quality: +20% (augmented)
# Energy Shield: 150 (augmented)
# --------
# Requirements:
# Level: 23
# Int: 24
# --------
# Sockets: S S S
# --------
# Item Level: 29
# --------
# 60% increased Armour, Evasion and Energy Shield (rune)
# --------
# +26 to maximum Energy Shield
# 19% increased Energy Shield
# +7 to maximum Life
# +18% to Cold Resistance
# 3.7 Life Regeneration per second
# +75 to Stun Threshold
# --------
# Corrupted
