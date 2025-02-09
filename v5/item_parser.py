from items import *


def keep_only_letters(txt):
    return ''.join([c for c in txt if 'a' <= c <= 'z' or 'A' <= c <= 'Z'])


class ModifierEncoding:
    def __init__(self, letters, decoder):
        self.letters = letters
        self.decoder = decoder
        self.identifier = None

    def check_type(self, line):
        if self.identifier is not None:
            return self.identifier(line)
        return keep_only_letters(line) == self.letters

    def __call__(self, line):
        return self.decoder(line)


class LocalDamageEncoding(ModifierEncoding):
    def __init__(self, dmg_type):
        self.dmg_type = dmg_type

        def decode(line):
            p0 = int(line.split(' ')[1])
            p1 = int(line.split(' ')[3])
            if self.dmg_type == 'Physical':
                return LocalAddModifier(Damage, Vector([Vector([p0, p1]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0])]))
            if self.dmg_type == 'Lightning':
                return LocalAddModifier(Damage, Vector([Vector([0, 0]), Vector([p0, p1]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0])]))
            if self.dmg_type == 'Fire':
                return LocalAddModifier(Damage, Vector([Vector([0, 0]), Vector([0, 0]), Vector([p0, p1]), Vector([0, 0]), Vector([0, 0])]))
            if self.dmg_type == 'Cold':
                return LocalAddModifier(Damage, Vector([Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([p0, p1]), Vector([0, 0])]))
            if self.dmg_type == 'Chaos':
                return LocalAddModifier(Damage, Vector([Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([p0, p1])]))

        super().__init__(f'Addsto{dmg_type}Damage', decode)


class LocalAddDefenseEncoding(ModifierEncoding):
    def __init__(self, defense_type):
        self.defense_type = defense_type

        def decode(line):
            p = int(line[1:].split(' ')[0])
            return LocalAddModifier(self.defense_type, p)

        super().__init__(f'tomaximum{self.defense_type.name}', decode)


class LocalIncDefenseEncoding(ModifierEncoding):
    def __init__(self, defense_type):
        self.defense_type = defense_type

        def decode(line):
            p = int(line.split('% ')[0])
            return LocalIncreaseModifier(self.defense_type, p)

        super().__init__(f'increased{self.defense_type.name}', decode)


class AddEncode(ModifierEncoding):
    def __init__(self, stat):
        def decode(line):
            p = int(line[1:].split(' to')[0])
            return AddModifier(stat, p)

        super().__init__(f'', decode)
        self.identifier = lambda x: x[0] == '+'


class ItemParser:
    stat_parsed_names = {
        'Critical Hit Chance': CritChance,
        'Attack Speed': AttackSpeed,
        'Critical Damage Bonus': CritBonus,
        'Accuracy Rating': Accuracy,
        'Reload Time': ReloadTime,
        'Attacks per Second': AttackSpeed,
    }

    damage_parsed_names = ['Physical Damage', 'Lightning Damage', 'Fire Damage', 'Cold Damage', 'Chaos Damage']

    item_classes = {
        'Crossbows': Crossbow,
    }

    def __init__(self, parsed_text):
        self.raw = parsed_text
        self.blocks = list(map(ItemParser.clean_parsed_fragment, parsed_text.split('--------\n')))
        self.header_block = self.blocks[0]

        self.base_stats_dict = {line.split(': ')[0]: line.split(': ')[1] for line in self.blocks[1].split('\n') if ': ' in line}

        if 'Quality' in self.base_stats_dict.keys():
            self.quality = int(self.base_stats_dict['Quality'].replace('%', '').replace('+', '')) / 100
            self.base_stats_dict.pop('Quality')

        self.rune_lines = []
        self.sockets = 0
        self.implicit_line = ''

        for block in self.blocks[2:]:
            lines = block.split('\n')
            for line in lines:
                if '(rune)' in line:
                    self.rune_lines.append(line.replace(' (rune)', '').strip())
                if 'Sockets' in line:
                    self.sockets = len([c for c in line.split(': ')[1] if c == ' S'])
                if '(implicit)' in line:
                    self.implicit_line = line.replace(' (implicit)', '').strip()
                if 'Item Level:' in line:
                    self.item_level = int(line.split(': ')[1])
                if 'Corrupted' in line:
                    self.corrupted = True

        self.affix_lines = list(self.blocks[-1].split('\n')) if not self.corrupted else list(self.blocks[-2].split('\n'))

    def decode_modifier(self, line):
        if keep_only_letters(line) == 'AddstoPhysicalDamage':
            p0 = int(line.split(' ')[1])
            p1 = int(line.split(' ')[3])
            return LocalAddModifier(Damage, Vector([Vector([p0, p1]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0])]))
        if keep_only_letters(line) == 'AddstoPhysicalDamage':
            p0 = int(line.split(' ')[1])
            p1 = int(line.split(' ')[3])
            return LocalAddModifier(Damage, Vector([Vector([p0, p1]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0]), Vector([0, 0])]))

    def parse_affixes(self):
        return [self.decode_modifier(line) for line in self.affix_lines]

    def parse_implicits(self):
        if self.implicit_line == '':
            return []
        return [self.decode_modifier(self.implicit_line)]

    @staticmethod
    def clean_parsed_fragment(line):
        return line.replace('\t', ' ').replace('(augmented)', '').strip()

    @staticmethod
    def parse_percent(txt):
        return Percent(float(txt.replace('%', '')) / 100)
