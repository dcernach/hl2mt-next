__author__ = 'p017058'
from PyQt4.QtCore import QSettings
import macros.util as mu


class InitMacros:
    def __init__(self):
        # TODO: How to Fix this?, why I cannot reference this as in mttoken.py __init__ (self.settings = QSettings)
        self.settings = QSettings("hl2mt.ini", QSettings.IniFormat)

    def gen_remove_init(self, macro_number):
        """
        Generates macro to remove current token from "init" window
        :param macro_number: macro id
        :return: maptool macro entry
        """
        item_width = '120'
        item_label = 'Remove from Init'
        item_group = '00 - Initiative'
        font_color = self.settings.value("colors/initf")
        back_color = self.settings.value("colors/initb")

        macro_code = '\n[h: removeFromInitiative()]'
        macro_code += '\n<table border="0" cellpadding="0" cellspacing="0" style="width:200px">'
        macro_code += '\n    <tr bgcolor="%s">' % back_color
        macro_code += '\n        <td><span style="color:%s"><b>Initiative</b></span></td>' % font_color
        macro_code += '\n    </tr>'
        macro_code += '\n    <tr>'
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
        item_group = '00 - Initiative'
        font_color = self.settings.value("colors/initf")
        back_color = self.settings.value("colors/initb")
        font_color, back_color = back_color, font_color  # invert

        macro_code = '\n[h: nextInitiative()]'
        macro_code += '\n[h: id = getInitiativeToken()]'
        macro_code += '\n[h: goto(id)]'  # center map on token
        macro_code += '\n[h: selectTokens(id, 0)]'  # select next token

        macro_code += '\n<table border="0" cellpadding="0" cellspacing="0" style="width:200px">'
        macro_code += '\n    <tr bgcolor="%s">' % font_color
        macro_code += '\n        <td><span style="color:%s"><b>Current Initiative</b></span></td>' % back_color
        macro_code += '\n    </tr>'
        macro_code += '\n    <tr>'
        macro_code += '\n         <td>Was given to <b>[r: token.name]</b>.</td>'
        macro_code += '\n    </tr>'
        macro_code += '\n</table>'

        entry = mu.create_entry(item_label, macro_code,
                                macro_number=macro_number,
                                macro_group=item_group,
                                btn_width=item_width,
                                btn_font_color=font_color,
                                btn_back_color=back_color)
        return entry
