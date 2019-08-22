#!/usr/bin/env python3
import os
import random
from pathlib import Path

from parsers import loki, korts
from xml.etree import ElementTree
from xml.dom import minidom


# TODO: Add arguments support to specify template to convert

def random_generator(size, chars):
    return ''.join(random.choice(chars) for x in range(size))


def generate_sf_template_id():
    glyphs = '0123456789'
    sf_template_id = '1'
    sf_template_id += random_generator(8, glyphs)
    return sf_template_id


def generate_profile_id():
    glyphs = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return random_generator(10, glyphs)


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def main(file, write_template=True):
    if file.endswith('.mmr'):
        print('Detected LoKi template')
        character = loki.parse(file)
    elif file.endswith('.xml'):
        print('Detected Kort\'s template')
        character = korts.parse(file)
    else:
        raise Exception("Unable to figure out format of template")

    default_selected_weapon_type = 'Right Hand'

    from xml.etree.ElementTree import Element, SubElement

    top = Element('PlayerSaveData')
    top.set('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')
    top.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')

    player_name = SubElement(top, 'playerName')
    player_name.text = character.name

    player_realm = SubElement(top, 'realm')
    player_realm.text = character.realm

    player_class = SubElement(top, 'className')
    player_class.text = character.realm_class

    player_race = SubElement(top, 'race')
    player_race.text = character.race

    player_level = SubElement(top, 'level')
    player_level.text = character.level

    items = SubElement(top, 'items')
    items.text = ''

    # Loop through all items start
    for parsed_item in character.items:
        item = SubElement(items, 'Item')
        item.text = ''

        item_source_type = SubElement(item, 'sourceType')

        # Options: Spellcraft, Merchant, ROG
        if parsed_item.origin == 'crafted':
            item_source_type.text = 'Spellcraft'
        else:
            item_source_type.text = 'ROG'

        item_allowed_position = SubElement(item, 'allowedPosition')

        item_allowed_position.text = parsed_item.location
        item_name = SubElement(item, 'itemName')
        item_name.text = parsed_item.name
        item_notes = SubElement(item, 'itemNotes')
        item_notes.text = ''
        item_num_feathers = SubElement(item, 'numFeathers')
        item_num_feathers.text = '0'  # Just always hardcode to 0, i don't care about feathers.
        item_level = SubElement(item, 'level')
        item_level.text = parsed_item.level
        item_quality = SubElement(item, 'quality')
        item_quality.text = parsed_item.quality
        item_enabled = SubElement(item, 'itemEnabled')
        if parsed_item.equip == 'yes':
            item_enabled.text = 'true'
            item_at_item_include = SubElement(item, 'AT_itemIncluded')
            item_at_item_include.text = 'true'

            # Also figure out which default selected mode: Right Hand, Two Handed, Ranged
            if parsed_item.location == 'Right Hand':
                default_selected_weapon_type = parsed_item.location
            elif parsed_item.location == "Two Handed":
                default_selected_weapon_type = parsed_item.location
            elif parsed_item.location == "Ranged":
                default_selected_weapon_type = parsed_item.location
        else:
            item_enabled.text = 'true'
            item_at_item_include = SubElement(item, 'AT_itemIncluded')
            item_at_item_include.text = 'false'

        item_stats = SubElement(item, 'stats')
        item_stats.text = ''
        # Loop through each items gems
        for gem in parsed_item.stats:
            item_stats_entry = SubElement(item_stats, 'StatEntry')
            item_stats_entry.text = ''
            item_stats_entry_bonus_type = SubElement(item_stats_entry, 'bonusType')
            item_stats_entry_bonus_type.text = gem.bonus_type
            item_stats_entry_bonus_attribute = SubElement(item_stats_entry, 'bonusAttribute')
            item_stats_entry_bonus_attribute.text = gem.bonus_attribute
            item_stats_entry_bonus_amount = SubElement(item_stats_entry, 'bonusAmount')
            item_stats_entry_bonus_amount.text = gem.bonus_amount
    # Loop through all items stop

    last_save_time = SubElement(top, 'lastSaveTime')
    last_save_time.text = '01:37 PM'

    last_save_date = SubElement(top, 'lastSaveData')
    last_save_date.text = 'aug. 14, 2019'

    profile_id = SubElement(top, 'profileID')
    profile_id.text = generate_profile_id()

    sf_template_id = SubElement(top, 'SF_TemplateID')
    sf_template_id.text = generate_sf_template_id()

    selected_weapon_type = SubElement(top, 'selectedWeaponType')
    selected_weapon_type.text = default_selected_weapon_type

    auto_template_stat_order = SubElement(top, 'AutoTemplate_StatOrder')
    auto_template_disabled_stats = SubElement(top, 'AutoTemplate_DisabledStats')

    output_file = '{}.znk'.format(character.name.replace(' ', '-'))
    if write_template:
        p = Path('out')

        if not p.exists():
            os.mkdir('out')

        with open('out{}{}'.format(os.sep, output_file), 'w') as fd:
            fd.write(prettify(top))
        print('Successfully converted: out{}{}'.format(os.sep, output_file))


if __name__ == '__main__':
    template = 'samples/Drewgiismitecleric.mmr'
    template = 'samples/loki-animist.mmr'
    template = 'samples/Ghita_template.xml'
    # template = 'samples/hunter_template.xml'
    main(template)
