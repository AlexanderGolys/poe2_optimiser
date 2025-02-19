from v5.items import *


def letters(txt):
    return ''.join([c for c in txt if 'a' <= c <= 'z' or 'A' <= c <= 'Z'])


def numeric(c):
    return '0' <= c <= '9'


def digits(txt):
    return ''.join([c for c in txt if numeric(c)])


def normalise_whitespace(txt):
    while '  ' in txt or '\t' in txt or '\n' in txt:
        txt = txt.replace('  ', ' ').replace('\t', ' ').replace('\n', ' ')
    return txt


def remove_whitespace(txt):
    return ''.join([c for c in txt if not c in [' ', '\t', '\n']])


def first_int(txt):
    for t in normalise_whitespace(txt).split(' '):
        if digits(t) == t:
            return int(t)
    raise ValueError('No integer found in text')


def all_ints(txt):
    return [int(t) for t in normalise_whitespace(txt).split(' ') if digits(t) == t]


def first_two_ints(txt):
    return all_ints(txt)[:2]


def first_float(txt):
    txt = normalise_whitespace(txt)
    if txt == '':
        raise ValueError('empty text, no floats found')
    if not '.' in txt[1:-1]:
        try:
            return first_int(txt)
        except ValueError:
            raise ValueError('No dot or integer found in text')

    dot_place = txt.index('.')
    if dot_place == 0 or txt[dot_place - 1] == ' ':
        return float('0.' + str(first_int(txt)))
    int_part = first_int(txt)
    dec = first_int(txt[dot_place + 1:])
    return float(str(int_part) + '.' + str(dec))


def first_percent_int(txt):
    return all_ints(txt.split('%')[0])[-1]


def first_percent_float(txt):
    txt = normalise_whitespace(txt)
    return first_float(txt.split('%')[0].split(' ')[-1])


def begins_with(txt, s):
    return txt[:len(s)] == s


class ModifierParser:
    def __init__(self, line, item_class):
        self.line = line
        self.letters = letters(line).lower()
        self.item_class = item_class

    def parse_local_weapon(self):
        if self.letters == 'increasedphysicaldamage':
            return LocalPhysicalDamageIncrease(first_percent_int(self.line) / 100)
        if self.letters == 'increasedattackspeed':
            return LocalIncreaseModifier(AttackSpeed, first_percent_int(self.line) / 100)
        if self.letters == 'addstolightningdamage':
            a, b = first_two_ints(self.line)
            return LocalAddLightningDamage(a, b)
        if self.letters == 'addstocolddamage':
            a, b = first_two_ints(self.line)
            return LocalAddColdDamage(a, b)
        if self.letters == 'addstofiredamage':
            a, b = first_two_ints(self.line)
            return LocalAddFireDamage(a, b)
        if self.letters == 'addstochaosdamage':
            a, b = first_two_ints(self.line)
            return LocalAddChaosDamage(a, b)
        if self.letters == 'addstophysicaldamage':
            a, b = first_two_ints(self.line)
            return LocalAddPhysicalDamage(a, b)

    def parse(self):
        if issubclass(self.item_class, Weapon):
            m = self.parse_local_weapon()
            if m is not None:
                return m

        local_add_armour_types = {
            'tomaximumenergyshield': EnergyShield,
            'toarmour': Armour,
            'toevasionrating': Evasion
        }
        if issubclass(self.item_class, ArmourItem):
            if self.letters in local_add_armour_types:
                return LocalAddModifier(local_add_armour_types[self.letters], first_int(self.line))

        global_add_keywords_int = {
            'toaccuracyrating': Accuracy,
            'tostrength': Strength,
            'todexterity': Dexterity,
            'tointelligence': Intelligence,
            'tomaximumlife': Life,
            'tomaximummana': Mana,
            'tomaximumenergyshield': EnergyShield,
            'toarmour': Armour,
            'toevasionrating': Evasion,
            'gainlifeperenemykilled': LifePerKill
        }

        if self.letters in global_add_keywords_int:
            return AddModifier(global_add_keywords_int[self.letters], first_int(self.line))

        nonumeric = {
            'bowattacksfireanadditionalarrow': AddModifier(ExtraProjectiles, 1),
        }

        if self.letters in nonumeric:
            return nonumeric[self.letters]

        damage_add = {
            'addstophysicaldamagetoattacks': AddPhysicalDamage,
            'addstofiredamagetoattacks': AddFireDamage,
            'addstocolddamagetoattacks': AddColdDamage,
            'addstolightningdamagetoattacks': AddChaosDamage,
            'addstochaosdamagetoattacks': AddChaosDamage
        }

        if self.letters in damage_add:
            a, b = first_two_ints(self.line)
            return damage_add[self.letters](a, b)

        damage_increase = {
            'increasedphysicaldamage': PhysicalDamageIncrease,
            'increasedfiredamage': IncreaseFireDamage,
            'increasedlightningdamage': IncreaseLightningDamage,
            'increasedchaosdamage': IncreaseChaosDamage,
            'increasedcoldamage': IncreaseColdDamage
        }

        if self.letters in damage_increase:
            return damage_increase[self.letters](first_percent_int(self.line) / 100)


class ItemParser:
    def __init__(self, filename):
        with open(filename) as f:
            self.string = f.read()
        self.blocks = self.string.split('\n--------\n')
        self.lines = [normalise_whitespace(l) for l in self.string.split('\n') if '--------' not in l and l != '']

    def item_class(self):
        classes = {
            'Amulets': Amulet,
            'Rings': Ring,
            'Crossbows': Crossbow,
            'Bows': Bow,
            'Quivers': OffHand,
            'Gloves': Gloves,
            'Boots': Boots,
            'Helmets': Helmet,
            'Body Armours': BodyArmour,
        }
        return classes[self.lines[0].split(': ')[1]]

    def rarity(self):
        for line in self.lines:
            if begins_with(line, 'Rarity: '):
                return line.split(': ')[1]
        return 'Rarity unknown'

    def item_level(self):
        for line in self.lines:
            if begins_with(line, 'Item Level: '):
                return first_int(line)
        return 'Item level unknown'

    def implicit_mod(self):
        for line in self.lines:
            if ' (implicit)' in line:
                return ModifierParser(line.replace(' (implicit)', ''), self.item_class()).parse()

    def corrupted_mod(self):
        for line in self.lines:
            if ' (enchant)' in line:
                return ModifierParser(line.replace(' (enchant)', ''), self.item_class()).parse()
