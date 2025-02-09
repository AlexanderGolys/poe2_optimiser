from v5.players import *


class Comparator:
    def __init__(self, player1, player2=None):
        self.player1 = player1
        self.player2 = player2 or deepcopy(player1)

    def compare_stat(self, stat):
        v1 = self.player1.get_stat(stat).value()
        v2 = self.player2.get_stat(stat).value()
        absolute = v2 - v1

        if isinstance(v1, Vector):
            v1 = v1.mean()
            v2 = v2.mean()
        if isinstance(v1, Vector):
            v1 = v1.mean()
            v2 = v2.mean()
        if isinstance(v1, Percent):
            v1 = v1.value
            v2 = v2.value

        sign = '+' if v2 > v1 else ''
        tab = '\t\t' if sign == '' else ' '
        sign_full = '(+)' if sign == '+' else '(-)'
        if v1 == 0:
            return f'{sign_full}{tab}{stat.name}: {sign}{absolute:.2f}'
        relative = (v2 - v1) / v1

        return f'{sign_full}{tab}{stat.name}: ({sign}{relative*100:.0f}%) {sign}{absolute:.2f} \t {v1:.2f} -> {v2:.2f}'

    def compare_players(self):
        stats = sum(self.player1.blocks, [])
        stats = [stat for stat in stats if not isinstance(stat, SpecialisedStatName)]
        return '\n'.join([self.compare_stat(stat) for stat in stats if self.player1.get_stat(stat).value() != self.player2.get_stat(stat).value()]) + '\n-----\n' + '\n'.join([self.compare_dps(skill) for skill in self.player1.active_skills])

    def compare_dps(self, skill):
        v1 = self.player1.active_skill_dps(skill)
        v2 = self.player2.active_skill_dps(skill)
        sign = '+' if v2 > v1 else '' if v2 < v1 else ''
        sign_full = '(+)' if sign == '+' else '(-)'
        absolute = v2 - v1
        relative = (v2 - v1) / v1
        return f'{sign_full} {skill.name} DPS: ({sign}{relative*100:.0f}%) \t {sign}{absolute:.0f} \t {v1:.0f} -> {v2:.0f}'


    def compare_items(self, item1, item2, slot=1):
        self.player2 = deepcopy(self.player1)
        self.player2.equip(item2, slot)
        self.player1.equip(item1, slot)
        return self.compare_players()

    def compare_inventories(self, inventory1, inventory2):
        self.player2 = deepcopy(self.player1)
        self.player2.inventory = inventory2
        self.player1.inventory = inventory1
        return self.compare_players()

    def compare_passives(self, passive1, passive2):
        self.player2 = deepcopy(self.player1)
        self.player2.passive_skills = passive2
        self.player1.passive_skills = passive1
        return self.compare_players()

    def choose_item(self, skill, *items, slot=1):
        best = None
        best_dps = 0
        dps_list = []
        for item in items:
            self.player1.equip(item, slot)
            dps = self.player1.active_skill_dps(skill)
            dps_list.append(dps)
            if dps > best_dps:
                best = item
                best_dps = dps
        print(f'Best DPS: {best_dps:.0f}  (among {[f"{d:.0f}" for d in dps_list]})')
        return best
