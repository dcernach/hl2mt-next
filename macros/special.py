__author__ = 'dandrade'

from PyQt4.QtCore import QSettings
from html import escape
import macros.util as MU


class SpecialMacros:
    def __init__(self):
        # TODO: How to Fix this?, why I cannot reference this as in mttoken.py __init__ (self.settings = QSettings)
        self.settings = QSettings("hl2mt.ini", QSettings.IniFormat)
        self.num_macros = None

    def fn_detail_macro_xml(self, num_macros):
        font = self.settings.value("colors/subf")
        background = self.settings.value("colors/subb")
        group = 'Submacros'
        width = '60'
        label = 'fn_detail'

        self.num_macros = num_macros
        ######
        ## Base Macro Template
        ######
        xml = '    <entry>\n'
        xml += '        <int>' + str(self.num_macros) + '</int>\n'
        xml += '        <net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '            <saveLocation></saveLocation>\n'
        xml += '            <index>' + str(self.num_macros) + '</index>\n'
        xml += '            <colorKey>' + background + '</colorKey>\n'
        xml += '            <hotKey>None</hotKey>\n'
        xml += '            <command>'
        xml += '%s\n'
        xml += '            </command>\n'
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
        xml += '           <allowPlayerEdits>false</allowPlayerEdits>\n'
        xml += '           <toolTip></toolTip>\n'
        xml += '           <commonMacro>false</commonMacro>\n'
        xml += '           <compareGroup>true</compareGroup>\n'
        xml += '           <compareIncludeLabel>true</compareIncludeLabel>\n'
        xml += '           <compareAutoExecute>true</compareAutoExecute>\n'
        xml += '           <compareApplyToSelectedTokens>true</compareApplyToSelectedTokens>\n'
        xml += '         </net.rptools.maptool.model.MacroButtonProperties>\n'
        xml += '       </entry>\n'

        ###################################################
        ## Lets play with macro code
        ###################################################

        macro_code = '[frame("ShowDetails"): {\n'
        macro_code += '[h:title = getStrProp(macro.args, "title", "", "&")]\n'
        macro_code += '[h:keys  = getStrProp(macro.args, "keys", "", "&")]\n'
        # html content
        macro_code += '  <html>\n'
        macro_code += '     <head>\n'
        macro_code += '         <title>Showing Details: [r:title]</title>\n'
        macro_code += '     <head>\n'
        macro_code += '     <body>\n'
        macro_code += '         [r:getProperty(keys)]\n'
        macro_code += '     </body>\n'
        macro_code += '  </html>\n'
        # /html content
        macro_code += '}]'

        return xml % escape(macro_code)

# [frame("Show Details"): {
#     <html>
#     <head>
#         <title>Show Details</title>
#     </head>
#     <body>
#         [h:lname = getStrProp(macro.args, "lname")]
#         <h1><u>[r:lname]</u></h1>
#         [h:url = getStrProp(macro.args, "url")]
#         [r: requestURL(url)]
#     </body>
# </html>
# }]
