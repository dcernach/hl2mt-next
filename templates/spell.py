__author__ = 'Dalton Andrade'

from html import escape


def gen_spell_detail(spell):
    """
    Generates the spell detail HTML using the spell information dictionary.
    :param spell: spell information dictionary.
    :return: html page based on input spell dictionary
    """
    if spell['save'].lower() != 'none':
        spell['cldc'] = '(CL: %s / DC: %s)' % (spell['casterlevel'], spell['dc'])
    else:
        spell['cldc'] = '(CL: %s)' % spell['casterlevel']

    spell['description'] = str.replace(spell['description'], '\n', '<br>')

    # html = '\n <html>'
    # html += '\n <head>'
    # html += '\n     <title>Spell: %s</title>' % spell['name']
    # html += '\n </head>'
    html = '\n <div style="padding: 0 10px 0 10px;">'
    html += '\n     <h2>%s <span>%s</span></h2>' % (spell['name'], spell['cldc'])
    html += '\n     <table cellpadding="2px" border="1" style="width:350px">'
    html += '\n         <tr>'
    html += '\n             <td style="width:110px"><b>Level</b></td>'
    html += '\n             <td style="width:240px">%s</td>' % spell['level']
    html += '\n         </tr>'
    html += '\n         <tr>'
    html += '\n             <td><b>School</b></td> <td>%s</td></tr>' % spell['schooltext']
    html += '\n         </tr>'
    html += '\n         <tr>'
    html += '\n             <td><b>Casting Time</b></td> <td>%s</td>' % spell['casttime']
    html += '\n         </tr>'
    html += '\n         <tr>'
    html += '\n             <td><b>Components</b></td> <td>%s</td>' % spell['componenttext']
    html += '\n         </tr>'

    if spell['range']:
        html += '\n     <tr>'
        html += '\n         <td><b>Range</b></td> <td>%s</td>' % spell['range']
        html += '\n     </tr>'

    if spell['area']:
        html += '\n     <tr>'
        html += '\n         <td><b>Area</b></td> <td>%s</td>' % spell['area']
        html += '\n     </tr>'

    if spell['target']:
        html += '\n     <tr>'
        html += '\n         <td><b>Target</b> </td><td>%s</td>' % spell['target']
        html += '\n     </tr>'

    if spell['duration']:
        html += '\n     <tr>'
        html += '\n         <td><b>Duration</b></td> <td>%s</td>' % spell['duration']
        html += '\n     </tr>'

    if spell['effect']:
        html += '\n     <tr>'
        html += '\n         <td><b>Effect</b></td> <td>%s</td>' % spell['effect']
        html += '\n     </tr>'

    html += '\n         <tr>'
    html += '\n             <td><b>Saving Throw</b></td> <td>%s</td>' % spell['save']
    html += '\n         </tr>'

    html += '\n         <tr>'
    html += '\n             <td><b>Spell Resistance</b></td> <td>%s</td>' % spell['resist']
    html += '\n         </tr>'

    html += '\n         <tr>'
    html += '\n             <td style="width:350px; text-align:justify" colspan="2">%s</td>' % spell['description']
    html += '\n         </tr>'

    html += '\n     </table>'
    html += '\n </div>'
    # html += '\n </html>'

    return escape(html)


def gen_spell_list(spells):
    spells_by_level = sorted(spells, key=lambda k: k['level'])
    current = -1
    spell_macro_count = 0

    pass
