from v5.comparators import *

boots = Boots(energy_shield=80, quality=0, item_level=81, runes=[], sockets=0, corrupted=True, local_mods_applied=True,
              affixes=[IncreaseModifier(MovementSpeed, .2),
                       AddModifier(Strength, 14),
                       AddModifier(Intelligence, 20),
                       AddModifier(Dexterity, 15),
                       LocalAddModifier(EnergyShield, 46)],
              implicits=[AddColdResistance(.24)])

belt = Belt(implicits=[AddModifier(Dexterity, 12), IncreaseModifier(ManaRecoveryFromFlask, .2)],
            affixes=[AddModifier(Life, 24),
                     AddModifier(Mana, 18),
                     AddModifier(LifeRegenerationRate, 3.2),
                     AddModifier(StunThreshold, 22),
                     MultiIncreaseModifier([ManaFlaskChargesGain, LifeFlaskChargesGain], .14),
                     AddModifier(ThornsDamage, DamageTypeVector(Physical=Vector([5, 6])))],
            corrupted=True)
gloves = Gloves(armour=18, quality=0, item_level=3, runes=[BodyRune], sockets=1, local_mods_applied=True,
                affixes=[LocalIncreaseModifier(Armour, .19),
                         AddModifier(Damage, DamageTypeVector(DMG0_LST, Fire=Vector([1, 4]))),
                         AddModifier(Accuracy, 11),
                         AddModifier(Rarity, .08),
                         IncreaseModifier(AttackSpeed, .07),
                         AddModifier(Strength, 7)])

body_armour = BodyArmour(energy_shield=150, quality=.2, item_level=20, runes=[], sockets=0, corrupted=True, local_mods_applied=True,
                         affixes=[AddLife(7),
                                  AddColdResistance(.18),
                                  AddModifier(StunThreshold, 75),
                                  AddModifier(LifeRegenerationRate, 3.7)])

helmet = Helmet(armour=23, evasion=18, item_level=3, runes=[BodyRune], sockets=1, local_mods_applied=True,
                affixes=[AddModifier(Accuracy, 15),
                         AddModifier(Life, 11),
                         AddModifier(Mana, 12),
                         AddModifier(Rarity, .11),
                         AddModifier(Strength, 8),
                         AddModifier(Dexterity, 5)])

ring1 = Ring(implicits=[AddFireResistance(.27)],
             affixes=[DamageIncreaseModifier(lightning=.05),
                      AddMana(12),
                      AddRarity(.09),
                      AddDexterity(7),
                      AddIntelligence(14),
                      AddModifier(LifeRegenerationRate, 5.3)])

ring2 = Ring(implicits=[AddLightningResistance(.3)],
             affixes=[AddModifier(Damage, DamageTypeVector(DMG0_LST, Fire=Vector([11, 17]))),
                      AddMana(62),
                      AddRarity(.09),
                      AddFireResistance(.15),
                      AddColdResistance(.14),
                      AddLightningResistance(.19)])

blur = PassiveSkill([AddDexterity(10), IncreaseModifier(Evasion, .2), IncreaseModifier(MovementSpeed, .04)])
amulet = Amulet(implicits=[AddDexterity(15)],
                affixes=[IncreaseModifier(Armour, .13),
                         AddModifier(EnergyShield, 20),
                         AddLife(57),
                         AddFireResistance(.13),
                         AddStrength(9),
                         AddIntelligence(12),
                         AddModifier(LifeRegenerationRate, 4.4)],
                allocated_passive=blur)

crossbow = Crossbow(DamageTypeVector(DMG0_LST, Physical=Vector([25, 97])), 1.84, 0.05, 0.7,
                    quality=.0, item_level=81, runes=[DesertRune, DesertRune], sockets=2, corrupted=True,
                    affixes=[AddStrength(13)])

crossbow2 = Crossbow(DamageTypeVector(DMG0_LST, Physical=Vector([21, 53]), Cold=Vector([13, 16])), 1.6, 0.0763, 0.7,
                     quality=.2, item_level=81, runes=[DesertRune, DesertRune], sockets=2, corrupted=True,
                     affixes=[AddModifier(CritBonus, .13), AddModifier(Accuracy, 63), AddModifier(LifePerKill, 2)])

crossbow3 = Crossbow(DamageTypeVector(DMG0_LST, Physical=Vector([21, 63]), Lightning=Vector([3, 43])), 1.89, 0.0743, 0.7,
                     quality=.2, item_level=81, runes=[DesertRune, DesertRune], sockets=2, corrupted=True,
                     affixes=[AddModifier(CritBonus, .11), AddModifier(Accuracy, 52)])

life_flask = LifeFlask(517, 4, 75, 10)
mana_flask = ManaFlask(252, 3.5, 75, 10, affixes=[AddModifier(ManaFlaskChargesPerSecond, .15)])

inventory = Inventory(boots=boots, belt=belt, gloves=gloves, body=body_armour, helmet=helmet, ring1=ring1, ring2=ring2, amulet=amulet,
                      weapon1=crossbow3, flask_life=life_flask, flask_mana=mana_flask)

base_stats = {Resistances: ResistanceVector([-.1, -.1, -.1, 0])}

forced_quest_mods = [
    AddResistance('Cold', .1),
    AddModifier(Spirit, 30),
    AddModifier(Life, 20)]

jewel1 = Jewel(affixes=[AllDamageIncreaseModifier(.15), IncreaseModifier(ManaRecoveryFromFlask, .13), IncreaseAilmentMagnitude(.07), IncreaseModifier(CharmChargesGain, .11)])

passives = PassiveSkillSet(jewels=[jewel1], full=[
    IncreasedDamagePassive(.1),
    IncreasedDamagePassive(.1),
    IncreasedDamagePassive(.1),
    IncreasedDamagePassive(.1),
    IncreaseAttackSpeedPassive(.03),

    IncreaseAttackSpeedPassive(.03),
    IncreaseAttackSpeedPassive(.03),
    PassiveSkill([AllDamageIncreaseModifier(.15), AddStrength(5), AddDexterity(5)]),
    PassiveSkill([IncreaseModifier(Armour, .12), IncreaseModifier(Evasion, .12)]),
    PassiveSkill([IncreaseModifier(Armour, .2), IncreaseModifier(Evasion, .2), IncreaseModifier(StunThreshold, .2)]),

    SinglePassiveSkill(IncreaseModifier(CooldownRecoveryRate, .05)),
    PassiveSkill([IncreaseModifier(AreaOfEffect, .1), IncreaseModifier(CooldownRecoveryRate, .1)]),
    SinglePassiveSkill(IncreaseModifier(CooldownRecoveryRate, .05)),
    IncreasedDamagePassive(.1),
    IncreasedDamagePassive(.1),

    IncreasedDamagePassive(.15),
    StrengthPassive(),
    DexterityPassive(),
    StrengthPassive(),
    DexterityPassive(),

    IncreasedDamagePassive(.1),
    SinglePassiveSkill(IncreaseModifier(GranadeDamage, .12)),
    SinglePassiveSkill(IncreaseModifier(GranadeCooldownRecoveryRate, .15)),
    SinglePassiveSkill(IncreaseModifier(GranadeCooldownRecoveryRate, .15)),
    SinglePassiveSkill(IncreaseModifier(GranadeCooldownRecoveryRate, .15)),

    SinglePassiveSkill(AddModifier(ExtraCooldownUses, 1)),
    SinglePassiveSkill(IncreaseModifier(GranadeAreaOfEffect, .12)),
    PassiveSkill([IncreaseModifier(FuseDuration, .5), AddModifier(GranadeExtraProjectiles, 1)]),
    SinglePassiveSkill(IncreaseModifier(GranadeAreaOfEffect, .12)),
    StrengthPassive(),

    StrengthPassive(),
    StrengthPassive(),
    SinglePassiveSkill(IncreaseModifier(GranadeDamage, .12)),
    SinglePassiveSkill(IncreaseModifier(GranadeDamage, .12)),
    SinglePassiveSkill(IncreaseModifier(FuseDuration, -.25)),
])

base_skill = ProjectileSkill('Shot', DamageConversion(), 1.82, 1, 0, 9, 0, [])

player = Player(Mercenary, 32, inventory=inventory, passive_skills=passives, quest_mods_chosen=[], quest_mods_forced=forced_quest_mods, base_stats=base_stats)

if __name__ == '__main__':
    print(player)
    print(player.active_skill_damage(base_skill))
    print(player.active_skill_dps(base_skill))
    print('----')
    print(Comparator(player).compare_items(crossbow, crossbow2))
    print('----')
    print(Comparator(player).compare_items(crossbow, crossbow3))

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
