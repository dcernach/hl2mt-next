import re
import struct
# from PyQt4.QtCore import *

import hashlib
import io
import html
import macros.health
import util
import templates.spell as spellTmpl

from macros.special import *
from macros.initiative import *

from PIL import Image


# noinspection PyCallByClass
class Pathfinder:
    """The Pathfinder class parses a Hero Lab character and converts it into a Maptool token"""

    def __init__(self, name, xml):
        self.name = str(name)
        self.xml = xml
        self.html_statblock = ''
        self.html_filename = ''
        self.languages = []
        self.attrib_scores = {}
        self.attrib_bonuses = {}
        self.saves = {}
        self.resists = {}
        self.immunities = {}
        self.maneuvers = {}
        self.skills = {}
        self.feats = {}
        self.traits = {}
        self.vision_lowlight = 0
        self.vision_dark = 0
        self.num_macros = 0
        self.cr = ''
        self.mr = ''
        self.weapons = []
        self.weapon_sort = 0
        self.items = []
        self.specials = {}
        self.itempowers = {}
        self.spells = []
        self.spells_memorized = []
        self.spells_known = []
        self.values = []

        self.custom_property_map_xml = {}
        self.properties_xml = '<map>\n  <entry>\n    <string>version</string>\n    <string>1.3.b87</string>\n' + \
                              '  </entry>\n</map>'

        self.settings = QSettings
        self.size_map = {'fine': 'fwABAc1lFSoBAAAAKgABAQ==', 'diminutive': 'fwABAc1lFSoCAAAAKgABAQ==',
                         'tiny': 'fwABAc5lFSoDAAAAKgABAA==', 'small': 'fwABAc5lFSoEAAAAKgABAA==',
                         'medium': 'fwABAc9lFSoFAAAAKgABAQ==', 'large': 'fwABAdBlFSoGAAAAKgABAA==',
                         'huge': 'fwABAdBlFSoHAAAAKgABAA==', 'gargantuan': 'fwABAdFlFSoIAAAAKgABAQ==',
                         'colossal': 'fwABAeFlFSoJAAAAKgABAQ=='}

        self.specialMacros = SpecialMacros()
        self.initMacros = InitMacros(self.custom_property_map_xml)

    def parse(self):
        self.parse_base()
        self.parse_languages()
        self.parse_attributes()
        self.parse_saves()
        self.parse_resists()
        self.parse_maneuvers()
        self.parse_skills()
        self.parse_feats()
        self.parse_traits()
        self.parse_senses()
        self.parse_weapons()
        self.parse_items()
        self.parse_specials()
        self.parse_itempowers()
        self.parse_spells()
        self.create_base_props()

    def parse_base(self):
        self.role = self.xml.get('role')
        self.player = self.xml.get('playername')
        self.race = self.xml.find('race').get('racetext')
        self.alignment = self.xml.find('alignment').get('name')
        self.size = self.xml.find('size').get('name').lower()

        if not self.size:
            self.size = 'medium'

        self.space = self.xml.find('size').find('space').get('value')
        self.reach = self.xml.find('size').find('reach').get('value')
        self.ac = self.xml.find('armorclass').get('ac')
        self.ac_touch = self.xml.find('armorclass').get('touch')
        self.ac_flat = self.xml.find('armorclass').get('flatfooted')
        self.hpc = self.xml.find('health').get('currenthp')
        self.hpm = self.xml.find('health').get('hitpoints')
        self.hd = self.xml.find('health').get('hitdice')
        self.movement = self.xml.find('movement').find('speed').get('value')
        self.initiative = self.xml.find('initiative').get('total')
        self.atk_melee = self.xml.find('attack').get('meleeattack')
        self.atk_ranged = self.xml.find('attack').get('rangedattack')
        self.bab = self.xml.find('attack').get('baseattack')
        self.gender = self.xml.find('personal').get('gender')
        self.pp = self.xml.find('money').get('pp')
        self.gp = self.xml.find('money').get('gp')
        self.sp = self.xml.find('money').get('sp')
        self.cp = self.xml.find('money').get('cp')
        self.xpvalue = '0'

        if self.xml.find('xpaward') is not None:
            self.xpvalue = self.xml.find('xpaward').get('value')

    def parse_languages(self):
        for language in self.xml.find('languages').iter('language'):
            self.languages.append(language.get('name'))

    def parse_attributes(self):
        for attribute in self.xml.find('attributes').iter('attribute'):
            self.attrib_scores[attribute.get('name')] = attribute.find('attrvalue').get('modified')
            self.attrib_bonuses[attribute.get('name')] = attribute.find('attrbonus').get('modified')

    def parse_saves(self):
        for save in self.xml.find('saves').iter('save'):
            self.saves[save.get('abbr')] = save.get('save')

    def parse_resists(self):
        for resistance in self.xml.find('immunities').iter('special'):
            self.resists[resistance.get('name')] = resistance.find('description').text
        for resistance in self.xml.find('damagereduction').iter('special'):
            self.resists[resistance.get('name')] = resistance.find('description').text
        for resistance in self.xml.find('resistances').iter('special'):
            self.resists[resistance.get('name')] = resistance.find('description').text
        for resistance in self.xml.find('weaknesses').iter('special'):
            self.resists[resistance.get('name')] = resistance.find('description').text

    def parse_maneuvers(self):
        self.cmb = self.xml.find('maneuvers').get('cmb')
        self.cmd = self.xml.find('maneuvers').get('cmd')
        self.cmd_flat = self.xml.find('maneuvers').get('cmdflatfooted')

        for maneuver in self.xml.find('maneuvers').iter('maneuvertype'):
            self.maneuvers[maneuver.get('name')] = maneuver.get('cmb')

    def parse_skills(self):
        for skill in self.xml.find('skills').iter('skill'):
            self.skills[skill.get('name')] = skill.get('value')

    def parse_feats(self):
        for feat in self.xml.find('feats').iter('feat'):
            self.feats[feat.get('name')] = feat.find('description').text

    def parse_traits(self):
        for trait in self.xml.find('traits').iter('trait'):
            self.traits[trait.get('name')] = trait.find('description').text

    def parse_senses(self):
        for sense in self.xml.find('senses').iter('special'):
            if sense.get('shortname') == 'Low-Light Vision':
                self.vision_lowlight = 1
            elif re.search('Darkvision \(?\d+', sense.get('shortname')):
                found = re.search('Darkvision \(?(\d+)', sense.get('shortname'))
                self.vision_dark = found.group(1)
            elif re.search('Darkvision', sense.get('shortname')):
                self.vision_dark = 60
            else:
                self.specials[sense.get('name')] = sense.find('description').text

    def parse_weapons(self):
        for weapon in self.xml.find('melee').iter('weapon'):
            temp = {'name': re.sub('\s*\(.+\)', '', weapon.get('name')), 'atk': weapon.get('attack'),
                    'dam': weapon.get('damage'), 'crit': weapon.get('crit')}
            if temp not in self.weapons:
                self.weapons.append(temp)

            if re.search('Thrown', weapon.get('categorytext')):
                temp = {'name': "Thrown " + re.sub('\s*\(.+\)', '', weapon.get('name')),
                        'atk': weapon.find('rangedattack').get('attack'), 'dam': weapon.get('damage'),
                        'crit': weapon.get('crit')}
                if temp not in self.weapons:
                    self.weapons.append(temp)

        for weapon in self.xml.find('ranged').iter('weapon'):
            temp = {'name': re.sub('\s*\(.+\)', '', weapon.get('name')), 'atk': weapon.get('attack'),
                    'dam': weapon.get('damage'), 'crit': weapon.get('crit')}
            self.weapons.append(temp)

    def parse_items(self):
        for item in self.xml.find('gear').iter('item'):
            temp = {'name': item.get('name'), 'num': item.get('quantity'), 'value': item.find('cost').get('text')}
            self.items.append(temp)

        for item in self.xml.find('magicitems').iter('item'):
            temp = {'name': item.get('name'), 'num': item.get('quantity'), 'value': item.find('cost').get('text')}
            self.items.append(temp)

    def parse_specials(self):
        for special in self.xml.find('movement').iter('special'):
            self.specials[special.get('name')] = special.find('description').text
        for special in self.xml.find('attack').iter('special'):
            self.specials[special.get('name')] = special.find('description').text
        for special in self.xml.find('skillabilities').iter('special'):
            self.specials[special.get('name')] = special.find('description').text
        for special in self.xml.find('otherspecials').iter('special'):
            self.specials[special.get('name')] = special.find('description').text
        for special in self.xml.find('auras').iter('special'):
            self.specials[special.get('name')] = special.find('description').text
        for special in self.xml.find('spelllike').iter('special'):
            self.specials[special.get('name')] = special.find('description').text
        for special in self.xml.find('defensive').iter('special'):
            self.specials[special.get('name')] = special.find('description').text
        for special in self.xml.find('health').iter('special'):
            self.specials[special.get('name')] = special.find('description').text

    def parse_itempowers(self):
        if self.xml.find('magicitems').find('item') is not None:
            for special in self.xml.find('magicitems').iter('item'):
                for power in special.iter('itempower'):
                    self.itempowers[power.get('name')] = power.find('description').text

    def parse_spells(self):
        for spell in self.xml.find('spellbook').iter('spell'):
            temp = {'name': spell.get('name'), 'level': spell.get('level'), 'casttime': spell.get('casttime'),
                    'range': spell.get('range'), 'target': spell.get('target'), 'area': spell.get('area'),
                    'effect': spell.get('effect'), 'duration': spell.get('duration'), 'save': spell.get('save'),
                    'resist': spell.get('resist'), 'dc': spell.get('dc'), 'componenttext': spell.get('componenttext'),
                    'schooltext': spell.get('schooltext'), 'description': spell.find('description').text,
                    'casterlevel': spell.get('casterlevel')}
            temp['save'] = re.sub('DC\s*\d+\s*', '', temp['save'])
            if not temp['save']:
                temp['save'] = 'None'
            if not temp['resist']:
                temp['resist'] = 'NA'
            self.spells.append(temp)

        for spell in self.xml.find('spellsmemorized').iter('spell'):
            temp = {'name': spell.get('name'), 'level': spell.get('level'), 'casttime': spell.get('casttime'),
                    'range': spell.get('range'), 'target': spell.get('target'), 'area': spell.get('area'),
                    'effect': spell.get('effect'), 'duration': spell.get('duration'), 'save': spell.get('save'),
                    'resist': spell.get('resist'), 'dc': spell.get('dc'), 'componenttext': spell.get('componenttext'),
                    'schooltext': spell.get('schooltext'), 'description': spell.find('description').text,
                    'casterlevel': spell.get('casterlevel')}
            temp['save'] = re.sub('DC\s*\d+\s*', '', temp['save'])
            if not temp['save']:
                temp['save'] = 'None'
            if not temp['resist']:
                temp['resist'] = 'NA'
            self.spells_memorized.append(temp)

        for spell in self.xml.find('spellsknown').iter('spell'):
            temp = {'name': spell.get('name'), 'level': spell.get('level'), 'casttime': spell.get('casttime'),
                    'range': spell.get('range'), 'target': spell.get('target'), 'area': spell.get('area'),
                    'effect': spell.get('effect'), 'duration': spell.get('duration'), 'save': spell.get('save'),
                    'resist': spell.get('resist'), 'dc': spell.get('dc'), 'componenttext': spell.get('componenttext'),
                    'schooltext': spell.get('schooltext'), 'description': spell.find('description').text,
                    'casterlevel': spell.get('casterlevel')}
            temp['save'] = re.sub('DC\s*\d+\s*', '', temp['save'])
            if not temp['save']:
                temp['save'] = 'None'
            if not temp['resist']:
                temp['resist'] = 'NA'
            self.spells_known.append(temp)

    def create_base_props(self):
        self.custom_property_map_xml["hl2mt_initiative"] = self.initiative

    def make_content_xml(self):
        #######################################################################
        # TODO: This method should be refactored!!!!
        #######################################################################
        xml = '<net.rptools.maptool.model.Token>\n'
        xml += '  <id>\n'
        xml += '    <baGUID>fwABASo0c8kCAAAASQAAAA==</baGUID>\n'
        xml += '  </id>\n'
        xml += '  <beingImpersonated>false</beingImpersonated>\n'

        xml += '  <imageAssetMap>\n'
        xml += '    <entry>\n'
        xml += '    <null/>\n'
        xml += '      <net.rptools.lib.MD5Key>\n'
        xml += '        <id>' + self.pog_md5 + '</id>\n'
        xml += '      </net.rptools.lib.MD5Key>\n'
        xml += '    </entry>\n'
        xml += '    <entry>\n'
        xml += '      <string>' + self.name + '</string>\n'
        xml += '      <net.rptools.lib.MD5Key reference="../../entry/net.rptools.lib.MD5Key"/>\n'
        xml += '    </entry>\n'
        xml += '  </imageAssetMap>\n'

        xml += '  <currentImageAsset>' + self.name + '</currentImageAsset>\n'

        xml += '    <x>0</x>\n'
        xml += '    <y>0</y>\n'
        xml += '    <z>0</z>\n'
        xml += '    <anchorX>0</anchorX>\n'
        xml += '    <anchorY>0</anchorY>\n'
        xml += '    <sizeScale>1.0</sizeScale>\n'
        xml += '    <lastX>0</lastX>\n'
        xml += '    <lastY>0</lastY>\n'
        xml += '    <snapToScale>true</snapToScale>\n'
        xml += '    <width>0</width>\n'
        xml += '    <height>0</height>\n'
        xml += '    <scaleX>1.0</scaleX>\n'
        xml += '    <scaleY>1.0</scaleY>\n'

        xml += '    <sizeMap>\n'
        xml += '      <entry>\n'
        xml += '        <java-class>net.rptools.maptool.model.SquareGrid</java-class>\n'
        xml += '        <net.rptools.maptool.model.GUID>\n'
        xml += '          <baGUID>' + self.size_map[self.size] + '</baGUID>\n'
        xml += '        </net.rptools.maptool.model.GUID>\n'
        xml += '      </entry>\n'
        xml += '    </sizeMap>\n'

        xml += '    <snapToGrid>true</snapToGrid>\n'
        xml += '    <isVisible>true</isVisible>\n'
        xml += '    <visibleOnlyToOwner>false</visibleOnlyToOwner>\n'
        xml += '    <name>' + self.name + '</name>\n'
        xml += '    <ownerType>0</ownerType>\n'
        xml += '    <tokenShape>CIRCLE</tokenShape>\n'
        xml += '    <tokenType>' + self.role.upper() + '</tokenType>\n'
        xml += '    <propertyType>' + self.settings.value("properties/propname") + '</propertyType>\n'
        xml += '    <isFlippedX>false</isFlippedX>\n'
        xml += '    <isFlippedY>false</isFlippedY>\n'

        xml += '    <charsheetImage>\n'
        xml += '      <id>' + self.portrait_md5 + '</id>\n'
        xml += '    </charsheetImage>\n'

        xml += '    <portraitImage reference="../charsheetImage"/>\n'

        text = 'Normal'

        if self.vision_lowlight:
            text = 'LowLight'
        if self.vision_dark:
            text = 'Darkvision'
        if self.vision_dark and self.settings.value("vision") == 'True':
            text = 'Darkvision' + str(self.vision_dark)
        if self.vision_dark and self.settings.value("vision") == 'True' and self.vision_lowlight:
            text += ' and Lowlight'

        # util.write_vision_types(self.name, text) # Debug only

        xml += '    <sightType>' + text + '</sightType>\n'
        xml += '    <hasSight>true</hasSight>\n'
        xml += '    <state/>\n'

        xml += '    <propertyMapCI>\n'
        xml += '      <store>\n'
        # ----------------------------------------------------------------------
        # --> Create custom token Properties
        # ----------------------------------------------------------------------
        xml += self.property_xml(self.settings.value("properties/strength"), self.attrib_scores['Strength'])
        xml += self.property_xml(self.settings.value("properties/dexterity"), self.attrib_scores['Dexterity'])
        xml += self.property_xml(self.settings.value("properties/constitution"), self.attrib_scores['Constitution'])
        xml += self.property_xml(self.settings.value("properties/intelligence"), self.attrib_scores['Intelligence'])
        xml += self.property_xml(self.settings.value("properties/wisdom"), self.attrib_scores['Wisdom'])
        xml += self.property_xml(self.settings.value("properties/charisma"), self.attrib_scores['Charisma'])
        xml += self.property_xml(self.settings.value("properties/race"), self.race)
        xml += self.property_xml(self.settings.value("properties/alignment"), self.alignment)
        xml += self.property_xml(self.settings.value("properties/name"), self.name)
        xml += self.property_xml(self.settings.value("properties/player"), self.player)
        xml += self.property_xml(self.settings.value("properties/hp"), self.hpc)
        xml += self.property_xml(self.settings.value("properties/hpmax"), self.hpm)
        xml += self.property_xml(self.settings.value("properties/hptemp"), "0")
        xml += self.property_xml(self.settings.value("properties/speed"), self.movement)
        xml += self.property_xml(self.settings.value("properties/reach"), self.reach)
        xml += self.property_xml(self.settings.value("properties/ac"), self.ac)
        xml += self.property_xml(self.settings.value("properties/acflat"), self.ac_flat)
        xml += self.property_xml(self.settings.value("properties/actouch"), self.ac_touch)
        xml += self.property_xml(self.settings.value("properties/cmd"), self.cmd)
        xml += self.property_xml(self.settings.value("properties/cmdflat"), self.cmd_flat)
        xml += self.property_xml(self.settings.value("properties/melee"), self.atk_melee)
        xml += self.property_xml(self.settings.value("properties/ranged"), self.atk_ranged)
        xml += self.property_xml(self.settings.value("properties/xpvalue"), self.xpvalue)

        if self.settings.contains("properties/items"):
            tmp = ''
            for item in self.items:
                name = item['name']
                name = str.replace(name, "'", "")
                name = str.replace(name, "[", "")
                name = str.replace(name, "]", "")
                tmp += name
                if int(item['num']) > 1:
                    tmp += ' (x' + item['num'] + ')'
                tmp += '\n'
            if len(tmp) > 0:
                tmp += '\n'
            if int(self.pp) > 0:
                tmp += self.pp + 'pp '
            if int(self.gp) > 0:
                tmp += self.gp + 'gp '
            if int(self.sp) > 0:
                tmp += self.sp + 'sp '
            if int(self.cp) > 0:
                tmp += self.cp + 'cp '
            tmp += '\n'
            tmp = html.escape(tmp)

            xml += self.property_xml(self.settings.value("properties/items"), tmp)
        # ----------------------------------------------------------------------
        # <-- Create token Properties
        # ----------------------------------------------------------------------
        xml += '\n\n'
        xml += '        #{custom}'  # dca: replace to add custom properties if any
        xml += '\n\n'
        xml += '      </store>\n'
        xml += '    </propertyMapCI>\n'

        xml += '    <macroPropertiesMap>\n'

        if self.settings.value("indexing") == 'HTML' or self.settings.value("description") == 'True':
            xml += self.charsheet_macro_xml()

        if self.settings.value("hp") == 'True':
            xml += self.hp_macro_xml()

        ###############################################################
        # Basic Saving-Throw Macros
        ###############################################################
        colorf = self.settings.value("colors/savesf")
        colorb = self.settings.value("colors/savesb")
        xml += self.roll_macro_xml('Ref', self.saves['Ref'], 'Reflex Save', 'Basic', '53', colorb, colorf, '3')
        xml += self.roll_macro_xml('Will', self.saves['Will'], 'Willpower Save', 'Basic', '53', colorb, colorf, '3')
        xml += self.roll_macro_xml('Fort', self.saves['Fort'], 'Fortitude Save', 'Basic', '53', colorb, colorf, '3')

        ###############################################################
        # Basic Attack Macros
        ###############################################################
        colorf = self.settings.value("colors/attacksf")
        colorb = self.settings.value("colors/attacksb")
        xml += self.roll_macro_xml('Melee', self.atk_melee, 'Basic Melee', 'Basic', '53',
                                   colorb, colorf, '2')
        xml += self.roll_macro_xml('Ranged', self.atk_ranged, 'Basic Ranged', 'Basic', '53',
                                   colorb, colorf, '2')

        colorf = self.settings.value("colors/cmbf")
        colorb = self.settings.value("colors/cmbb")
        xml += self.roll_macro_xml('CMB', self.cmb, 'Basic CMB', 'Basic', '53',
                                   colorb, colorf, '2')

        ###############################################################
        # Basic Initiative Macros
        ###############################################################

        # xml += self.init_macro_xml()
        # xml += self.init_macro_xml(False)

        self.num_macros += 1
        xml += self.initMacros.gen_roll_init(self.num_macros)

        self.num_macros += 1
        xml += self.initMacros.gen_add_init(self.num_macros)

        self.num_macros += 1
        xml += self.initMacros.gen_remove_init(self.num_macros)

        self.num_macros += 1
        xml += self.initMacros.gen_next_init(self.num_macros)

        ###############################################################
        # Basic DICE Macros
        ###############################################################
        if self.settings.value("basicdice") == 'True':
            xml += self.basic_die_macro_xml('d4')
            xml += self.basic_die_macro_xml('d6')
            xml += self.basic_die_macro_xml('d8')
            xml += self.basic_die_macro_xml('d10')
            xml += self.basic_die_macro_xml('d12')
            xml += self.basic_die_macro_xml('d20')

        if self.settings.value("ability") == 'True':
            colorf = self.settings.value("colors/abilityf")
            colorb = self.settings.value("colors/abilityb")
            xml += self.roll_macro_xml('Str', self.attrib_bonuses['Strength'], 'Strength Check',
                                       'Basic Ability Checks', '31', colorb, colorf, '1')

            xml += self.roll_macro_xml('Dex', self.attrib_bonuses['Dexterity'], 'Dexterity Check',
                                       'Basic Ability Checks', '31', colorb, colorf, '2')

            xml += self.roll_macro_xml('Con', self.attrib_bonuses['Constitution'], 'Constitution Check',
                                       'Basic Ability Checks', '31', colorb, colorf, '3')

            xml += self.roll_macro_xml('Int', self.attrib_bonuses['Intelligence'], 'Intelligence Check',
                                       'Basic Ability Checks', '31', colorb, colorf, '4')

            xml += self.roll_macro_xml('Wis', self.attrib_bonuses['Wisdom'], 'Wisdom Check',
                                       'Basic Ability Checks', '31', colorb, colorf, '5')

            xml += self.roll_macro_xml('Cha', self.attrib_bonuses['Charisma'], 'Charisma Check',
                                       'Basic Ability Checks', '31', colorb, colorf, '6')

        if self.settings.value("skills") == 'True':
            for k, v in list(self.skills.items()):
                xml += self.roll_macro_xml(k, v, k, 'Skills', '75', self.settings.value("colors/skillsb"),
                                           self.settings.value("colors/skillsf"), '1')

        if self.settings.value("weapons") == 'True':
            for weapon in self.weapons:
                xml += self.weapon_macro_xml(weapon['name'], weapon['atk'], weapon['dam'], weapon['crit'])

        if self.settings.value("maneuvers") == 'True':
            for k, v in list(self.maneuvers.items()):
                xml += self.roll_macro_xml(k, v, k, 'Maneuvers', '75', self.settings.value("colors/maneuversb"),
                                           self.settings.value("colors/maneuversf"), '1')

        if self.feats:
            xml += self.list_macro_xml('Feats', self.feats, '75')

        if self.traits:
            xml += self.list_macro_xml('Traits', self.traits, '75')

        if self.specials:
            xml += self.list_macro_xml('Specials', self.specials, '75')

        if self.itempowers:
            xml += self.list_macro_xml('Item Powers', self.itempowers, '75')

        if self.resists:
            xml += self.list_macro_xml('Resists', self.resists, '75')

        if self.spells:
            xml += self.spell_list_macro_xml('Spellbook', self.spells, '75')

        if self.spells_memorized:
            xml += self.spell_list_macro_xml('Memorized', self.spells_memorized, '75')

        if self.spells_known:
            xml += self.spell_list_macro_xml('Spells Known', self.spells_known, '75')

        if self.items and self.settings.value("items") == 'True':
            xml += self.items_macro_xml()

        for row in range(0, 50):
            if self.settings.contains("cm_name_" + str(row)) and len(self.settings.value("cm_name_" + str(row))) > 0:
                name = self.settings.value("cm_name_" + str(row))
                group = self.settings.value("cm_group_" + str(row))
                font = self.settings.value("cm_font_" + str(row))
                background = self.settings.value("cm_background_" + str(row))
                value = self.settings.value("cm_value_" + str(row))

                xml += self.custom_macro_xml(name, group, font, background, value)

        if self.settings.value("indexing") == 'HTML':
            xml += self.list_show_macro_xml()

        if self.settings.value("description") == 'True':
            self.num_macros += 1
            xml += self.specialMacros.fn_detail_macro_xml(self.num_macros)

        xml += '    </macroPropertiesMap>\n'

        xml += '    <speechMap/>\n'
        xml += '    </net.rptools.maptool.model.Token>\n'

        # Replace placeholder '#{custom}' with added special properties
        # TODO: Find a better way to do this without using replace (entire method refactoring)
        if len(self.custom_property_map_xml) > 0:
            prop_xml = ""

            for k, v in self.custom_property_map_xml.items():
                prop_xml += self.property_xml(k, v)

            xml = str.replace(xml, "#{custom}", prop_xml)
        else:
            xml = str.replace(xml, "#{custom}", "")

        self.content_xml = xml

    def property_xml(self, name, value):

        xml = ''
        xml += '        <entry>\n'
        xml += '          <string>' + str(name).lower() + '</string>\n'
        xml += '          <net.rptools.CaseInsensitiveHashMap_-KeyValue>\n'
        xml += '            <key>' + str(name) + '</key>\n'
        xml += '            <value class="string">' + value + '</value>\n'
        xml += '            <outer-class reference="../../../.."/>\n'
        xml += '          </net.rptools.CaseInsensitiveHashMap_-KeyValue>\n'
        xml += '        </entry>\n'

        return xml

    def hp_macro_xml(self):

        self.num_macros += 1
        colorf = self.settings.value("colors/hpf")
        colorb = self.settings.value("colors/hpb")
        hpc = self.settings.value("properties/hp")
        hpm = self.settings.value("properties/hpmax")

        xml = '        <entry>\n'
        xml += '         <int>' + str(self.num_macros) + '</int>\n'
        xml += '         <net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '           <saveLocation></saveLocation>\n'
        xml += '           <index>' + str(self.num_macros) + '</index>\n'
        xml += '           <colorKey>' + colorb + '</colorKey>\n'
        xml += '           <hotKey>None</hotKey>\n'
        xml += '           <command>'

        tmp = ''

        if hpc and hpm:

            tmp += '[h:status = input(\n'
            tmp += '"dmgOrHealing|Normal Damage,Normal Healing,Temp Damage,Temp Healing,Temp Bonus,Heal Both,Reset '
            tmp += 'HP|Is the character taking damage or being healed?|LIST|SELECT=0",\n'
            tmp += '"hpChange|0|Number of Hit Points")]\n'

            tmp += '[h:abort(status)]\n'
            tmp += '\n'
            tmp += '[switch(dmgOrHealing),CODE:\n'
            tmp += 'case 0: {\n'
            tmp += '  [h:HPC = HPC - hpChange]\n'
            tmp += '  [h:HPTotal = HPC + HPT]\n'
            tmp += '  [h:bar.Health = HPTotal / HPM]\n'
            tmp += '  [r:token.name] loses [r:hpChange] hit points.\n'
            tmp += '};\n'
            tmp += 'case 1: {\n'
            tmp += '  [h:HPC = HPC + hpChange]\n'
            tmp += '  [h,if(HPC > HPM), CODE:\n'
            tmp += '  {\n'
            tmp += '    [h:HPC = HPM]\n'
            tmp += '  }\n;'
            tmp += '  {}]\n'
            tmp += '  [h:HPTotal = HPC + HPT]\n'
            tmp += '  [h:bar.Health = HPTotal / HPM]\n'
            tmp += '  [r:token.name] is healed and gains  [r:hpChange] hit points.\n'
            tmp += '};\n'
            tmp += 'case 2: {\n'
            tmp += '  [h:HPT = HPT - hpChange]\n'
            tmp += '  [h:HPTotal = HPC + HPT]\n'
            tmp += '  [h:bar.Health = HPTotal / HPM]\n'
            tmp += '  [r:token.name] loses [r:hpChange] temp hit points.\n'
            tmp += '};\n'
            tmp += 'case 3: {\n'
            tmp += '  [h:HPT = HPT + hpChange]\n'
            tmp += '  [h,if(HPT > 0), CODE:\n'
            tmp += '  {\n'
            tmp += '    [h:HPT = 0]\n'
            tmp += '  };\n'
            tmp += '  {}]\n'
            tmp += '  [h:HPTotal = HPC + HPT]\n'
            tmp += '  [h:bar.Health = HPTotal / HPM]\n'
            tmp += '  [r:token.name] is healed  [r:hpChange] temp hit points.\n'
            tmp += '};\n'
            tmp += 'case 4: {\n'
            tmp += '  [h:HPT = HPT + hpChange]\n'
            tmp += '  [h:HPTotal = HPC + HPT]\n'
            tmp += '  [h:bar.Health = HPTotal / HPM]\n'
            tmp += '  [r:token.name] gains  [r:hpChange] temp hit points.\n'
            tmp += '};\n'
            tmp += 'case 5: {\n'
            tmp += '  [h:HPT = HPT + hpChange]\n'
            tmp += '  [h,if(HPT > 0), CODE:\n'
            tmp += '  {\n'
            tmp += '    [h:HPT = 0]\n'
            tmp += '  };\n'
            tmp += '  {}]\n'
            tmp += '  [h:HPC = HPC + hpChange]\n'
            tmp += '  [h,if(HPC > HPM), CODE:\n'
            tmp += '  {\n'
            tmp += '    [h:HPC = HPM]\n'
            tmp += '  };\n'
            tmp += '  {}]\n'
            tmp += '  [h:HPTotal = HPC + HPT]\n'
            tmp += '  [h:bar.Health = HPTotal / HPM]\n'
            tmp += '  [r:token.name] is healed  [r:hpChange] normal and temp hit points.\n'
            tmp += '};\n'
            tmp += 'case 6: {\n'
            tmp += '  [h:HPC = HPM]\n'
            tmp += '  [h:HPT = 0]\n'
            tmp += '  [h:HPTotal = HPC + HPT]\n'
            tmp += '  [h:bar.Health = HPTotal / HPM]\n'
            tmp += '  [r:token.name] has been reset and is at  [r:HPC] hit points.\n'
            tmp += '};\n'
            tmp += 'default: { Unknown action }]\n'

            tmp += macros.health.gen_status_frag(hpcurr_prop=hpc, hpmax_prop=hpm)

        elif hpm:
            tmp += '[h:status = input(\n'
            tmp += '"hpChange|0|Number of Hit Points",\n'
            tmp += '"dmgOrHealing|Damage,Healing|Is the character taking damage or being healed?|RADIO|SELECT=0")]\n'
            tmp += '[h:abort(status)]\n'
            tmp += '[if(dmgOrHealing == 0),CODE:\n'
            tmp += '{\n'
            tmp += '[h:' + hpm + ' = ' + hpm + ' - hpChange]\n'
            tmp += '[r:token.name] loses [r:hpChange] hit points.\n'
            tmp += '};\n'
            tmp += '{\n'
            tmp += '[h:' + hpm + ' = ' + hpm + ' + hpChange]\n'
            tmp += '[r:token.name] gains  [r:hpChange] hit points.\n'
            tmp += '};]\n'

        elif hpc:
            tmp += '[h:status = input(\n'
            tmp += '"hpChange|0|Number of Hit Points",\n'
            tmp += '"dmgOrHealing|Damage,Healing|Is the character taking damage or being healed?|RADIO|SELECT=0")]\n'
            tmp += '[h:abort(status)]\n'
            tmp += '[if(dmgOrHealing == 0),CODE:\n'
            tmp += '{\n'
            tmp += '[h:' + hpc + ' = ' + hpc + ' - hpChange]\n'
            tmp += '[r:token.name] loses [r:hpChange] hit points.\n'
            tmp += '};\n'
            tmp += '{\n'
            tmp += '[h:' + hpc + ' = ' + hpc + ' + hpChange]\n'
            tmp += '[r:token.name] gains  [r:hpChange] hit points.\n'
            tmp += '};]\n'

        xml += html.escape(tmp)

        xml += '</command>\n'
        xml += '           <label>HP</label>\n'
        xml += '           <group>Basic</group>\n'
        xml += '           <sortby>1</sortby>\n'
        xml += '           <autoExecute>true</autoExecute>\n'
        xml += '           <includeLabel>false</includeLabel>\n'
        xml += '           <applyToTokens>true</applyToTokens>\n'
        xml += '           <fontColorKey>' + colorf + '</fontColorKey>\n'
        xml += '           <fontSize>1.00em</fontSize>\n'
        xml += '           <minWidth>53</minWidth>\n'
        xml += '           <maxWidth>53</maxWidth>\n'
        xml += '           <allowPlayerEdits>true</allowPlayerEdits>\n'
        xml += '           <toolTip></toolTip>\n'
        xml += '           <commonMacro>false</commonMacro>\n'
        xml += '           <compareGroup>true</compareGroup>\n'
        xml += '           <compareIncludeLabel>true</compareIncludeLabel>\n'
        xml += '           <compareAutoExecute>true</compareAutoExecute>\n'
        xml += '           <compareApplyToSelectedTokens>true</compareApplyToSelectedTokens>\n'
        xml += '         </net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '       </entry>\n'

        return xml

    def custom_macro_xml(self, name, group, font, background, value):

        self.num_macros += 1

        width = len(name) * 8

        xml = '        <entry>\n'
        xml += '         <int>' + str(self.num_macros) + '</int>\n'
        xml += '         <net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '           <saveLocation></saveLocation>\n'
        xml += '           <index>' + str(self.num_macros) + '</index>\n'
        xml += '           <colorKey>' + background + '</colorKey>\n'
        xml += '           <hotKey>None</hotKey>\n'
        xml += '           <command>'

        xml += html.escape(value)

        xml += '</command>\n'
        xml += '           <label>' + name + '</label>\n'
        xml += '           <group>' + group + '</group>\n'
        xml += '           <sortby></sortby>\n'
        xml += '           <autoExecute>true</autoExecute>\n'
        xml += '           <includeLabel>false</includeLabel>\n'
        xml += '           <applyToTokens>true</applyToTokens>\n'
        xml += '           <fontColorKey>' + font + '</fontColorKey>\n'
        xml += '           <fontSize>1.00em</fontSize>\n'
        xml += '           <minWidth>' + str(width) + '</minWidth>\n'
        xml += '           <maxWidth>' + str(width) + '</maxWidth>\n'
        xml += '           <allowPlayerEdits>true</allowPlayerEdits>\n'
        xml += '           <toolTip></toolTip>\n'
        xml += '           <commonMacro>false</commonMacro>\n'
        xml += '           <compareGroup>true</compareGroup>\n'
        xml += '           <compareIncludeLabel>true</compareIncludeLabel>\n'
        xml += '           <compareAutoExecute>true</compareAutoExecute>\n'
        xml += '           <compareApplyToSelectedTokens>true</compareApplyToSelectedTokens>\n'
        xml += '         </net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '       </entry>\n'

        return xml

    def roll_macro_xml(self, label, bonus, name, group, width, background, font, sortby):

        self.num_macros += 1

        found = re.search('(\+?\-?\d+)', bonus)
        if found:
            bonus = int(found.group(1))
        else:
            bonus = 0

        if bonus > 0:
            roll = 'd20 + ' + str(bonus)
        elif bonus < 0:
            roll = 'd20 - ' + str(bonus * -1)
        else:
            roll = 'd20'

        xml = '        <entry>\n'
        xml += '         <int>' + str(self.num_macros) + '</int>\n'
        xml += '         <net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '           <saveLocation></saveLocation>\n'
        xml += '           <index>' + str(self.num_macros) + '</index>\n'
        xml += '           <colorKey>' + background + '</colorKey>\n'
        xml += '           <hotKey>None</hotKey>\n'
        xml += '           <command>'
        tmp = "<table border='0' cellpadding='0' cellspacing='0' style='width:200px'>\n"
        tmp += "<tr bgcolor='" + background + "'>\n"
        tmp += "<td><span style='color:" + font + "'><b>" + name + "</b></span></td>\n"
        tmp += "</tr>\n"
        tmp += "<tr>\n"
        tmp += "<td>[e:" + roll + "]</td>\n"
        tmp += "</tr>\n"
        tmp += "</table>\n"

        xml += html.escape(tmp)

        xml += '</command>\n'
        xml += '           <label>' + label + '</label>\n'
        xml += '           <group>' + group + '</group>\n'
        xml += '           <sortby>' + sortby + '</sortby>\n'
        xml += '           <autoExecute>true</autoExecute>\n'
        xml += '           <includeLabel>false</includeLabel>\n'
        xml += '           <applyToTokens>true</applyToTokens>\n'
        xml += '           <fontColorKey>' + font + '</fontColorKey>\n'
        xml += '           <fontSize>1.00em</fontSize>\n'
        xml += '           <minWidth>' + width + '</minWidth>\n'
        xml += '           <maxWidth>' + width + '</maxWidth>\n'
        xml += '           <allowPlayerEdits>true</allowPlayerEdits>\n'
        xml += '           <toolTip>' + str(bonus) + '</toolTip>\n'
        xml += '           <commonMacro>false</commonMacro>\n'
        xml += '           <compareGroup>true</compareGroup>\n'
        xml += '           <compareIncludeLabel>true</compareIncludeLabel>\n'
        xml += '           <compareAutoExecute>true</compareAutoExecute>\n'
        xml += '           <compareApplyToSelectedTokens>true</compareApplyToSelectedTokens>\n'
        xml += '         </net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '       </entry>\n'

        return xml

    def basic_die_macro_xml(self, die):

        label = die
        name = die
        width = '31'
        group = 'Basic Dice'
        font = self.settings.value("colors/basicf")
        background = self.settings.value("colors/basicb")
        sortby = '1'

        self.num_macros += 1

        xml = '        <entry>\n'
        xml += '         <int>' + str(self.num_macros) + '</int>\n'
        xml += '         <net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '           <saveLocation></saveLocation>\n'
        xml += '           <index>' + str(self.num_macros) + '</index>\n'
        xml += '           <colorKey>' + background + '</colorKey>\n'
        xml += '           <hotKey>None</hotKey>\n'
        xml += '           <command>'
        tmp = "<table border='0' cellpadding='0' cellspacing='0' style='width:200px'>\n"
        tmp += "<tr bgcolor='" + background + "'>\n"
        tmp += "<td><span style='color:" + font + "'><b>" + name + "</b></span></td>\n"
        tmp += "</tr>\n"
        tmp += "<tr>\n"
        tmp += "<td>[e:" + die + "]</td>\n"
        tmp += "</tr>\n"
        tmp += "</table>\n"

        xml += html.escape(tmp)

        xml += '</command>\n'
        xml += '           <label>' + label + '</label>\n'
        xml += '           <group>' + group + '</group>\n'
        xml += '           <sortby>' + sortby + '</sortby>\n'
        xml += '           <autoExecute>true</autoExecute>\n'
        xml += '           <includeLabel>false</includeLabel>\n'
        xml += '           <applyToTokens>true</applyToTokens>\n'
        xml += '           <fontColorKey>' + font + '</fontColorKey>\n'
        xml += '           <fontSize>1.00em</fontSize>\n'
        xml += '           <minWidth>' + width + '</minWidth>\n'
        xml += '           <maxWidth>' + width + '</maxWidth>\n'
        xml += '           <allowPlayerEdits>true</allowPlayerEdits>\n'
        xml += '           <toolTip></toolTip>\n'
        xml += '           <commonMacro>false</commonMacro>\n'
        xml += '           <compareGroup>true</compareGroup>\n'
        xml += '           <compareIncludeLabel>true</compareIncludeLabel>\n'
        xml += '           <compareAutoExecute>true</compareAutoExecute>\n'
        xml += '           <compareApplyToSelectedTokens>true</compareApplyToSelectedTokens>\n'
        xml += '         </net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '       </entry>\n'

        return xml

    def spell_list_macro_xml(self, name, spells, width):

        font = self.settings.value("colors/specialsf")
        background = self.settings.value("colors/specialsb")

        group = 'Special'
        label = name

        self.num_macros += 1

        xml = '        <entry>\n'
        xml += '         <int>' + str(self.num_macros) + '</int>\n'
        xml += '         <net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '           <saveLocation></saveLocation>\n'
        xml += '           <index>' + str(self.num_macros) + '</index>\n'
        xml += '           <colorKey>' + background + '</colorKey>\n'
        xml += '           <hotKey>None</hotKey>\n'
        xml += '           <command>'

        # [frame("name"): {
        xml += html.escape('[frame("' + name + '"): {\n', True)
        xml += html.escape('<html>\n')
        xml += html.escape('<head>\n')
        xml += html.escape('  <title>' + name + ' ([r:token.name])</title>\n')
        xml += html.escape('</head>\n')
        xml += html.escape('<body style="padding:0 10px 0px 10px ">\n')
        xml += html.escape('<h1>')
        xml += html.escape('   <span>%s</span><br>') % name
        xml += html.escape('   <small><b>%s</b></small>') % util.clean_name(self.name)
        xml += html.escape('</h1>')

        # xml += html.escape('  <h1>' + util.clean_name(self.name) + ' (' + name + ')</h1>\n')

        spells_by_level = sorted(spells, key=lambda k: k['level'])
        current = -1
        spell_macro_count = 0

        for spell in spells_by_level:
            if int(spell['level']) > current:
                current = int(spell['level'])
                xml += html.escape('<h2>Level ' + str(spell['level']) + ' Spells</h2>\n')

            sname = spell['name']

            if spell['save'].lower() != 'none':
                spell_save = ' (CL:' + spell['casterlevel'] + ' / DC:' + spell['dc'] + ')'
            else:
                spell_save = ' (CL:' + spell['casterlevel'] + ')'

            # With Indexing
            if self.settings.value("indexing") == 'HTML':
                str_macro = '[r: macrolink("%(sname)s", "lshow@token", "none", "url=%(httpbase)s%(index)s;lname=%(sname)s", ' \
                            'currentToken())]'

                str_macro = str_macro % {'sname': sname,
                                         'httpbase': self.settings.value("httpbase"),
                                         'index': self.index_append(self.spell_html(spell))}

                xml += html.escape(str_macro)
                xml += html.escape(spell_save)
                xml += html.escape('<br>\n')

            # With Description
            elif self.settings.value("description") == 'True':
                # Put entire decription in custom property to avoid StackOverflow
                spell_key = "hl2mt_Spells_%03i" % spell_macro_count
                self.custom_property_map_xml[spell_key] = spellTmpl.gen_spell_detail(spell)

                str_macro = '<div>'
                str_macro += '    [r: macroLink("%(spell)s", "fn_detail@token", "none", '
                str_macro += '       "title=%(title)s&keys=%(keys)s", currentToken())]'
                str_macro += '    <small>%(saves)s</small>\n'
                str_macro += '</div>\n'
                str_macro = str_macro % {"spell": sname, "title": sname, "keys": spell_key, "saves": spell_save}

                xml += html.escape(str_macro)

                spell_macro_count += 1

            # No indexing
            else:
                xml += spell['name']
                if spell['save'].lower() != 'none':
                    xml += ' (CL:' + spell['casterlevel'] + ' / DC:' + spell['dc'] + ')'
                else:
                    xml += ' (CL:' + spell['casterlevel'] + ')'
                xml += '&lt;br&gt;&#xd;\n'

        # </body>
        xml += '&lt;/body&gt;&#xd;\n'
        # </html>
        xml += '&lt;/html&gt;&#xd;\n'
        # }]
        xml += '}]&#xd;\n'

        xml += '</command>\n'
        xml += '           <label>' + label + '</label>\n'
        xml += '           <group>' + group + '</group>\n'
        xml += '           <sortby>6</sortby>\n'
        xml += '           <autoExecute>true</autoExecute>\n'
        xml += '           <includeLabel>false</includeLabel>\n'
        xml += '           <applyToTokens>true</applyToTokens>\n'
        xml += '           <fontColorKey>' + font + '</fontColorKey>\n'
        xml += '           <fontSize>1.00em</fontSize>\n'
        xml += '           <minWidth>' + width + '</minWidth>\n'
        xml += '           <maxWidth>' + width + '</maxWidth>\n'
        xml += '           <allowPlayerEdits>true</allowPlayerEdits>\n'
        xml += '           <toolTip></toolTip>\n'
        xml += '           <commonMacro>false</commonMacro>\n'
        xml += '           <compareGroup>true</compareGroup>\n'
        xml += '           <compareIncludeLabel>true</compareIncludeLabel>\n'
        xml += '           <compareAutoExecute>true</compareAutoExecute>\n'
        xml += '           <compareApplyToSelectedTokens>true</compareApplyToSelectedTokens>\n'
        xml += '         </net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '       </entry>\n'

        return xml

    @staticmethod
    def spell_html(spell):

        str_html = "<h2>" + spell['name']

        if spell['save'].lower() != 'none':
            str_html += '<small> (CL:' + spell['casterlevel'] + ' / DC:' + spell['dc'] + ') </small>'
        else:
            str_html += '<small> (CL:' + spell['casterlevel'] + ') </small>'

        str_html += '</h2><hr style="margin: 0px 0 10px 0">'

        # <b>School</b>
        str_html += '<b>Level</b> ' + spell['level'] + '<br>'

        # <b>School</b>
        str_html += '<b>School</b> ' + spell['schooltext'] + '<br>'

        # <b>Casting Time</b> <br>
        str_html += '<b>Casting Time</b> ' + spell['casttime'] + '<br>'

        # <b>Components</b>
        str_html += '<b>Components</b> ' + spell['componenttext'] + '<br>'

        # <b>Range</b>
        if spell['range']:
            str_html += '<b>Range</b> ' + spell['range'] + '<br>'

        # <b>Area</b>
        if spell['area']:
            str_html += '<b>Area</b> ' + spell['area'] + '<br>'

        # <b>Target</b>
        if spell['target']:
            str_html += '<b>Target</b> ' + spell['target'] + '<br>'

        # <b>Duration</b>
        if spell['duration']:
            str_html += '<b>Duration</b> ' + spell['duration'] + '<br>'

        # <b>Effect</b>
        if spell['effect']:
            str_html += '<b>Effect</b> ' + spell['effect'] + '<br>'

        # <b>Saving Throw</b>
        str_html += '<b>Saving Throw</b> ' + spell['save'] + '<br>'

        # <b>Spell Resistance</b>
        str_html += '<b>Spell Resistance</b> ' + spell['resist'] + '<br>'

        # description
        # str_html += '<br>\n'

        str_html += str.replace(spell['description'], '\n', '<br>')

        # str_html += '<br>\n'
        # str_html += '<br>\n'
        # str_html += '<br>\n'
        # str_html += '<hr>\n'

        return str_html

    def list_macro_xml(self, name, items, width):
        font = self.settings.value("colors/specialsf")
        background = self.settings.value("colors/specialsb")
        group = 'Special'
        label = name

        self.num_macros += 1

        xml = '        <entry>\n'
        xml += '         <int>' + str(self.num_macros) + '</int>\n'
        xml += '         <net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '           <saveLocation></saveLocation>\n'
        xml += '           <index>' + str(self.num_macros) + '</index>\n'
        xml += '           <colorKey>' + background + '</colorKey>\n'
        xml += '           <hotKey>None</hotKey>\n'
        xml += '           <command>'

        # #############################################################
        # Create specific macro
        # #############################################################
        xml += html.escape('\n[frame("' + name + '"): {')
        xml += html.escape('\n  <html>')
        xml += html.escape('\n      <head>')
        xml += html.escape('\n          <title>%s</title>' % name)
        xml += html.escape('\n      </head>')
        xml += html.escape('\n      <body style="padding:0 10px 0 10px">')
        xml += html.escape('\n          <h1>')
        xml += html.escape('\n              <span>%s</span><br>') % name
        xml += html.escape('\n              <small><b>%s</b></small>') % util.clean_name(self.name)
        xml += html.escape('\n          </h1>')
        # xml += html.escape('\n          <h1>%s %s</h1>' % (util.clean_name(self.name), name))

        list_macro_count = 0

        for k, v in sorted(items.items()):
            k = str.replace(k, "[", "(")
            k = str.replace(k, "]", ")")
            k = str.replace(k, "'", "&#x00b4;")  # dca: Safe Name

            if v is None:
                xml += k
                xml += '<br>'
                continue

            # With Indexing
            if self.settings.value("indexing") == 'HTML':
                # [r: macroLink("k", "lshow@token", "none", "url=url;lname=k", currentToken())
                xml += '[r: macrolink(&quot;' + k + '&quot;, &quot;lshow@token&quot;, &quot;none&quot;, &quot;url=' + \
                       self.settings.value("httpbase") + self.index_append(util.pretty_html(v)) + ';lname=' + \
                       k + '&quot;, currentToken())]'

            # With Description
            elif self.settings.value("description") == 'True':
                # Put entire decription in custom property
                any_key = "hl2mt_%s_%03i" % (name, list_macro_count)

                # Detail Template
                detail_tmpl = '\n<div style="padding: 0 10px 0 10px;">'
                detail_tmpl += '\n  <h2>'
                detail_tmpl += '\n      <span>%s</span><br>' % k
                detail_tmpl += '\n      <small><b>%s</b></small>' % self.name
                detail_tmpl += '\n  </h2>'
                detail_tmpl += '\n  <span>\n%s\n</span>' % util.pretty_html(v)
                detail_tmpl += '\n</div>'

                self.custom_property_map_xml[any_key] = html.escape(detail_tmpl)  # spellTmpl.gen_spell_detail(spell)

                macro_link = '<div>'
                macro_link += '    [r: macroLink("%(name)s", "fn_detail@token", "none", '
                macro_link += '       "title=%(title)s&keys=%(keys)s", currentToken())]'
                macro_link += '</div>\n'
                macro_link = macro_link % {"name": k, "title": k, "keys": any_key}

                xml += html.escape(macro_link)

                list_macro_count += 1

            # No indexing
            else:
                xml += k

        xml += html.escape('\n      </body>')
        xml += html.escape('\n  </html>')
        xml += html.escape('\n}]\n')

        # #############################################################
        #
        # #############################################################

        xml += '</command>\n'
        xml += '           <label>' + label + '</label>\n'
        xml += '           <group>' + group + '</group>\n'
        xml += '           <sortby>6</sortby>\n'
        xml += '           <autoExecute>true</autoExecute>\n'
        xml += '           <includeLabel>false</includeLabel>\n'
        xml += '           <applyToTokens>true</applyToTokens>\n'
        xml += '           <fontColorKey>' + font + '</fontColorKey>\n'
        xml += '           <fontSize>1.00em</fontSize>\n'
        xml += '           <minWidth>' + width + '</minWidth>\n'
        xml += '           <maxWidth>' + width + '</maxWidth>\n'
        xml += '           <allowPlayerEdits>true</allowPlayerEdits>\n'
        xml += '           <toolTip></toolTip>\n'
        xml += '           <commonMacro>false</commonMacro>\n'
        xml += '           <compareGroup>true</compareGroup>\n'
        xml += '           <compareIncludeLabel>true</compareIncludeLabel>\n'
        xml += '           <compareAutoExecute>true</compareAutoExecute>\n'
        xml += '           <compareApplyToSelectedTokens>true</compareApplyToSelectedTokens>\n'
        xml += '         </net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '       </entry>\n'

        return xml

    def items_macro_xml(self):

        font = self.settings.value("colors/specialsf")
        background = self.settings.value("colors/specialsb")
        group = 'Special'
        label = 'Inventory'
        width = '75'

        self.num_macros += 1

        xml = '        <entry>\n'
        xml += '         <int>' + str(self.num_macros) + '</int>\n'
        xml += '         <net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '           <saveLocation></saveLocation>\n'
        xml += '           <index>' + str(self.num_macros) + '</index>\n'
        xml += '           <colorKey>' + background + '</colorKey>\n'
        xml += '           <hotKey>None</hotKey>\n'
        xml += '           <command>'

        tmp = '\n[frame("Inventory"): {'
        tmp += '\n  <html>'
        tmp += '\n  <head>'
        tmp += '\n      <title>Inventory</title>'
        tmp += '\n  </head>'
        tmp += '\n  <body style="padding:0 10px 0 10px">'
        tmp += '\n      <h1>'
        tmp += '\n          <span>Inventory</span><br>'
        tmp += '\n          <small><b>%s</b></small>' % util.clean_name(self.name)
        tmp += '\n      </h1>'

        for item in sorted(self.items, key=lambda k: k['name']):
            name = item['name']
            name = str.replace(name, "'", "")
            name = str.replace(name, "[", "")
            name = str.replace(name, "]", "")

            tmp += '<div>'
            tmp += name

            if len(item['value']) == 0:
                item['value'] = '0 gp'

            if int(item['num']) > 1:
                tmp += ' (x' + item['num'] + ', ' + item['value'] + ')'
            else:
                tmp += ' (' + item['value'] + ')'

            tmp += '</div>'

        if len(tmp) > 0:
            tmp += '    <div><br><b>Money: </b>&nbsp;'

        if int(self.pp) > 0:
            tmp += self.pp + 'pp &nbsp;'
        if int(self.gp) > 0:
            tmp += self.gp + 'gp &nbsp;'
        if int(self.sp) > 0:
            tmp += self.sp + 'sp &nbsp;'
        if int(self.cp) > 0:
            tmp += self.cp + 'cp'

        tmp += '\n      </div>'
        tmp += '\n      </body>\n'
        tmp += '\n  </html>\n'
        tmp += '}]'

        xml += html.escape(tmp)

        xml += '</command>\n'
        xml += '           <label>' + label + '</label>\n'
        xml += '           <group>' + group + '</group>\n'
        xml += '           <sortby>6</sortby>\n'
        xml += '           <autoExecute>true</autoExecute>\n'
        xml += '           <includeLabel>false</includeLabel>\n'
        xml += '           <applyToTokens>true</applyToTokens>\n'
        xml += '           <fontColorKey>' + font + '</fontColorKey>\n'
        xml += '           <fontSize>1.00em</fontSize>\n'
        xml += '           <minWidth>' + width + '</minWidth>\n'
        xml += '           <maxWidth>' + width + '</maxWidth>\n'
        xml += '           <allowPlayerEdits>true</allowPlayerEdits>\n'
        xml += '           <toolTip></toolTip>\n'
        xml += '           <commonMacro>false</commonMacro>\n'
        xml += '           <compareGroup>true</compareGroup>\n'
        xml += '           <compareIncludeLabel>true</compareIncludeLabel>\n'
        xml += '           <compareAutoExecute>true</compareAutoExecute>\n'
        xml += '           <compareApplyToSelectedTokens>true</compareApplyToSelectedTokens>\n'
        xml += '         </net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '       </entry>\n'

        return xml

    def gm_macro_xml(self, label, macro):

        font = self.settings.value("colors/gmf")
        background = self.settings.value("colors/gmb")
        group = 'GM'
        label = label
        width = '70'

        self.num_macros += 1

        xml = '        <entry>\n'
        xml += '         <int>' + str(self.num_macros) + '</int>\n'
        xml += '         <net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '           <saveLocation></saveLocation>\n'
        xml += '           <index>' + str(self.num_macros) + '</index>\n'
        xml += '           <colorKey>' + background + '</colorKey>\n'
        xml += '           <hotKey>None</hotKey>\n'
        xml += '           <command>'

        xml += html.escape(macro)

        xml += '</command>\n'
        xml += '           <label>' + label + '</label>\n'
        xml += '           <group>' + group + '</group>\n'
        xml += '           <sortby>6</sortby>\n'
        xml += '           <autoExecute>true</autoExecute>\n'
        xml += '           <includeLabel>false</includeLabel>\n'
        xml += '           <applyToTokens>true</applyToTokens>\n'
        xml += '           <fontColorKey>' + font + '</fontColorKey>\n'
        xml += '           <fontSize>1.00em</fontSize>\n'
        xml += '           <minWidth>' + width + '</minWidth>\n'
        xml += '           <maxWidth>' + width + '</maxWidth>\n'
        xml += '           <allowPlayerEdits>true</allowPlayerEdits>\n'
        xml += '           <toolTip></toolTip>\n'
        xml += '           <commonMacro>false</commonMacro>\n'
        xml += '           <compareGroup>true</compareGroup>\n'
        xml += '           <compareIncludeLabel>true</compareIncludeLabel>\n'
        xml += '           <compareAutoExecute>true</compareAutoExecute>\n'
        xml += '           <compareApplyToSelectedTokens>true</compareApplyToSelectedTokens>\n'
        xml += '         </net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '       </entry>\n'

        return xml

    def list_show_macro_xml(self):

        font = self.settings.value("colors/subf")
        background = self.settings.value("colors/subb")
        group = 'Submacros'
        width = '35'
        label = 'lshow'

        self.num_macros += 1

        xml = '        <entry>\n'
        xml += '         <int>' + str(self.num_macros) + '</int>\n'
        xml += '         <net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '           <saveLocation></saveLocation>\n'
        xml += '           <index>' + str(self.num_macros) + '</index>\n'
        xml += '           <colorKey>' + background + '</colorKey>\n'
        xml += '           <hotKey>None</hotKey>\n'
        xml += '           <command>'

        # [frame("Show Details"): {
        xml += '[frame(&quot;Show Details&quot;): {&#xd;\n'
        # <html>
        xml += '&lt;html&gt;&#xd;\n'
        # <head>
        xml += '&lt;head&gt;&#xd;\n'
        # <title>Show Details</title>
        xml += '&lt;title&gt;Show Details&lt;/title&gt;&#xd;\n'
        # </head>
        xml += '&lt;/head&gt;&#xd;\n'
        # <body>
        xml += '&lt;body&gt;&#xd;\n'
        # [h:lname = getStrProp(macro.args, "lname")]
        xml += '[h:lname = getStrProp(macro.args, &quot;lname&quot;)]\n'
        # <h1><u>[r:lname]</u></h1>
        xml += '&lt;h1&gt;&lt;u&gt;[r:lname]&lt;/u&gt;&lt;/h1&gt;&#xd;\n'

        # [h:url = getStrProp(macro.args, "url")]
        xml += '[h:url = getStrProp(macro.args, &quot;url&quot;)]\n'
        # [r: requestURL(url)]
        xml += '[r: requestURL(url)]\n'

        # </body>
        xml += '&lt;/body&gt;&#xd;\n'
        # </html>
        xml += '&lt;/html&gt;&#xd;\n'
        # }]
        xml += '}]&#xd;\n'

        xml += '</command>\n'
        xml += '           <label>' + label + '</label>\n'
        xml += '           <group>' + group + '</group>\n'
        xml += '           <sortby>6</sortby>\n'
        xml += '           <autoExecute>true</autoExecute>\n'
        xml += '           <includeLabel>false</includeLabel>\n'
        xml += '           <applyToTokens>true</applyToTokens>\n'
        xml += '           <fontColorKey>' + font + '</fontColorKey>\n'
        xml += '           <fontSize>1.00em</fontSize>\n'
        xml += '           <minWidth>' + width + '</minWidth>\n'
        xml += '           <maxWidth>' + width + '</maxWidth>\n'
        xml += '           <allowPlayerEdits>true</allowPlayerEdits>\n'
        xml += '           <toolTip></toolTip>\n'
        xml += '           <commonMacro>false</commonMacro>\n'
        xml += '           <compareGroup>true</compareGroup>\n'
        xml += '           <compareIncludeLabel>true</compareIncludeLabel>\n'
        xml += '           <compareAutoExecute>true</compareAutoExecute>\n'
        xml += '           <compareApplyToSelectedTokens>true</compareApplyToSelectedTokens>\n'
        xml += '         </net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '       </entry>\n'

        return xml

    def init_macro_xml(self, roll=True):

        font = self.settings.value("colors/initf")
        background = self.settings.value("colors/initb")
        group = '00 - Initiative'  # 'Basic'
        width = '120'  # '25'
        name = 'Initiative'

        if roll:
            label = 'Roll Init'
        else:
            font, background = background, font  # Swap colors
            label = 'Add to Init'

        self.num_macros += 1
        bonus = str.replace(self.initiative, '+', '')

        if self.custom_property_map_xml["hl2mt_initiative"]:
            bonus = "hl2mt_initiative"

        xml = '<entry>\n'
        xml += '    <int>' + str(self.num_macros) + '</int>\n'
        xml += '    <net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '        <saveLocation></saveLocation>\n'
        xml += '        <index>' + str(self.num_macros) + '</index>\n'
        xml += '        <colorKey>' + background + '</colorKey>\n'
        xml += '        <hotKey>None</hotKey>\n'
        xml += '        <command>'

        # tmp = '[h: Roll = d20]\n'
        tmp = "<table border='0' cellpadding='0' cellspacing='0' style='width:200px'>\n"
        tmp += "    <tr bgcolor='" + background + "'>\n"
        tmp += "        <td><span style='color:" + font + "'><b>" + name + "</b></span></td>\n"
        tmp += "    </tr>\n"
        tmp += "    <tr>\n"

        if roll:
            tmp += "    <td>[e: InitRoll = d20 + " + bonus + "]</td>\n"
        else:
            tmp += "    <td>[r: InitRoll = TotalRoll]</td>\n"

        tmp += "    </tr>\n"
        tmp += "</table>\n"

        tmp += '[h: addToInitiative()]\n'
        tmp += '[h: setInitiative(InitRoll)]\n'
        tmp += '[h: sortInitiative()]\n'

        xml += html.escape(tmp)

        xml += '        </command>\n'

        xml += '        <label>' + label + '</label>\n'
        xml += '        <group>' + group + '</group>\n'
        # xml += '        <sortby>6</sortby>\n'
        xml += '        <sortby>%i</sortby>\n' % self.num_macros
        xml += '        <autoExecute>true</autoExecute>\n'
        xml += '        <includeLabel>false</includeLabel>\n'
        xml += '        <applyToTokens>true</applyToTokens>\n'
        xml += '        <fontColorKey>' + font + '</fontColorKey>\n'
        xml += '        <fontSize>1.00em</fontSize>\n'
        xml += '        <minWidth>' + width + '</minWidth>\n'
        xml += '        <maxWidth>' + width + '</maxWidth>\n'
        xml += '        <allowPlayerEdits>false</allowPlayerEdits>\n'
        xml += '        <toolTip>' + bonus + '</toolTip>\n'
        xml += '        <commonMacro>false</commonMacro>\n'
        xml += '        <compareGroup>true</compareGroup>\n'
        xml += '        <compareIncludeLabel>true</compareIncludeLabel>\n'
        xml += '        <compareAutoExecute>true</compareAutoExecute>\n'
        xml += '        <compareApplyToSelectedTokens>true</compareApplyToSelectedTokens>\n'
        xml += '    </net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '</entry>\n'

        return xml

    def weapon_macro_xml(self, name, attack, damage, crit):

        font = self.settings.value("colors/attacksf")
        background = self.settings.value("colors/attacksb")
        full_font = self.settings.value("colors/fullf")
        full_background = self.settings.value("colors/fullb")

        group = 'Attacks'
        width = '120'

        regex = re.search('(\d+)\s*\-\s*(\d+)', crit)
        if regex:
            crit_low = regex.group(1)
            crit_high = regex.group(2)
        else:
            crit_low = "20"
            crit_high = "20"

        regex = re.compile('([\+\-]\d+)')
        results = []
        # Check to see if we have something like +8 or -2 or +8/+4
        if regex.match(attack):
            results = regex.findall(attack)

        # First we create a normal to-hit macro using the first number in the +8/+4 results
        if len(results) > 0:
            mod = results[0]
            mod = int(mod)
            if mod > 0:
                roll = " + " + str(mod)
            elif mod < 0:
                roll = " - " + str(mod)
            else:
                roll = ""
        else:
            roll = ""

        self.num_macros += 1
        self.weapon_sort += 1

        xml = '        <entry>\n'
        xml += '         <int>' + str(self.num_macros) + '</int>\n'
        xml += '         <net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '           <saveLocation></saveLocation>\n'
        xml += '           <index>' + str(self.num_macros) + '</index>\n'
        xml += '           <colorKey>' + background + '</colorKey>\n'
        xml += '           <hotKey>None</hotKey>\n'
        xml += '           <command>'

        tmp = "[h: roll = d20]\n"
        tmp += "[h,if(roll >= " + crit_low + " && roll <= " + crit_high + "): color=\"red\";color=\"blue\"]\n"

        tmp += "\n<table border='1' cellpadding='0' cellspacing='0' style='width:200px'>"
        tmp += "\n  <tr bgcolor='" + background + "'>"
        tmp += "\n      <td><span style='color:" + font + "'><b>" + name + "(" + crit + ")</b></span></td>"
        tmp += "\n      <td><span style='color:" + font + "'><b>Damage</b></span></td>"
        tmp += "\n  </tr>"
        tmp += "\n  <tr>"
        tmp += "\n      <td>"
        tmp += "\n          <font color=[r: color]>"
        tmp += "\n              [e: roll" + roll + "]"
        tmp += "\n              [r, if(roll >= " + crit_low + " && roll <= " + crit_high + "): \"<b>Critical!</b>\"]"
        tmp += "\n          </font>"
        tmp += "\n      </td>"
        tmp += "\n      <td>"
        tmp += "\n          <font color=[r: color]>"
        # #############################################################
        if re.search('\d*d\d+', damage):
            tmp += "[e:" + damage + "]"
        else:
            tmp += "" + damage + ""
        # #############################################################
        tmp += "\n            </font>"
        tmp += "\n        </td>"
        tmp += "\n    </tr>"
        tmp += "\n</table>\n"

        xml += html.escape(tmp)

        xml += '</command>\n'
        xml += '           <label>' + name + '</label>\n'
        xml += '           <group>' + group + '</group>\n'
        xml += '           <sortby>' + str(self.weapon_sort) + '</sortby>\n'
        xml += '           <autoExecute>true</autoExecute>\n'
        xml += '           <includeLabel>false</includeLabel>\n'
        xml += '           <applyToTokens>true</applyToTokens>\n'
        xml += '           <fontColorKey>' + font + '</fontColorKey>\n'
        xml += '           <fontSize>1.00em</fontSize>\n'
        xml += '           <minWidth>' + width + '</minWidth>\n'
        xml += '           <maxWidth>' + width + '</maxWidth>\n'
        xml += '           <allowPlayerEdits>true</allowPlayerEdits>\n'
        xml += '           <toolTip>Single Attack</toolTip>\n'
        xml += '           <commonMacro>false</commonMacro>\n'
        xml += '           <compareGroup>true</compareGroup>\n'
        xml += '           <compareIncludeLabel>true</compareIncludeLabel>\n'
        xml += '           <compareAutoExecute>true</compareAutoExecute>\n'
        xml += '           <compareApplyToSelectedTokens>true</compareApplyToSelectedTokens>\n'
        xml += '         </net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '       </entry>\n'

        # Next, if we have multiple attacks, create a full attack macro
        if len(results) > 1:

            self.weapon_sort += 1
            self.num_macros += 1

            xml += '        <entry>\n'
            xml += '         <int>' + str(self.num_macros) + '</int>\n'
            xml += '         <net.rptools.maptool.model.MacroButtonProperties>\n'
            xml += '           <saveLocation></saveLocation>\n'
            xml += '           <index>' + str(self.num_macros) + '</index>\n'
            xml += '           <colorKey>' + full_background + '</colorKey>\n'
            xml += '           <hotKey>None</hotKey>\n'
            xml += '           <command>'

            tmp = "<table border='1' cellpadding='0' cellspacing='0' style='width:200px'>\n"
            tmp += "<tr bgcolor='" + full_background + "'>\n"
            tmp += "<td><span style='color:" + full_font + "'><b>" + name + "(" + crit + ")</b></span></td>\n"
            tmp += "<td><span style='color:" + full_font + "'><b>Damage</b></span></td>\n"
            tmp += "</tr>\n"

            for mod in results:
                mod = int(mod)
                if mod > 0:
                    roll = " + " + str(mod)
                elif mod < 0:
                    roll = " - " + str(mod)
                else:
                    roll = ""

                tmp += "[h: roll = d20]\n"
                tmp += "[h,if(roll >= " + crit_low + " && roll <= " + crit_high + "): color=\"red\";color=\"blue\"]"

                tmp += "\n<tr>"
                tmp += "\n  <td>"
                tmp += "\n      <font color=[r: color]>"
                tmp += "\n         [e: roll" + roll + "]"
                tmp += "\n         [r, if(roll >= " + crit_low + " && roll <= " + crit_high + "): \"<b>Critical!</b>\"]"
                tmp += "\n      </font>"
                tmp += "\n</td>"

                if re.search('\d*d\d+', damage):
                    tmp += "<td><font color=[r: color]>[e:" + damage + "]</font></td>\n"
                else:
                    tmp += "<td><font color=[r: color]>" + damage + "</font></td>\n"

                tmp += "</tr>\n"

            tmp += "</table>\n"

            xml += html.escape(tmp)

            xml += '</command>\n'
            xml += '           <label>' + name + '</label>\n'
            xml += '           <group>' + group + '</group>\n'
            xml += '           <sortby>' + str(self.weapon_sort) + '</sortby>\n'
            xml += '           <autoExecute>true</autoExecute>\n'
            xml += '           <includeLabel>false</includeLabel>\n'
            xml += '           <applyToTokens>true</applyToTokens>\n'
            xml += '           <fontColorKey>' + full_font + '</fontColorKey>\n'
            xml += '           <fontSize>1.00em</fontSize>\n'
            xml += '           <minWidth>' + width + '</minWidth>\n'
            xml += '           <maxWidth>' + width + '</maxWidth>\n'
            xml += '           <allowPlayerEdits>true</allowPlayerEdits>\n'
            xml += '           <toolTip>Full Attack</toolTip>\n'
            xml += '           <commonMacro>false</commonMacro>\n'
            xml += '           <compareGroup>true</compareGroup>\n'
            xml += '           <compareIncludeLabel>true</compareIncludeLabel>\n'
            xml += '           <compareAutoExecute>true</compareAutoExecute>\n'
            xml += '           <compareApplyToSelectedTokens>true</compareApplyToSelectedTokens>\n'
            xml += '         </net.rptools.maptool.model.MacroButtonProperties>\n'
            xml += '       </entry>\n'

        return xml

    def charsheet_macro_xml(self):

        font = self.settings.value("colors/sheetf")
        background = self.settings.value("colors/sheetb")
        group = 'Special'
        label = 'Sheet'
        width = '75'
        url = self.settings.value("httpbase")

        self.num_macros += 1

        xml = '        <entry>\n'
        xml += '         <int>' + str(self.num_macros) + '</int>\n'
        xml += '         <net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '           <saveLocation></saveLocation>\n'
        xml += '           <index>' + str(self.num_macros) + '</index>\n'
        xml += '           <colorKey>' + background + '</colorKey>\n'
        xml += '           <hotKey>None</hotKey>\n'
        xml += '           <command>'

        tmp = '\n'

        if self.settings.value("indexing") == 'HTML':
            tmp += '            [frame("Character Sheet"): {\n'
            tmp += '                [r: requestURL("' + url + self.html_filename + '")]\n'
            tmp += '            }]\n'

        elif self.settings.value("description") == 'True':
            hl2mt_statblock = re.sub(r"<meta http-equiv.*?>", '', self.html_statblock.decode())
            hl2mt_statblock = hl2mt_statblock.replace('[', '(')
            hl2mt_statblock = hl2mt_statblock.replace(']', ')')
            hl2mt_statblock = hl2mt_statblock.replace('<body>', '<body style="padding:10px">')

            self.custom_property_map_xml["hl2mt_statblock"] = html.escape(hl2mt_statblock)

            tmp += '            [frame("Statblock"): {\n'
            tmp += '                [r: getProperty("hl2mt_statblock")]\n'  # dca: HL Statblock
            tmp += '            }]\n'

        xml += html.escape(tmp)

        xml += '            </command>\n'

        xml += '            <label>' + label + '</label>\n'
        xml += '            <group>' + group + '</group>\n'
        xml += '            <sortby>1</sortby>\n'
        xml += '            <autoExecute>true</autoExecute>\n'
        xml += '            <includeLabel>false</includeLabel>\n'
        xml += '            <applyToTokens>true</applyToTokens>\n'
        xml += '            <fontColorKey>' + font + '</fontColorKey>\n'
        xml += '            <fontSize>1.00em</fontSize>\n'
        xml += '            <minWidth>' + width + '</minWidth>\n'
        xml += '            <maxWidth>' + width + '</maxWidth>\n'
        xml += '            <allowPlayerEdits>true</allowPlayerEdits>\n'
        xml += '            <toolTip></toolTip>\n'
        xml += '            <commonMacro>false</commonMacro>\n'
        xml += '            <compareGroup>true</compareGroup>\n'
        xml += '            <compareIncludeLabel>true</compareIncludeLabel>\n'
        xml += '            <compareAutoExecute>true</compareAutoExecute>\n'
        xml += '            <compareApplyToSelectedTokens>true</compareApplyToSelectedTokens>\n'
        xml += '        </net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '    </entry>\n'

        return xml

    def make_pog(self, image_name):

        # im = Image.open(str(image_name))
        # size = (128, 128)
        # im.thumbnail(size, Image.ANTIALIAS)

        im = Image.open(str(image_name))

        if (im.size[0] > 300 or im.size[1] > 300):
            size = (256, 256)  # resize POG to 256x256max
            im.thumbnail(size, Image.ANTIALIAS)
        else:
            size = im.size
            im.thumbnail(size, Image.NONE)

        output = io.BytesIO()
        im.save(output, 'png')

        self.pog_md5 = hashlib.md5(output.getvalue()).hexdigest()
        output.close()
        self.pog_asset = self.pog_md5 + '.png'
        self.pog_xml = '<net.rptools.maptool.model.Asset>\n  <id>\n    <id>' + self.pog_md5 + \
                       '</id>\n  </id>\n  <name>' + self.name + \
                       '</name>\n  <extension>png</extension>\n  <image/>\n</net.rptools.maptool.model.Asset>\n'
        self.pog = im

    def make_portrait(self, image_name):
        # im = Image.open(str(image_name))
        # size = (200, 200)
        # im.thumbnail(size, Image.ANTIALIAS)

        im = Image.open(str(image_name))

        if (im.size[0] > 400 or im.size[1] > 400):
            size = (400, 400)  # resize portrait to 400x400
            im.thumbnail(size, Image.ANTIALIAS)
        else:
            size = im.size
            im.thumbnail(size, Image.NONE)

        output = io.BytesIO()
        im.save(output, 'png')
        self.portrait_md5 = hashlib.md5(output.getvalue()).hexdigest()
        output.close()
        self.portrait_asset = self.portrait_md5 + '.png'
        self.portrait_xml = '<net.rptools.maptool.model.Asset>\n  <id>\n    <id>' + self.portrait_md5 + \
                            '</id>\n  </id>\n  <name>' + self.name + \
                            '</name>\n  <extension>png</extension>\n  <image/>\n</net.rptools.maptool.model.Asset>\n'
        self.portrait = im

    def make_thumbnail(self):
        pass
        #####
        # dead code... unecessaary processing.
        #####
        # size = 50, 50  # TODO: Fix-it to use existing image resolution.
        # im = self.pog.copy()
        # im.thumbnail(size, Image.ANTIALIAS)
        # self.thumbnail = im
        self.thumbnail = self.portrait

    def index_append(self, value):

        if not value in self.values:
            self.values.append(value)

        return hashlib.sha224(value.encode('utf-8')).hexdigest() + '.html'
