__author__ = 'dandrade'
import html

# Global count variable for macros entries
_macro_index = {"macro_index": 0}


def get_index():
    _macro_index["macro_index"] += 1
    return _macro_index["macro_index"]


def create_entry(label, group, command, auto_execute=True, width=None, font_color='black',
                 bg_color='gray', player_edit=False, tooltip=None):
    if width is None:
        width = len(label) * 8

    macro_index = get_index()

    entry = '\n<entry>'
    entry += '\n    <int>%i</int>' % (macro_index)
    entry += '\n    <net.rptools.maptool.model.MacroButtonProperties>'
    entry += '\n        <saveLocation></saveLocation>'
    entry += '\n        <index>%i</index>' % (macro_index)
    entry += '\n        <colorKey>%s</colorKey>' % (bg_color)
    entry += '\n        <hotKey>None</hotKey>'
    entry += '\n        <command>%s</command>' % (html.escape(command))
    entry += '\n        <label>%s</label>' % (label)
    entry += '\n        <group>%s</group>' % (group)
    entry += '\n        <sortby>1</sortby>'
    entry += '\n        <autoExecute>true</autoExecute>'
    entry += '\n        <includeLabel>false</includeLabel>'
    entry += '\n        <applyToTokens>true</applyToTokens>'
    entry += '\n        <fontColorKey>%s</fontColorKey>' % (font_color)
    entry += '\n        <fontSize>1.00em</fontSize>'
    entry += '\n        <minWidth>%i</minWidth>' % (width)
    entry += '\n        <maxWidth>%i</maxWidth' % (width)
    entry += '\n        <allowPlayerEdits>%s</allowPlayerEdits>' % (str(player_edit).lower())
    entry += '\n        <toolTip>%s</toolTip>' % (tooltip if tooltip is not None else "")
    entry += '\n        <commonMacro>false</commonMacro>'
    entry += '\n        <compareGroup>true</compareGroup>'
    entry += '\n        <compareIncludeLabel>true</compareIncludeLabel>'
    entry += '\n        <compareAutoExecute>true</compareAutoExecute>'
    entry += '\n        <compareApplyToSelectedTokens>true</compareApplyToSelectedTokens>'
    entry += '\n    </net.rptools.maptool.model.MacroButtonProperties>'
    entry += '\n</entry>'

    return entry
