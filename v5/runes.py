from v5.qualities import *



class Rune:
    def __init__(self, weapon, armour):
        self.armour_modifier = armour
        self.weapon_modifier = weapon


GlacialRune = Rune(AddModifier(Damage, DamageTypeVector(DMG0_LST, **{'Cold': Vector([6, 10])})),
                   AddResistance('Cold', .12))
BodyRune = Rune(AddModifier(PhysicalLifeLeech, .03), AddModifier(Life, 25))
DesertRune = Rune(AddModifier(Damage, DamageTypeVector(DMG0_LST, **{'Fire': Vector([7, 11])})),
                  AddResistance('Fire', .12))
IronRune = Rune(LocalIncreaseModifier(Damage, Vector([.2, 0, 0, 0, 0])), LocalDefenceIncrease(.2))
SoulCoreOfCitaqualotl = Rune(ElementalDamageIncrease(.3), AddModifier(Resistances, ResistanceVector([.05, .05, .05, 0])))
StormRune = Rune(AddLightningDamage(1, 20), AddResistance('Lightning', .12))
