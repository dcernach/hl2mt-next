import re
import string
import hashlib
import Image
import StringIO
import cgi
from PyQt4.QtCore import *


class Pathfinder:
    """The Pathfinder class parses a Hero Lab character and converts it into a Maptool token"""

    def __init__(self, name, xml):
        self.name = str(name.toUtf8())
        self.xml = xml
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
        self.items = []
        self.specials = {}
        self.itempowers = {}
        self.spells = []
        self.spells_memorized = []
        self.spells_known = []
        self.values = []
        self.properties_xml = '<map>\n  <entry>\n    <string>version</string>\n    <string>1.3.b87</string>\n' + \
                              '  </entry>\n</map>'
        self.settings = QSettings
        self.size_map = {'fine': 'fwABAc1lFSoBAAAAKgABAQ==', 'diminutive': 'fwABAc1lFSoCAAAAKgABAQ==',
                         'tiny': 'fwABAc5lFSoDAAAAKgABAA==', 'small': 'fwABAc5lFSoEAAAAKgABAA==',
                         'medium': 'fwABAc9lFSoFAAAAKgABAQ==', 'large': 'fwABAdBlFSoGAAAAKgABAA==',
                         'huge': 'fwABAdBlFSoHAAAAKgABAA==', 'gargantuan': 'fwABAdFlFSoIAAAAKgABAQ==',
                         'colossal': 'fwABAeFlFSoJAAAAKgABAQ=='}

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

    def pretty_html(self, text):
        text = string.replace(text, '\n', '<br>')
        text = string.replace(text, 'Benefit:', '<b>Benefit:</b>')
        text = string.replace(text, 'Special:', '<b>Special:</b>')
        text = string.replace(text, 'Requirement:', '<b>Requirement:</b>')
        text = string.replace(text, 'Requirements:', '<b>Requirements:</b>')
        text = string.replace(text, 'Prerequisite:', '<b>Prerequisite:</b>')
        text = string.replace(text, 'Prerequisites:', '<b>Prerequisites:</b>')
        text = string.replace(text, 'Normal:', '<b>Normal:</b>')
        return text

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

    def make_content_xml(self):
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
        xml += '    <propertyType>' + self.settings.value("properties/propname").toString() + '</propertyType>\n'
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
        if self.vision_dark and self.settings.value("vision").toBool():
            text = 'Darkvision' + str(self.vision_dark)
        if self.vision_dark and self.settings.value("vision").toBool() and self.vision_lowlight:
            text += ' and Lowlight'

        xml += '    <sightType>' + text + '</sightType>\n'
        xml += '    <hasSight>true</hasSight>\n'
        xml += '    <state/>\n'
        xml += '    <propertyMapCI>\n'
        xml += '      <store>\n'

        xml += self.property_xml(self.settings.value("properties/strength").toString(), self.attrib_scores['Strength'])
        xml += self.property_xml(self.settings.value("properties/dexterity").toString(), self.attrib_scores['Dexterity'])
        xml += self.property_xml(self.settings.value("properties/constitution").toString(), self.attrib_scores['Constitution'])
        xml += self.property_xml(self.settings.value("properties/intelligence").toString(), self.attrib_scores['Intelligence'])
        xml += self.property_xml(self.settings.value("properties/wisdom").toString(), self.attrib_scores['Wisdom'])
        xml += self.property_xml(self.settings.value("properties/charisma").toString(), self.attrib_scores['Charisma'])
        xml += self.property_xml(self.settings.value("properties/race").toString(), self.race)
        xml += self.property_xml(self.settings.value("properties/alignment").toString(), self.alignment)
        xml += self.property_xml(self.settings.value("properties/name").toString(), self.name)
        xml += self.property_xml(self.settings.value("properties/player").toString(), self.player)
        xml += self.property_xml(self.settings.value("properties/hp").toString(), self.hpc)
        xml += self.property_xml(self.settings.value("properties/hpmax").toString(), self.hpm)
        xml += self.property_xml(self.settings.value("properties/speed").toString(), self.movement)
        xml += self.property_xml(self.settings.value("properties/reach").toString(), self.reach)
        xml += self.property_xml(self.settings.value("properties/ac").toString(), self.ac)
        xml += self.property_xml(self.settings.value("properties/acflat").toString(), self.ac_flat)
        xml += self.property_xml(self.settings.value("properties/actouch").toString(), self.ac_touch)
        xml += self.property_xml(self.settings.value("properties/cmd").toString(), self.cmd)
        xml += self.property_xml(self.settings.value("properties/cmdflat").toString(), self.cmd_flat)
        xml += self.property_xml(self.settings.value("properties/melee").toString(), self.atk_melee)
        xml += self.property_xml(self.settings.value("properties/ranged").toString(), self.atk_ranged)

        xml += '      </store>\n'
        xml += '    </propertyMapCI>\n'

        xml += '    <macroPropertiesMap>\n'

        if self.settings.value("indexing").toString() == 'HTML':
            xml += self.charsheet_macro_xml()

        if self.settings.value("hp").toBool():
            xml += self.hp_macro_xml()

        colorf = self.settings.value("colors/savesf").toString()
        colorb = self.settings.value("colors/savesb").toString()
        xml += self.roll_macro_xml('Ref', self.saves['Ref'], 'Reflex Save', 'Basic', '25',
                                   colorb, colorf, '3')
        xml += self.roll_macro_xml('Will', self.saves['Will'], 'Willpower Save', 'Basic', '25',
                                   colorb, colorf, '3')
        xml += self.roll_macro_xml('Fort', self.saves['Fort'], 'Fortitude Save', 'Basic', '25',
                                   colorb, colorf, '3')
        colorf = self.settings.value("colors/attacksf").toString()
        colorb = self.settings.value("colors/attacksb").toString()
        xml += self.roll_macro_xml('Melee', self.atk_melee, 'Basic Melee', 'Basic', '35',
                                   colorb, colorf, '2')
        xml += self.roll_macro_xml('Ranged', self.atk_ranged, 'Basic Ranged', 'Basic', '45',
                                   colorb, colorf, '2')
        colorf = self.settings.value("colors/cmbf").toString()
        colorb = self.settings.value("colors/cmbb").toString()
        xml += self.roll_macro_xml('CMB', self.cmb, 'Basic CMB', 'Basic', '25',
                                   colorb, colorf, '2')
        xml += self.init_macro_xml()

        if self.settings.value("basicdice").toBool():
            xml += self.basic_die_macro_xml('d4')
            xml += self.basic_die_macro_xml('d6')
            xml += self.basic_die_macro_xml('d8')
            xml += self.basic_die_macro_xml('d10')
            xml += self.basic_die_macro_xml('d12')
            xml += self.basic_die_macro_xml('d20')

        if self.settings.value("skills").toBool():
            for k, v in self.skills.items():
                xml += self.roll_macro_xml(k, v, k, 'Skills', '75', self.settings.value("colors/skillsb").toString(),
                                           self.settings.value("colors/skillsf").toString(), '1')

        if self.settings.value("weapons").toBool():
            for weapon in self.weapons:
                xml += self.weapon_macro_xml(weapon['name'], weapon['atk'], weapon['dam'], weapon['crit'])

        if self.settings.value("maneuvers").toBool():
            for k, v in self.maneuvers.items():
                xml += self.roll_macro_xml(k, v, k, 'Maneuvers', '75', self.settings.value("colors/maneuversb").toString(),
                                           self.settings.value("colors/maneuversf").toString(), '1')

        if self.feats:
            xml += self.list_macro_xml('Feats', self.feats, '35')

        if self.traits:
            xml += self.list_macro_xml('Traits', self.traits, '35')

        if self.specials:
            xml += self.list_macro_xml('Specials', self.specials, '50')

        if self.itempowers:
            xml += self.list_macro_xml('Item Powers', self.itempowers, '60')

        if self.resists:
            xml += self.list_macro_xml('Resists', self.resists, '50')

        if self.spells:
            xml += self.spell_list_macro_xml('Spellbook', self.spells, '60')

        if self.spells_memorized:
            xml += self.spell_list_macro_xml('Memorized', self.spells_memorized, '65')

        if self.spells_known:
            xml += self.spell_list_macro_xml('Spells Known', self.spells_known, '80')

        if self.items and self.settings.value("items").toBool():
            xml += self.items_macro_xml()

        if self.settings.value("indexing").toBool() != 'None':
            xml += self.list_show_macro_xml()

        xml += '    </macroPropertiesMap>\n'

        xml += '    <speechMap/>\n'
        xml += '    </net.rptools.maptool.model.Token>\n'

        self.content_xml = xml

    def property_xml(self, name, value):

        xml = ''
        xml += '        <entry>\n'
        xml += '          <string>' + str(name).lower() + '</string>\n'
        xml += '          <net.rptools.CaseInsensitiveHashMap_-KeyValue>\n'
        xml += '            <key>' + name + '</key>\n'
        xml += '            <value class="string">' + value + '</value>\n'
        xml += '            <outer-class reference="../../../.."/>\n'
        xml += '          </net.rptools.CaseInsensitiveHashMap_-KeyValue>\n'
        xml += '        </entry>\n'

        return xml

    def hp_macro_xml(self):

        self.num_macros += 1
        colorf = self.settings.value("colors/hpf").toString()
        colorb = self.settings.value("colors/hpb").toString()
        hpc = self.settings.value("properties/hp").toString()
        hpm = self.settings.value("properties/hpmax").toString()

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
            tmp += '"hpChange|0|Number of Hit Points",\n'
            tmp += '"dmgOrHealing|Damage,Healing|Is the character taking damage or being healed?|RADIO|SELECT=0")]\n'
            tmp += '[h:abort(status)]\n'
            tmp += '[if(dmgOrHealing == 0),CODE:\n'
            tmp += '{\n'
            tmp += '[h:' + hpc + ' = ' + hpc + ' - hpChange]\n'
            tmp += '[h:bar.Health = ' + hpc + ' / ' + hpm + ']\n'
            tmp += '[r:token.name] loses [r:hpChange] hit points.\n'
            tmp += '};\n'
            tmp += '{\n'

            tmp += '[h:' + hpc + ' = ' + hpc + ' + hpChange]\n'
            tmp += '[h:bar.Health = ' + hpc + ' / ' + hpm + ']\n'
            tmp += '[r:token.name] is healed and gains  [r:hpChange] hit points.\n'
            tmp += '};]\n'
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
            tmp += '[r:token.name] is gains  [r:hpChange] hit points.\n'
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
            tmp += '[r:token.name] is gains  [r:hpChange] hit points.\n'
            tmp += '};]\n'

        xml += cgi.escape(tmp)

        xml += '</command>\n'
        xml += '           <label>HP</label>\n'
        xml += '           <group>Basic</group>\n'
        xml += '           <sortby>1</sortby>\n'
        xml += '           <autoExecute>true</autoExecute>\n'
        xml += '           <includeLabel>false</includeLabel>\n'
        xml += '           <applyToTokens>true</applyToTokens>\n'
        xml += '           <fontColorKey>' + colorf + '</fontColorKey>\n'
        xml += '           <fontSize>1.00em</fontSize>\n'
        xml += '           <minWidth>30</minWidth>\n'
        xml += '           <maxWidth>30</maxWidth>\n'
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

        xml += cgi.escape(tmp)

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
        width = '30'
        group = 'Basic Dice'
        font = self.settings.value("colors/basicf").toString()
        background = self.settings.value("colors/basicb").toString()
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

        xml += cgi.escape(tmp)

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

        font = self.settings.value("colors/specialsf").toString()
        background = self.settings.value("colors/specialsb").toString()

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
        xml += '[frame(&quot;' + name + '&quot;): {&#xd;\n'
        # <html>
        xml += '&lt;html&gt;&#xd;\n'
        # <head>
        xml += '&lt;head&gt;&#xd;\n'
        # <title>name</title>
        xml += '&lt;title&gt;' + name + '&lt;/title&gt;&#xd;\n'
        # </head>
        xml += '&lt;/head&gt;&#xd;\n'
        # <body>
        xml += '&lt;body&gt;&#xd;\n'

        xml += '&lt;br&gt;&#xd;\n'
        # <h1><u>Character Name name </u></h1>
        xml += '&lt;h1&gt;&lt;u&gt;' + self.name + ' ' + name + ' &lt;/u&gt;&lt;/h1&gt;&#xd;\n'
        # <br>
        xml += '&lt;br&gt;&#xd;\n'

        spells_by_level = sorted(spells, key=lambda k: k['level'])
        current = -1
        for spell in spells_by_level:
            if spell['level'] > current:
                current = spell['level']
                xml += '&lt;h2&gt;&lt;u&gt;Level ' + str(spell['level']) + ' Spells &lt;/u&gt;&lt;/h2&gt;&#xd;\n'

            sname = spell['name']
            if self.settings.value("indexing").toString() == 'HTML':
                xml += '[r: macrolink(&quot;' + sname + \
                       '&quot;, &quot;lshow@token&quot;, &quot;none&quot;, &quot;url=' + \
                       self.settings.value("httpbase").toString() + \
                       self.index_append(self.spell_html(spell)) +\
                       ';lname=' + sname + '&quot;, currentToken())]'

                if spell['save'].lower() != 'none':
                    xml += ' (CL:' + spell['casterlevel'] + ' / DC:' + spell['dc'] + ')'
                else:
                    xml += ' (CL:' + spell['casterlevel'] + ')'

                xml += '&lt;br&gt;&#xd;\n'
            # No indexing
            else:
                xml += spell['name']
                if spell['save'].lower() != 'none':
                    xml += ' (CL:' + spell['casterlevel'] + ' / DC:' + spell['dc'] + ')'
                else:
                    xml += ' (CL:' + spell['casterlevel'] + ')'
                xml += '&lt;br&gt;&#xd;\n'

        #</body>
        xml += '&lt;/body&gt;&#xd;\n'
        #</html>
        xml += '&lt;/html&gt;&#xd;\n'
        #}]
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

        # <b>School</b>
        html = '<b>School</b> ' + spell['schooltext']
        # <h3>Casting</h3>
        html += '<h3>Casting</h3>\n'
        # <hr>
        html += '<hr>\n'
        # <b>Casting Time</b> <br>
        html += '<b>Casting Time</b> ' + spell['casttime'] + '<br>'
        # <b>Components</b>
        html += '<b>Components</b> ' + spell['componenttext']
        # <h3>Effect</h3>
        html += '<h3>Effect</h3>\n'
        # <hr>
        html += '<hr>\n'
        # <b>Range</b>
        if spell['range']:
            html += '<b>Range</b> ' + spell['range'] + '<br>'
        # <b>Area</b>
        if spell['area']:
            html += '<b>Area</b> ' + spell['area'] + '<br>'
        # <b>Target</b>
        if spell['target']:
            html += '<b>Target</b> ' + spell['target'] + '<br>'
        # <b>Duration</b>
        if spell['duration']:
            html += '<b>Duration</b> ' + spell['duration'] + '<br>'
        # <b>Effect</b>
        if spell['effect']:
            html += '<b>Effect</b> ' + spell['effect'] + '<br>'
        # <b>Saving Throw</b> <b>Spell Resistance</b>
        html += '<b>Saving Throw</b> ' + spell['save']
        html += ' <b>Spell Resistance</b> ' + spell['resist']
        # <h3>Description</h3>
        html += '<h3>Description</h3>\n'
        # <hr>
        html += '<hr>\n'
        html += string.replace(spell['description'], '\n', '<br>')

        return html

    def list_macro_xml(self, name, items, width):

        font = self.settings.value("colors/specialsf").toString()
        background = self.settings.value("colors/specialsb").toString()
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
        xml += '[frame(&quot;' + name + '&quot;): {&#xd;\n'
        # <html>
        xml += '&lt;html&gt;&#xd;\n'
        # <head>
        xml += '&lt;head&gt;&#xd;\n'
        # <title>name</title>
        xml += '&lt;title&gt;' + name + '&lt;/title&gt;&#xd;\n'
        # </head>
        xml += '&lt;/head&gt;&#xd;\n'
        # <body>
        xml += '&lt;body&gt;&#xd;\n'

        xml += '&lt;br&gt;&#xd;\n'
        # <h1><u>Character Name name </u></h1>
        xml += '&lt;h1&gt;&lt;u&gt;' + self.name + ' ' + name + ' &lt;/u&gt;&lt;/h1&gt;&#xd;\n'
        # <br>
        xml += '&lt;br&gt;&#xd;\n'

        for k, v in items.items():
            if v is None:
                xml += k
                xml += '&lt;br&gt;&#xd;\n'
                continue
            # Indexing
            if self.settings.value("indexing").toString() == 'HTML':
                # [r: macroLink("k", "lshow@token", "none", "url=url;lname=k", currentToken())
                xml += '[r: macrolink(&quot;' + k + '&quot;, &quot;lshow@token&quot;, &quot;none&quot;, &quot;url=' + \
                       self.settings.value("httpbase").toString() + self.index_append(self.pretty_html(v)) + ';lname=' +\
                       k + '&quot;, currentToken())]'
            # No index
            else:
                xml += k
            xml += '&lt;br&gt;&#xd;\n'

        #</body>
        xml += '&lt;/body&gt;&#xd;\n'
        #</html>
        xml += '&lt;/html&gt;&#xd;\n'
        #}]
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

    def items_macro_xml(self):

        font = self.settings.value("colors/specialsf").toString()
        background = self.settings.value("colors/specialsb").toString()
        group = 'Special'
        label = 'Items'
        width = '40'

        self.num_macros += 1

        xml = '        <entry>\n'
        xml += '         <int>' + str(self.num_macros) + '</int>\n'
        xml += '         <net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '           <saveLocation></saveLocation>\n'
        xml += '           <index>' + str(self.num_macros) + '</index>\n'
        xml += '           <colorKey>' + background + '</colorKey>\n'
        xml += '           <hotKey>None</hotKey>\n'
        xml += '           <command>'

        tmp = '[frame("Items"): {\n'
        tmp += '<html>\n'
        tmp += '<head>\n'
        tmp += '<title>Items</title>\n'
        tmp += '</head>\n'
        tmp += '<body>\n'
        tmp += '<br>\n'
        tmp += '<h1><u>' + self.name + ' Items </u></h1>\n'
        tmp += '<br>\n'

        for item in self.items:
            name = item['name']
            name = string.replace(name, "'", "")
            name = string.replace(name, "[", "")
            name = string.replace(name, "]", "")
            tmp += name
            if int(item['num']) > 1:
                tmp += ' (x' + item['num'] + ', ' + item['value'] + ')'
            else:
                tmp += ' (' + item['value'] + ')'
            tmp += '<br>\n'

        tmp += '</body>\n'
        tmp += '</html>\n'
        tmp += '}]\n'

        xml += cgi.escape(tmp)

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

        font = self.settings.value("colors/subf").toString()
        background = self.settings.value("colors/subb").toString()
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

        #</body>
        xml += '&lt;/body&gt;&#xd;\n'
        #</html>
        xml += '&lt;/html&gt;&#xd;\n'
        #}]
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

    def init_macro_xml(self):

        font = self.settings.value("colors/initf").toString()
        background = self.settings.value("colors/initb").toString()
        group = 'Basic'
        width = '25'
        name = 'Initiative'
        label = 'Init'

        self.num_macros += 1
        bonus = string.replace(self.initiative, '+', '')

        xml = '        <entry>\n'
        xml += '         <int>' + str(self.num_macros) + '</int>\n'
        xml += '         <net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '           <saveLocation></saveLocation>\n'
        xml += '           <index>' + str(self.num_macros) + '</index>\n'
        xml += '           <colorKey>' + background + '</colorKey>\n'
        xml += '           <hotKey>None</hotKey>\n'
        xml += '           <command>'
        xml += '[h: Roll = d20]\n'

        tmp = "<table border='0' cellpadding='0' cellspacing='0' style='width:200px'>\n"
        tmp += "<tr bgcolor='" + background + "'>\n"
        tmp += " <td><span style='color:" + font + "'><b>" + name + "</b></span></td>\n"
        tmp += "</tr>\n"
        tmp += "<tr>\n"
        tmp += "<td>[r: InitRoll = Roll + " + bonus + "]</td>\n"
        tmp += "</tr>\n"
        tmp += "</table>\n"

        xml += cgi.escape(tmp)

        xml += '[h: setInitiative(InitRoll)]\n'
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
        xml += '           <toolTip>' + bonus + '</toolTip>\n'
        xml += '           <commonMacro>false</commonMacro>\n'
        xml += '           <compareGroup>true</compareGroup>\n'
        xml += '           <compareIncludeLabel>true</compareIncludeLabel>\n'
        xml += '           <compareAutoExecute>true</compareAutoExecute>\n'
        xml += '           <compareApplyToSelectedTokens>true</compareApplyToSelectedTokens>\n'
        xml += '         </net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '       </entry>\n'

        return xml

    def weapon_macro_xml(self, name, attack, damage, crit):

        font = self.settings.value("colors/attacksf").toString()
        background = self.settings.value("colors/attacksb").toString()
        group = 'Attacks'
        width = '100'

        found = re.search('(\+?\-?\d+)', attack)
        if found:
            attack = int(found.group(1))
        else:
            attack = 0

        if attack > 0:
            roll = 'd20 + ' + str(attack)
        elif attack < 0:
            roll = 'd20 - ' + str(attack * -1)
        else:
            roll = 'd20'

        # Check to make sure damage is a xdy format

        self.num_macros += 1

        xml = '        <entry>\n'
        xml += '         <int>' + str(self.num_macros) + '</int>\n'
        xml += '         <net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '           <saveLocation></saveLocation>\n'
        xml += '           <index>' + str(self.num_macros) + '</index>\n'
        xml += '           <colorKey>' + background + '</colorKey>\n'
        xml += '           <hotKey>None</hotKey>\n'
        xml += '           <command>'

        tmp = "<table border='1' cellpadding='0' cellspacing='0' style='width:200px'>\n"
        tmp += "<tr bgcolor='" + background + "'>\n"
        tmp += "<td><span style='color:" + font + "'><b>" + name + "(" + crit + ")</b></span></td>\n"
        tmp += "<td><span style='color:" + font + "'><b>Damage</b></span></td>\n"
        tmp += "</tr>\n"
        tmp += "<tr>\n"
        tmp += "<td>[e:" + roll + "]</td>\n"
        if re.search('\d*d\d+', damage):
            tmp += "<td>[e:" + damage + "]</td>\n"
        else:
            tmp += "<td>" + damage + "</td>\n"
        tmp += "</tr>\n"
        tmp += "</table>\n"

        xml += cgi.escape(tmp)

        xml += '</command>\n'
        xml += '           <label>' + name + '</label>\n'
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

    def charsheet_macro_xml(self):

        font = self.settings.value("colors/sheetf").toString()
        background = self.settings.value("colors/sheetb").toString()
        group = 'Basic'
        label = 'Sheet'
        width = '40'
        url = self.settings.value("httpbase").toString()

        self.num_macros += 1

        xml = '        <entry>\n'
        xml += '         <int>' + str(self.num_macros) + '</int>\n'
        xml += '         <net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '           <saveLocation></saveLocation>\n'
        xml += '           <index>' + str(self.num_macros) + '</index>\n'
        xml += '           <colorKey>' + background + '</colorKey>\n'
        xml += '           <hotKey>None</hotKey>\n'
        xml += '           <command>'

        tmp = '[frame("Character Sheet"): {\n'
        tmp += '[r: requestURL("' + url + self.html_filename + '")]\n'
        tmp += '}]\n'

        xml += cgi.escape(tmp)

        xml += '</command>\n'
        xml += '           <label>' + label + '</label>\n'
        xml += '           <group>' + group + '</group>\n'
        xml += '           <sortby>1</sortby>\n'
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

    def make_pog(self, image_name):

        im = Image.open(str(image_name))
        size = (128, 128)
        im.thumbnail(size, Image.ANTIALIAS)

        output = StringIO.StringIO()
        im.save(output, 'png')
        self.pog_md5 = hashlib.md5(output.getvalue()).hexdigest()
        output.close()
        self.pog_asset = self.pog_md5 + '.png'
        self.pog_xml = '<net.rptools.maptool.model.Asset>\n  <id>\n    <id>' + self.pog_md5 + \
                       '</id>\n  </id>\n  <name>' + self.name + \
                       '</name>\n  <extension>png</extension>\n  <image/>\n</net.rptools.maptool.model.Asset>\n'
        self.pog = im

    def make_portrait(self, image_name):

        im = Image.open(str(image_name))
        size = (200, 200)
        im.thumbnail(size, Image.ANTIALIAS)

        output = StringIO.StringIO()
        im.save(output, 'png')
        self.portrait_md5 = hashlib.md5(output.getvalue()).hexdigest()
        output.close()
        self.portrait_asset = self.portrait_md5 + '.png'
        self.portrait_xml = '<net.rptools.maptool.model.Asset>\n  <id>\n    <id>' + self.portrait_md5 + \
                            '</id>\n  </id>\n  <name>' + self.name + \
                            '</name>\n  <extension>png</extension>\n  <image/>\n</net.rptools.maptool.model.Asset>\n'
        self.portrait = im

    def make_thumbnail(self):
        size = 50, 50
        im = self.pog.copy()
        im.thumbnail(size, Image.ANTIALIAS)
        self.thumbnail = im

    def index_append(self, value):

        if not value in self.values:
            self.values.append(value)

        return hashlib.md5(value.encode('utf-8')).hexdigest() + '.html'
