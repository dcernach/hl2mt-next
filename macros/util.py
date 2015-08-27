__author__ = 'dandrade'
import html

# Global count variable for macros entries
_macro_index = {"macro_index": 0}


def get_index():
    _macro_index["macro_index"] += 1
    return _macro_index["macro_index"]

def create_entry(macro_label, macro_command,
                 macro_number=None,
                 macro_group=None,
                 macro_sort_prefix=None,
                 macro_auto_execute=True,
                 macro_applyto_selected=True,
                 macro_player_editable=False,
                 btn_font_color='black',
                 btn_back_color='gray',
                 btn_width=None,
                 btn_tooltip=None):

    if macro_number is None:
        macro_number = get_index()

    if macro_sort_prefix is None:
        macro_sort_prefix = macro_number

    if btn_width is None:
        btn_width = len(macro_label) * 8

    macro_auto_execute = str(macro_auto_execute).lower()
    macro_player_editable = str(macro_player_editable).lower()
    macro_applyto_selected = str(macro_applyto_selected).lower()

    entry = '\n<entry>'
    entry += '\n    <int>%s</int>' % macro_number
    entry += '\n    <net.rptools.maptool.model.MacroButtonProperties>'
    entry += '\n        <saveLocation></saveLocation>'
    entry += '\n        <index>%s</index>' % macro_number
    entry += '\n        <colorKey>%s</colorKey>' % btn_back_color
    entry += '\n        <hotKey>None</hotKey>'
    entry += '\n        <command>'
    entry += '%s' % html.escape(macro_command)
    entry += '\n        </command>'
    entry += '\n        <label>%s</label>' % macro_label
    entry += '\n        <group>%s</group>' % (macro_group if macro_group is not  None else "")
    entry += '\n        <sortby>%s</sortby>' % macro_sort_prefix
    entry += '\n        <autoExecute>%s</autoExecute>' % macro_auto_execute
    entry += '\n        <includeLabel>false</includeLabel>'
    entry += '\n        <applyToTokens>%s</applyToTokens>' % macro_applyto_selected
    entry += '\n        <fontColorKey>%s</fontColorKey>' % btn_font_color
    entry += '\n        <fontSize>1.00em</fontSize>'
    entry += '\n        <minWidth>%s</minWidth>' % btn_width
    entry += '\n        <maxWidth>%s</maxWidth>' % btn_width
    entry += '\n        <allowPlayerEdits>%s</allowPlayerEdits>' % macro_player_editable
    entry += '\n        <toolTip>%s</toolTip>' % (btn_tooltip if btn_tooltip is not None else "")
    # /Macro Commonality
    entry += '\n        <commonMacro>false</commonMacro>'
    entry += '\n        <compareGroup>true</compareGroup>'
    entry += '\n        <compareIncludeLabel>true</compareIncludeLabel>'
    entry += '\n        <compareAutoExecute>true</compareAutoExecute>'
    entry += '\n        <compareApplyToSelectedTokens>true</compareApplyToSelectedTokens>'
    # /Macro Commonality
    entry += '\n    </net.rptools.maptool.model.MacroButtonProperties>'
    entry += '\n</entry>'

    return entry


def explode_roll(dice, roll_var, bonus_var):
    macro_code = '<b>[r: %(r)s + %(b)s]</b> = '
    macro_code += '%(d)s <b>([r: %(r)s])</b> + Bonus <b>([r: %(b)s])</b>'

    macro_code = macro_code % ({'d': dice, 'r': roll_var, 'b': bonus_var})

    return macro_code
