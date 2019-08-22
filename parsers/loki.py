#!/usr/bin/env python3
import xmltodict

from Character import Character
from Gem import Gem

resists_table = {
    '0': '1',
    '1': '2',
    '2': '3',
    '3': '5',
    '4': '7',
    '5': '9',
    '6': '11',
    '7': '13',
    '8': '15',
    '9': '17',
}

power_table = resists_table

stats_table = {
    '0': '1',
    '1': '4',
    '2': '7',
    '3': '10',
    '4': '13',
    '5': '16',
    '6': '19',
    '7': '22',
    '8': '25',
    '9': '28',
}

hits_table = {
    '0': '4',
    '1': '12',
    '2': '20',
    '3': '28',
    '4': '36',
    '5': '44',
    '6': '52',
    '7': '60',
    '8': '68',
    '9': '76',
}


class Item:
    def __init__(self):
        self.location = ''
        self.origin = ''
        self.equip = ''
        self.name = ''
        self.level = ''
        self.quality = ''
        self.stats = []

    def item_to_zenkcraft_format(self):
        if self.location == 'Chest':
            self.location = 'Torso'
        if self.location == 'Head':
            self.location = 'Helmet'
        if self.location == 'Two-Handed':
            self.location = 'Two Handed'
        if self.location == 'Jewel':
            self.location = 'Jewelry'
        if self.location == 'Belt':
            self.location = 'Waist'
        if self.location == 'Left Ring':
            self.location = 'L. Ring'
        if self.location == 'Right Ring':
            self.location = 'R. Ring'
        if self.location == 'Left Wrist':
            self.location = 'L. Wrist'
        if self.location == 'Right Wrist':
            self.location = 'R. Wrist'

        for gem in self.stats:
            if gem.bonus_type == 'Hits':
                gem.bonus_type = 'H.P.'
                gem.bonus_attribute = 'Hit Points'

            if gem.bonus_type == 'Power':
                gem.bonus_attribute = 'Power'

            if gem.bonus_attribute == 'All Magic':
                gem.bonus_attribute = 'All Magic Skills'

    def add_location(self, location):
        self.location = location

    def add_origin(self, origin):
        self.origin = origin

    def add_equip(self, equip):
        self.equip = equip

    def add_stats(self, stats):
        for stats_key, stats_val in stats.items():
            if stats_key == '@name':
                self.name = stats_val
            if stats_key == '@level':
                self.level = stats_val
            if stats_key == '@quality':
                self.quality = stats_val
            if stats_key == 'gem':
                for gem_info in stats_val:
                    gem = Gem()
                    for gem_key, gem_val in gem_info.items():
                        if gem_key == 'type':
                            gem.bonus_type = gem_val
                        elif gem_key == 'amount':
                            if self.origin == 'crafted':
                                if gem.bonus_type == 'Resist':
                                    gem.bonus_amount = resists_table[gem_val]
                                elif gem.bonus_type == 'Stat':
                                    gem.bonus_amount = stats_table[gem_val]
                                elif gem.bonus_type == 'Power':
                                    gem.bonus_amount = power_table[gem_val]
                                elif gem.bonus_type == 'Hits':
                                    gem.bonus_amount = hits_table[gem_val]
                            else:
                                gem.bonus_amount = gem_val
                        elif gem_key == 'effect':
                            gem.bonus_attribute = gem_val
                    self.stats.append(gem)
            self.item_to_zenkcraft_format()

    def __repr__(self):
        return 'Location: "{}", Origin: "{}", Equip: "{}", Name: "{}", Level: "{}", Quality: "{}", Stats: {}'.format(
            self.location, self.origin, self.equip, self.name, self.level, self.quality, self.stats)


def parse(template_file):
    with open(template_file) as fd:
        doc = xmltodict.parse(fd.read())

    dump = doc['character']
    template_char = Character(dump['@name'], dump['@level'], dump['@realm'], dump['@class'], dump['@race'])

    for dump_key, dump_val in dump['items'].items():
        if dump_key == 'item':
            for my_item in dump_val:
                item = Item()
                for key, value in my_item.items():
                    if key == '@loc':
                        item.add_location(value)
                    if key == '@origin':
                        item.add_origin(value)
                    if key == '@equip':
                        item.add_equip(value)
                    if item.origin == key:
                        item.add_stats(value)
                template_char.items.append(item)
    return template_char


if __name__ == '__main__':
    file = 'samples/Drewgiismitecleric.mmr'
    character = parse(file)
    print(character)
    for stats in character.items:
        print(stats)
