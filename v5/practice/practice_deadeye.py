from src.comparators import *
from src.item_parser import *

jewel1 = Jewel(affixes=[
    AllDamageIncreaseModifier(.05),
    MovementSpeedIncrease(.02),
    AllDamageIncreaseModifier(.11),
    IncreaseModifier(ManaRecoveryFromFlask, .12)])
jewel2 = Jewel(affixes=[
    MovementSpeedIncrease(.02),
    AddLightningPenetration(.08),
    AddModifier(PoisonChance, .09),
    IncreaseModifier(PoisonMagnitude, .09)])
jewel3 = Jewel(affixes=[
    AllDamageIncreaseModifier(.11),
    MovementSpeedIncrease(.02),
    IncreaseModifier(ProjectileSpeed, .08),
    AttackSpeedIncrease(.04)])
jewel4 = Jewel(affixes=[
    AllDamageIncreaseModifier(.09),
    MovementSpeedIncrease(.02),
    AllDamageIncreaseModifier(.05),
    AttackSpeedIncrease(.02)])
jewel5 = Jewel(affixes=[
    AllDamageIncreaseModifier(.12),
    MovementSpeedIncrease(.02),
    IncreaseModifier(Accuracy, .05),
    AttackSpeedIncrease(.02)])
jewel6 = Jewel(affixes=[
    AllDamageIncreaseModifier(.14),
    MovementSpeedIncrease(.02),
    IncreaseModifier(Accuracy, .07),
    IncreaseModifier(LifeRecoveryFromFlask, .07)])

full_passives = [IncreasedDamagePassive(.1),
                 IncreasedDamagePassive(.1),
                 IncreaseAttackSpeedPassive(.03),
                 IncreaseAttackSpeedPassive(.03),
                 PassiveSkill([AttackSpeedIncrease(.08), ProjectileSpeedIncrease(.08), AddDexterity(10)]),
                 SinglePassiveSkill(AilmentChanceIncrease(.1)),
                 IncreasedDamagePassive(.1),
                 PassiveSkill([AllDamageIncreaseModifier(.15), AddModifier(PierceChance, .15)]),
                 SinglePassiveSkill(FlaskRecoveryIncrease(.1)),
                 PassiveSkill([FlaskRecoveryIncrease(.1), AddModifier(ChanceToNotConsumeFlaskCharges, .1)]),

                 SinglePassiveSkill(FlaskRecoveryIncrease(.1)),
                 PassiveSkill([MovementSpeedIncrease(.04), AddDexterity(10), IncreaseModifier(Evasion, .2)]),
                 SinglePassiveSkill(MovementSpeedIncrease(.02)),
                 SinglePassiveSkill(MovementSpeedIncrease(.02)),
                 DexterityPassive(),
                 DexterityPassive(),
                 IncreasedDamagePassive(.1),
                 IncreasedDamagePassive(.1),
                 IncreasedDamagePassive(.1),

                 PassiveSkill([AllDamageIncreaseModifier(.16), IncreaseModifier(CloseRangeAccuracy, .4)]),
                 StrengthPassive(),
                 DexterityPassive(),
                 DexterityPassive(),
                 PassiveSkill([AllDamageIncreaseModifier(.08), IncreaseModifier(SkillEffectDuration, .08)]),
                 PassiveSkill([AllDamageIncreaseModifier(.08), IncreaseModifier(SkillEffectDuration, .08)]),
                 PassiveSkill([AllDamageIncreaseModifier(.16), IncreaseModifier(SkillEffectDuration, .16), IncreaseModifier(BuffDuration, .1)]),
                 StrengthPassive(),
                 DexterityPassive(),
                 IntelligencePassive(),

                 StrengthPassive(),
                 IntelligencePassive(),
                 DexterityPassive(),
                 StrengthPassive(),
                 SinglePassiveSkill(IncreaseModifier(MovementSpeedIfKilledRecently, .03)),
                 PassiveSkill([IncreaseModifier(MovementSpeedIfKilledRecently, .04), IncreaseModifier(AttackSpeedIfKilledRecently, .08)]),
                 SinglePassiveSkill(IncreaseModifier(MovementSpeedIfKilledRecently, .03)),
                 SinglePassiveSkill(ElementalDamageIncrease(.12)),
                 SinglePassiveSkill(ElementalDamageIncrease(.12)),
                 SinglePassiveSkill(ElementalDamageIncrease(.12)),

                 SinglePassiveSkill(ElementalDamageIncrease(.12)),
                 SinglePassiveSkill(ElementalDamageIncrease(.12)),
                 SinglePassiveSkill(AddElementalPenetration(.15)),
                 SinglePassiveSkill(MultiIncreaseModifier([ShockChance, IgniteChance, ElectrocuteBuildup, FreezeBuildup], .25)),
                 SinglePassiveSkill(AddLightningPenetration(.06)),
                 PassiveSkill([AddLightningPenetration(.15), IncreaseModifier(ShockChance, .3)]),
                 SinglePassiveSkill(AddLightningPenetration(.06)),
                 SinglePassiveSkill(DamageIncreaseModifier(lightning=.1)),
                 SinglePassiveSkill(DamageIncreaseModifier(lightning=.12)),
                 SinglePassiveSkill(DamageIncreaseModifier(lightning=.12)),

                 # SinglePassiveSkill(LightningRodModifier()),
                 SinglePassiveSkill(DamageIncreaseModifier(lightning=.1)),
                 DexterityPassive(),
                 DexterityPassive(),
                 IncreaseAttackSpeedPassive(.03),
                 IncreaseAttackSpeedPassive(.03),
                 SinglePassiveSkill(AddModifier(BlindChance, .08)),
                 PassiveSkill([AddModifier(BlindChance, .15), AttackSpeedIncrease(.1)]),
                 DexterityPassive(),
                 DexterityPassive(),

                 DexterityPassive(),
                 SinglePassiveSkill(IncreaseModifier(DamageAgainstElementalAilments, .12)),
                 SinglePassiveSkill(IncreaseModifier(DamageAgainstElementalAilments, .12)),
                 PassiveSkill([IncreaseModifier(DamageAgainstElementalAilments, .25), MultiIncreaseModifier([ShockDuration, IgniteDuration, ChillDuration], .15)]),
                 SinglePassiveSkill(ElementalDamageIncrease(.12)),
                 SinglePassiveSkill(ElementalDamageIncrease(.12)),
                 SinglePassiveSkill(ElementalDamageIncrease(.2)),
                 DexterityPassive(),
                 DexterityPassive(),
                 SinglePassiveSkill(IncreaseModifier(ShockMagnitude, .15)),

                 IncreasedDamagePassive(.1),
                 PassiveSkill([AllDamageIncreaseModifier(.08), MovementSpeedIncrease(.02)]),
                 PassiveSkill([AllDamageIncreaseModifier(.25), AddModifier(MaimChance, .25)]),
                 DexterityPassive(),
                 IncreaseAttackSpeedPassive(.03),
                 IncreaseAttackSpeedPassive(.03),
                 PassiveSkill([AttackSpeedIncrease(.1), MovementSpeedIncrease(.03)]),
                 DexterityPassive(),
                 IncreasedDamagePassive(.1),

                 SinglePassiveSkill(IncreaseModifier(Accuracy, .1)),
                 SinglePassiveSkill(feathered_fletching),
                 IncreasedDamagePassive(.12),
                 IncreasedDamagePassive(.12),
                 SinglePassiveSkill(AddModifier(PierceExtraTargets, 1)),
                 SinglePassiveSkill(IncreaseModifier(CritBonus, .16)),
                 SinglePassiveSkill(IncreaseModifier(CritBonus, .0)),
                 StrengthPassive(),
                 IntelligencePassive(),
                 SinglePassiveSkill(IncreaseModifier(Evasion, .15)),

                 PassiveSkill([IncreaseModifier(Evasion, .3), MovementSpeedIncrease(.03)]),
                 SinglePassiveSkill(IncreaseModifier(Evasion, .15)),
                 DexterityPassive(),
                 PassiveSkill([ElementalDamageIncrease(.08), IncreaseModifier(ShockChance, .1)]),
                 PassiveSkill([ElementalDamageIncrease(.08), IncreaseModifier(ShockChance, .1)]),
                 PassiveSkill([ElementalDamageIncrease(.08), IncreaseModifier(ShockChance, .1)]),
                 SinglePassiveSkill(IncreaseModifier(DamageAgainstElementalAilments, .15)),
                 SinglePassiveSkill(AddLightningPenetration(.06)),
                 SinglePassiveSkill(AddLightningPenetration(.06)),
                 SinglePassiveSkill(AddLightningPenetration(.06)),

                 PassiveSkill([AddLightningPenetration(.15), AddDexterity(10)]),

                 ]

wss1passives = [SinglePassiveSkill(DamageIncreaseModifier(lightning=.1)),
                SinglePassiveSkill(DamageIncreaseModifier(lightning=.1)),
                SinglePassiveSkill(DamageIncreaseModifier(lightning=.1)),
                SinglePassiveSkill(IncreaseModifier(ShockChance, .15)),
                SinglePassiveSkill(IncreaseModifier(ShockChance, .0)),

                SinglePassiveSkill(IncreaseModifier(FarAwayDamage, .12)),
                SinglePassiveSkill(IncreaseModifier(FarAwayDamage, .12)),
                PassiveSkill([IncreaseModifier(FarAwayDamage, .25), IncreaseModifier(FarAwayCritChance, .25)]),
                ]

passives2_full = full_passives + [SinglePassiveSkill(LightningRodModifier())]

wss2passives = []

asc_passives = [IncreaseAttackSpeedPassive(.04),
                SinglePassiveSkill(ProjectileSpeedIncrease(.1)),
                SinglePassiveSkill(MoreModifier(FarAwayDamage, .2)),
                SinglePassiveSkill(IncreaseModifier(Accuracy, .12)),
                # PassiveSkill([MovementSpeedIncrease(.1), AttackSpeedIncrease(.3), IncreaseModifier(Evasion, 1.5)]),
                ]

passives = PassiveSkillSet(jewels=[jewel1, jewel2, jewel3, jewel4, jewel5, jewel6],
                           full=full_passives, ws1=wss1passives, ws2=[], ascendancy=asc_passives)
passives2 = PassiveSkillSet(jewels=[jewel1, jewel2, jewel3, jewel4, jewel5, jewel6], full=passives2_full, ws1=wss1passives, ws2=[], ascendancy=asc_passives)

gem1 = SkillGem(DamageGain('Lightning', .25), MoreModifier(Damage, Vector([0, 0, -.5, -.5, 0])))
gem2 = SkillGem(MoreModifier(AttackSpeed, .25))
gem3 = SkillGem(MoreModifier(Damage, Vector([0, .25, .25, .25, 0])))
gem4 = SkillGem(AddModifier(ExtraProjectileSkillLevel, 1))
gem5 = SkillGem(MoreModifier(Damage, Vector([0, .25, .25, .25, 0])))
gem6 = SkillGem(MoreModifier(Damage, Vector([Vector([0, .3]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0])])))

base_skill = ActiveSkill('Shot', DamageConversion(), 3.61, 1, 0, 20, 0, [])

lightning_arrow = ActiveSkill('Lightning Arrow', DamageConversion('Physical', 'Lightning', .4), 2.52, .9, 0, 19, 0, gems=[gem1, gem2, gem3, gem4],
                              dmg_mult_per_new_level=[.13, .13, .14, .15, .15])

belt = Belt(implicit=IncreaseModifier(CharmDuration, .15),
            affixes=[AddModifier(Armour, 41),
                     IncreaseModifier(ManaFlaskRecoveryRate, .36),
                     AddFireResistance(.38),
                     AddColdResistance(.3),
                     AddChaosResistance(.23),
                     AddModifier(ThornsDamage, DamageTypeVector(Physical=Vector([20, 29])))])

body_armour = BodyArmour(evasion=1140, quality=0, item_level=20, runes=[StormRune, GlacialRune], sockets=2, corrupted=True,
                         affixes=[AddSpirit(41),
                                  AddFireResistance(.34),
                                  AddLightningResistance(.22),
                                  AddChaosResistance(.18),
                                  AddModifier(ThornsDamage, DamageTypeVector(Physical=Vector([8, 13])))])

wild_storm = PassiveSkill([MoreModifier(Damage, Vector([Vector([0, 0]), Vector([0, .15]), Vector([0, .0]), Vector([0, .0]), Vector([0, 0])]))])

amulet = Amulet(implicit=AddModifier(LifeRegenerationRate, 2),
                affixes=[IncreaseModifier(Evasion, .37),
                         AddLife(24),
                         AddRarity(.49),
                         AddModifier(ExtraProjectileSkillLevel, 3),
                         AddAllAttributes(22),
                         AddFireResistance(.34)],
                allocated_passive=AllocatedPassiveSkill(wild_storm, 'Wild Storm'))

bow = Bow(DamageTypeVector(DMG0_LST, Physical=Vector([96, 180]), Lightning=Vector([10, 228])), round(1.2 * 1.12, 6), 0.05,
          quality=.0, item_level=81, runes=[], sockets=2,
          implicit=AddModifier(ExtraProjectiles, 1),
          affixes=[AddAccuracy(117), AddModifier(LifePerKill, 76)])

quiver = OffHand(implicit=AttackSpeedIncrease(.07),
                 affixes=[AddFireDamage(13, 25),
                          AddLightningDamage(3, 71),
                          ProjectileSpeedIncrease(.4),
                          IncreaseModifier(CritBonus, .1),
                          AddDexterity(27),
                          AddModifier(PierceChance, .26)])

life_flask = LifeFlask(1910, 3, 75, 10, affixes=[IncreaseModifier(LifeFlaskChargesGain, .51)])
mana_flask = ManaFlask(618, 3, 75, 10, affixes=[AddModifier(ManaFlaskChargesPerSecond, .2)])
charm = Charm(3.8, 99, 80, 'Immune to freeze')

hand_of_wisdom = Gloves(energy_shield=23, evasion=60, quality=0, item_level=82, runes=[GlacialRune], sockets=1, corrupted=True,
                        affixes=[widom_int, wisdom_dex,
                                 AddDexterity(20), AddIntelligence(19)])

ring2 = Ring(implicit=AddMana(29),
             affixes=[AddLightningDamage(1, 66),
                      AddPhysicalDamage(2, 5),
                      DamageIncreaseModifier(cold=.19),
                      AddDexterity(22),
                      AddIntelligence(31),
                      IncreasedManaRegen(.27)])

ring3 = Ring(
    affixes=[AddLightningDamage(1, 81),
             AddLife(34),
             AddMana(160),
             AddDexterity(14),
             AddIntelligence(33),
             IncreasedManaRegen(.27)])

boots = Boots(evasion=109, energy_shield=42, quality=0, item_level=82, runes=[], sockets=1, corrupted=False,
              affixes=[IncreaseModifier(MovementSpeed, .35),
                       AddLife(61),
                       AddMana(120),
                       AddDexterity(30),
                       AddFireResistance(.44),
                       AddModifier(StunThreshold, 12)])

helmet = Helmet(evasion=146, energy_shield=55, quality=0, item_level=82, runes=[GlacialRune], sockets=1, corrupted=False,
                affixes=[AddLife(172),
                         AddMana(177),
                         AddRarity(.26),
                         AddDexterity(19),
                         AddIntelligence(32),
                         AddLightningResistance(.34)])

# with open('items_data/ring1.txt') as f:
#     parsed = f.read()
#     parser = ItemParser(parsed)
#     ring1 = parser.parse_item()

inventory = Inventory(boots=boots, belt=belt, gloves=hand_of_wisdom, body=body_armour, helmet=helmet,
                      ring1=ring3, ring2=ring3, weapon1=bow,
                      amulet=amulet,
                      flask_life=life_flask, flask_mana=mana_flask, charm1=charm, offhand=quiver)

base_stats = {Resistances: ResistanceVector([-.6, -.6, -.6, 0])}
quest_mods_chosen = [IncreaseModifier(ManaRecoveryFromFlask, .15), IncreasedManaRegen(.25), IncreaseModifier(LifeRecoveryFromFlask, .15), AddChaosResistance(.1)]
player = Player(Ranger, 90, inventory=inventory, passive_skills=passives, quest_mods_chosen=quest_mods_chosen, base_stats=base_stats,
                active_skills=[base_skill, lightning_arrow])

if __name__ == '__main__':
    print(player)
    print('---')
    print(Comparator(player, player).compare_players())
