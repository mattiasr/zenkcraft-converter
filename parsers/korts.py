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
        self.template_index = ''
        self.stats = []

    def item_to_zenkcraft_format(self):
        if self.location == 'Chest':
            self.location = 'Torso'
        if self.location == 'Head':
            self.location = 'Helmet'
        if self.location == '2 Handed':
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
        if self.origin == 'player':
            self.origin = 'crafted'

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
        if equip == '1':
            self.equip = 'yes'
        else:
            self.equip = 'no'

    def __repr__(self):
        return 'Location: "{}", Origin: "{}", Equip: "{}", Name: "{}", Level: "{}", Quality: "{}", Stats: {}'.format(
            self.location, self.origin, self.equip, self.name, self.level, self.quality, self.stats)


def parse(template_file):
    with open(template_file) as fd:
        doc = xmltodict.parse(fd.read())

    dump = doc['SCTemplate']
    template_char = Character(dump['Name'], dump['Level'], dump['Realm'], dump['Class'], dump['Race'])

    # Parse the items
    for dump_item in dump['SCItem']:
        if dump_item['Location'] == 'Mythical':
            continue
        item = Item()
        item.name = dump_item['ItemName']
        item.level = dump_item['Level']
        item.quality = dump_item['ItemQuality']
        item.add_location(dump_item['Location'])
        item.add_origin(dump_item['ActiveState'])
        item.add_equip(dump_item['Equipped'])
        item.template_index = dump_item['TemplateIndex']
        if 'SLOT' in dump_item:
            for gem_stat in dump_item['SLOT']:
                gem = Gem()
                gem.bonus_type = gem_stat['Type']
                gem.bonus_attribute = gem_stat['Effect']
                gem.bonus_amount = gem_stat['Amount']
                item.stats.append(gem)
        item.item_to_zenkcraft_format()
        template_char.items.append(item)

    # Parse the outfits, We select outfit nr1 as our outfit
    equipped_outfit_items = []
    for key, val in dump.items():
        if key == 'Outfit':
            for sub_key, sub_val in val.items():
                if sub_key == 'OutfitItem':
                    for outfit_item in sub_val:
                        for outfit_index in outfit_item:
                            if outfit_index == "@Index":
                                equipped_outfit_items.append(outfit_item[outfit_index])

    filtered_items = []
    for temp_item in template_char.items:
        if temp_item.template_index in equipped_outfit_items:
            filtered_items.append(temp_item)

    template_char.items = filtered_items
    return template_char


if __name__ == '__main__':
    file = '../samples/hunter_template.xml'
    character = parse(file)
    print(character)
    for stats in character.items:
        print(stats)
