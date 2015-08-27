__author__ = 'p017058'
from PyQt4.QtCore import QSettings
import macros.util as mu


class InitMacros:
    def __init__(self, prop_map=[]):
        # TODO: How to Fix this?, why I cannot reference this as in mttoken.py __init__ (self.settings = QSettings)
        self.settings = QSettings("hl2mt.ini", QSettings.IniFormat)
        self.prop_map = prop_map

    def gen_remove_init(self, macro_number):
        """
        Generates macro to remove current token from "init" window
        :param macro_number: macro id
        :return: maptool macro entry
        """
        item_width = '120'
        item_label = 'Remove from Init'
        item_group = '00 Initiative'
        font_color = self.settings.value("colors/initf")
        back_color = self.settings.value("colors/initb")

        macro_code = '\n[h: removeFromInitiative()]'
        macro_code += '\n<table border="0" cellpadding="5" cellspacing="0" style="width:200px">'
        macro_code += '\n    <tr bgcolor="%s">' % back_color
        macro_code += '\n        <td><span style="color:%s"><b>Initiative</b></span></td>' % font_color
        macro_code += '\n    </tr>'
        macro_code += '\n    <tr style="border:1px solid %s">' % back_color
        macro_code += '\n         <td>Was removed from initiative.</td>'
        macro_code += '\n    </tr>'
        macro_code += '\n</table>'

        entry = mu.create_entry(item_label, macro_code,
                                macro_number=macro_number,
                                macro_group=item_group,
                                btn_width=item_width,
                                btn_font_color=font_color,
                                btn_back_color=back_color)
        return entry

    def gen_next_init(self, macro_number):
        """
        Generates macro to move current "init" token to the next "init" token and centers it into view.
        :param macro_number: macro id
        :return: maptool macro entry
        """
        item_width = '120'
        item_label = 'Next Init'
        item_group = '00 Initiative'
        font_color = self.settings.value("colors/initf")
        back_color = self.settings.value("colors/initb")
        font_color, back_color = back_color, font_color  # invert

        macro_code = '\n[h: nextInitiative()]'
        macro_code += '\n[h: id = getInitiativeToken()]'
        macro_code += '\n[h: goto(id)]'  # center map on token
        macro_code += '\n[h: selectTokens(id, 0)]'  # select next token

        macro_code += '\n<table border="0" cellpadding="5" cellspacing="0" style="width:200px">'
        macro_code += '\n    <tr bgcolor="%s">' % font_color
        macro_code += '\n        <td><span style="color:%s"><b>Current Initiative</b></span></td>' % back_color
        macro_code += '\n    </tr>'
        macro_code += '\n    <tr style="border:1px solid %s">' % font_color
        macro_code += '\n         <td>Was given to <b>[r: getName(id)]</b>.</td>'
        macro_code += '\n    </tr>'
        macro_code += '\n</table>'

        entry = mu.create_entry(item_label, macro_code,
                                macro_number=macro_number,
                                macro_group=item_group,
                                btn_width=item_width,
                                btn_font_color=font_color,
                                btn_back_color=back_color)
        return entry

    def gen_roll_init(self, macro_number):
        item_width = '120'
        item_label = 'Roll Init'
        item_group = '00 Initiative'
        font_color = self.settings.value("colors/initf")
        back_color = self.settings.value("colors/initb")
        self.prop_map["hl2mt_initiative"] = self.prop_map["hl2mt_initiative"].replace('+', '')

        macro_roll = mu.explode_roll('d20', 'v_roll', 'v_bonus')

        macro_code = '\n[h: v_roll = d20]'
        macro_code += '\n[h: v_bonus = getProperty("hl2mt_initiative")]'
        macro_code += '\n[h: v_total = v_roll + v_bonus]'

        macro_code += '\n<table border="0" cellpadding="5" cellspacing="0" style="width:200px">'
        macro_code += '\n    <tr bgcolor="%s">' % back_color
        macro_code += '\n        <td><span style="color:%s"><b>Initiative</b></span></td>' % font_color
        macro_code += '\n    </tr>'
        macro_code += '\n    <tr style="border:1px solid %s">' % back_color
        macro_code += '\n         <td>%s</td>' % macro_roll
        macro_code += '\n    </tr>'
        macro_code += '\n</table>'

        macro_code += '\n[h: addToInitiative()]'
        macro_code += '\n[h: setInitiative(v_total)]'
        macro_code += '\n[h: sortInitiative()]'

        entry = mu.create_entry(item_label, macro_code,
                                macro_number=macro_number,
                                macro_group=item_group,
                                btn_width=item_width,
                                btn_font_color=font_color,
                                btn_back_color=back_color)
        return entry

    def gen_add_init(self, macro_number):
        item_width = '120'
        item_label = 'Add to Init'
        item_group = '00 Initiative'
        font_color = self.settings.value("colors/initf")
        back_color = self.settings.value("colors/initb")

        font_color, back_color = back_color, font_color

        macro_code = '\n[h: v_total = InitiativeRoll]'

        macro_code += '\n<table border="0" cellpadding="5" cellspacing="0" style="width:200px">'
        macro_code += '\n    <tr bgcolor="%s">' % font_color
        macro_code += '\n        <td><span style="color:%s"><b>Initiative</b></span></td>' % back_color
        macro_code += '\n    </tr>'
        macro_code += '\n    <tr style="border:1px solid %s">' % font_color
        macro_code += '\n         <td><b>[r: v_total]</b> was rolled</td>'
        macro_code += '\n    </tr>'
        macro_code += '\n</table>'

        macro_code += '\n[h: addToInitiative()]'
        macro_code += '\n[h: setInitiative(v_total)]'
        macro_code += '\n[h: sortInitiative()]'

        entry = mu.create_entry(item_label, macro_code,
                                macro_number=macro_number,
                                macro_group=item_group,
                                btn_width=item_width,
                                btn_font_color=font_color,
                                btn_back_color=back_color)
        return entry
