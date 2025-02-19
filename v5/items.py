from v5.runes import *
from v5.modifiers import *

NORMAL_ITEM = 'Normal'
MAGIC_ITEM = 'Magic'
RARE_ITEM = 'Rare'
UNIQUE_ITEM = 'Unique'


class Item:
    def __init__(self, base_stats={}, implicit=None, affixes=[], quality=0, quality_class=DEFAULT_QUALITY, max_quality=20, sockets=0, runes=[], item_level=82, corrupted=False, corrupted_mod=None,
                 rarity=RARE_ITEM):
        self.base_stats = {name: StatValue(value) for name, value in base_stats.items()}
        self.implicit_mod = implicit
        self.corrupted_mod = corrupted_mod
        self.rarity = rarity
        self.affixes = affixes
        self.runes = runes
        self.quality_ = quality
        self.quality_class_ = quality_class
        self.max_quality = max_quality
        self.item_type_name = 'Unknown item type'
        self.no_sockets = max(sockets, len(runes))
        self.item_level = item_level
        self.corrupted = corrupted
        self.corrupted_mod = corrupted_mod

    def rune_mods(self):
        if isinstance(self, Weapon):
            return [r.weapon_modifier for r in self.runes]
        return [r.armour_modifier for r in self.runes]

    @property
    def quality(self):
        return self.quality_

    @quality.setter
    def quality(self, value):
        self.quality_ = int(value)

    @property
    def quality_class(self):
        return self.quality_class_

    def mods(self):
        implicits = [self.implicit_mod] if self.implicit_mod is not None else []
        corrupted = [self.corrupted_mod] if self.corrupted_mod is not None else []
        return corrupted + implicits + self.affixes + self.rune_mods()

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

    def quality_str(self, show_zero=False):
        if self.quality == 0 and not show_zero:
            return ''
        if self.quality_class is None:
            return f'Quality: {self.quality}%\n'
        return f'{self.quality_class}: {self.quality}%\n'

    def header_str(self):
        s = f'{self.item_type_name} (item level {self.item_level}, {self.rarity})\n'
        if self.corrupted:
            s += 'Corrupted\n'
        return s + self.quality_str()

    def __str__(self):
        s = self.header_str()
        s += f'{self.base_stats}\n'
        if self.corrupted_mod is not None:
            s += f'[corruption]\t{self.corrupted_mod}\t\n------------------\n'
        if self.implicit_mod is not None:
            s += f'[implicit]\t{self.implicit_mod}\n------------------\n'
        for mod in self.rune_mods():
            s += f'[rune]\t{mod}\n'
        if self.runes:
            s += '------------------\n'
        for mod in self.affixes:
            s += f'{mod}\n'
        if self.affixes:
            s += '------------------\n\n'
        return s

    def rebase_base_float_stat(self, stat_name, value, quality_applied=False):
        if quality_applied:
            value /= 1 + self.quality / 100
        inc = 1
        for mod in self.local_mods():
            if isinstance(mod, LocalIncreaseModifier) and mod.stat_name == stat_name:
                inc += mod.value
        value /= inc
        for mod in self.local_mods():
            if isinstance(mod, LocalAddModifier) and mod.stat_name == stat_name:
                value -= mod.value
        return value


class Weapon(Item):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, max_quality=20, quality_class=DEFAULT_QUALITY)
        self.item_type_name = 'Weapon'

    def rebase_damage(self, dmg_):
        dmg = deepcopy(dmg_)
        physical_inc = 1

        for rune_mod in self.rune_mods():
            if isinstance(rune_mod, AddModifier) and rune_mod.stat_name == Damage:
                dmg -= rune_mod.value
            if isinstance(rune_mod, LocalPhysicalDamageIncrease):
                physical_inc += rune_mod.value

        dmg *= Vector([1 / (1 + self.quality / 100), 1, 1, 1, 1])

        for mod in self.local_mods():
            if isinstance(mod, LocalPhysicalDamageIncrease):
                physical_inc += mod.value

        dmg['Physical'] /= physical_inc

        for mod in self.local_mods():
            if isinstance(mod, LocalAddModifier) and mod.stat_name == Damage:
                dmg['Physical'] -= mod.value
        return dmg


class Bow(Weapon):
    def __init__(self, dmg, attack_speed, crit_chance, local_applied=True, **kwargs):
        super().__init__(base_stats={Damage: dmg, AttackSpeed: attack_speed, CritChance: crit_chance}, **kwargs)
        if local_applied:
            self.base_stats[Damage] = DamageStatValue(self.rebase_damage(self.base_stats[Damage].value()))
            self.base_stats[AttackSpeed] = StatValue(self.rebase_base_float_stat(AttackSpeed, self.base_stats[AttackSpeed].value()))
            self.base_stats[CritChance] = StatValue(self.rebase_base_float_stat(CritChance, self.base_stats[CritChance].value()))
        self.item_type_name = 'Bow'


class Crossbow(Weapon):
    def __init__(self, dmg, attack_speed, crit_chance, reload_time, local_applied=True, **kwargs):
        super().__init__(base_stats={Damage: dmg, AttackSpeed: attack_speed, CritChance: crit_chance, ReloadTime: reload_time}, **kwargs)
        if local_applied:
            self.base_stats[Damage] = DamageStatValue(self.rebase_damage(self.base_stats[Damage].value()))
            self.base_stats[AttackSpeed] = StatValue(self.rebase_base_float_stat(AttackSpeed, self.base_stats[AttackSpeed].value()))
            self.base_stats[CritChance] = StatValue(self.rebase_base_float_stat(CritChance, self.base_stats[CritChance].value()))
            self.base_stats[ReloadTime] = StatValue(self.rebase_base_float_stat(ReloadTime, self.base_stats[ReloadTime].value()))
        self.item_type_name = 'Crossbow'


class OffHand(Item):
    def __init__(self, **kwargs):
        super().__init__(base_stats={}, quality=0, quality_class=None, max_quality=0, sockets=0, runes=[], **kwargs)
        self.item_type_name = 'Off-hand'


class ArmourItem(Item):
    def __init__(self, armour=0, evasion=0, energy_shield=0, local_applied=True, **kwargs):
        super().__init__(base_stats={Armour: armour, Evasion: evasion, EnergyShield: energy_shield}, max_quality=20, quality_class=DEFAULT_QUALITY, **kwargs)
        if local_applied:
            self.base_stats[Armour] = IntStatValue(self.rebase_base_float_stat(Armour, armour, True))
            self.base_stats[Evasion] = IntStatValue(self.rebase_base_float_stat(Evasion, evasion, True))
            self.base_stats[EnergyShield] = IntStatValue(self.rebase_base_float_stat(EnergyShield, energy_shield, True))
        self.item_type_name = 'Armour Type Item'


class Boots(ArmourItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_type_name = 'Boots'


class Gloves(ArmourItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_type_name = 'Gloves'


class Helmet(ArmourItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_type_name = 'Helmet'


class BodyArmour(ArmourItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_type_name = 'Body Armour'


class Jewellery(Item):
    def __init__(self, **kwargs):
        super().__init__(base_stats={}, sockets=0, runes=[], **kwargs)
        self.item_type_name = 'Jewellery Type Item'


class AmuletOrRing(Jewellery):
    def __init__(self, local_applied=True, **kwargs):
        super().__init__(**kwargs)
        for mod in self.affixes:
            if isinstance(mod, NumericalModifier) and self.quality_class_ in mod.applicable_qualities:
                if local_applied:
                    mod.magnitude = self.quality / 100 + 1
                else:
                    mod.magnify_to(self.quality / 100 + 1)
        self.item_type_name = 'Amulet or Ring'


class ManaFlask(Item):
    def __init__(self, mana_recovery, time, charges, cost, local_applied=True, **kwargs):
        super().__init__({ManaRecoveryFromFlask: mana_recovery, ManaFlaskRecoveryRate: 1 / time, ManaFlaskCharges: charges, ManaFlaskChargesCost: cost, ManaFlaskChargesPerSecond: 0},
                         sockets=0, runes=[], quality_class=DEFAULT_QUALITY, max_quality=20, **kwargs)
        if local_applied:
            self.base_stats[ManaRecoveryFromFlask] = self.rebase_base_float_stat(ManaRecoveryFromFlask, mana_recovery, True)
        self.item_type_name = 'Mana Flask'


class LifeFlask(Item):
    def __init__(self, life_recovery, time, charges, cost, local_applied=True, **kwargs):
        super().__init__({LifeRecoveryFromFlask: life_recovery, LifeFlaskRecoveryRate: 1 / time, LifeFlaskCharges: charges, LifeFlaskChargesCost: cost},
                         sockets=0, runes=[], quality_class=DEFAULT_QUALITY, max_quality=20, **kwargs)
        if local_applied:
            self.base_stats[LifeRecoveryFromFlask] = self.rebase_base_float_stat(LifeRecoveryFromFlask, life_recovery, True)
        self.item_type_name = 'Life Flask'


class Charm(Item):
    def __init__(self, duration, charges, cost, effect, **kwargs):
        super().__init__({CharmDuration: duration, CharmCharges: charges, CharmCost: cost, CharmSlots: 1},
                         sockets=0, runes=[], quality_class=DEFAULT_QUALITY, max_quality=20, **kwargs)
        self.effect = effect
        self.item_type_name = 'Charm'


class AllocatedPassiveSkill(Modifier):
    def __init__(self, passive_skill, skill_name='Unknown'):
        self.passive_skill = passive_skill
        self.skill_name = skill_name
        self.local = False

        def act(name, value):
            for mod in self.passive_skill.modifiers:
                value = mod(name, value)
            return value

        super().__init__(act, False)

    def __str__(self):
        return f'Allocated Passive Skill: {self.skill_name}'


class Amulet(AmuletOrRing):
    def __init__(self, allocated_passive=None, **kwargs):
        super().__init__(**kwargs)
        self.allocated_passive = allocated_passive
        self.item_type_name = 'Amulet'

    def mods(self):
        allocated = [self.allocated_passive] if self.allocated_passive is not None else []
        return super().mods() + allocated

    def __str__(self):
        s = self.header_str()
        s += f'{self.base_stats}\n'
        if self.corrupted_mod is not None:
            s += f'[corruption]\t{self.corrupted_mod}\t\n------------------\n'
        if self.implicit_mod is not None:
            s += f'[implicit]\t{self.implicit_mod}\n------------------\n'
        if self.allocated_passive is not None:
            s += f'[allocated passive: {self.allocated_passive.skill_name}]\n{self.allocated_passive.passive_skill}\n------------------\n'
        for mod in self.affixes:
            s += f'{mod}\n'
        if self.affixes:
            s += '------------------\n\n'
        return s


class Ring(AmuletOrRing):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_type_name = 'Ring'


class Belt(Jewellery):
    def __init__(self, **kwargs):
        super().__init__(quality=0, quality_class=None, **kwargs)
        self.item_type_name = 'Belt'


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
