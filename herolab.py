import xml.etree.ElementTree as ET
import os
import re
import zipfile
import string
import glob
from token import Pathfinder
from PyQt4.QtCore import *
import StringIO


class HeroLab:

    def __init__(self, input_folder, subdir, source, filename):
        self.html = ''
        self.text = ''
        self.xml = ''
        self.settings = QSettings
        self.subdir = subdir
        self.source = source
        self.input_folder = input_folder
        self.values = []
        filename = str(filename)
        self.html_filename = ''

        lab_file = input_folder + subdir + '/' + source

        minion_num = 0
        txt_search = ''
        html_search = ''
        xml_search = ''

        if re.search('^(\d+)\.(\d+)_', filename):
            found = re.search('^(\d+)\.(\d+)_', filename)
            char_num = found.group(1)
            minion_num = found.group(2)

            txt_search = '^' + filename + '\.txt$'
            html_search = '^' + filename + '\.htm$'
            xml_search = '^' + char_num + '_.+\.xml$'

        elif re.search('^(\d+)_', filename):

            txt_search = '^' + filename + '\.txt$'
            html_search = '^' + filename + '\.htm$'
            xml_search = '^' + filename + '\.xml$'

        lab_zip = zipfile.ZipFile(str(lab_file.toAscii()), 'r')
        index_xml = lab_zip.open('index.xml')
        tree = ET.parse(index_xml)
        index_xml.close()
        index_root = tree.getroot()

        for index_char in index_root.find('characters').iter('character'):
            for statblock in index_char.iter('statblock'):
                if re.search(txt_search, statblock.get("filename")):
                    text_file = statblock.get("folder") + "/" + statblock.get("filename")
                    self.text = lab_zip.read(text_file)
                if re.search(html_search, statblock.get("filename")):
                    html_file = statblock.get("folder") + "/" + statblock.get("filename")
                    self.html = lab_zip.read(html_file)
                if re.search(xml_search, statblock.get("filename")):
                    xml_name = statblock.get("folder") + "/" + statblock.get("filename")
                    xml_file = lab_zip.open(xml_name)
                    xml_tree = ET.parse(xml_file)
                    xml_file.close()
                    xml_root = xml_tree.getroot()
                    for char in xml_root.iter('character'):
                        minions = char.find('minions')
                        if minions is not None:
                            char.remove(minions)
                        if minion_num:
                            minion_count = 0
                            for minion in minions.iter('character'):
                                minion_count += 1
                                if minion_count == int(minion_num):
                                    self.xml = minion
                        else:
                            self.xml = char

        lab_zip.close()

    def create_token(self, name, portrait, pog, filename):

        token = Pathfinder(name, self.xml, self.html)
        token.name = name
        token.values = self.values
        token.settings = self.settings

        full_dir = str(self.settings.value("folderOutput").toString() + self.subdir)
        self.html_filename = string.replace(str(filename), full_dir + '/', '')
        self.html_filename = re.sub(r'\.rptok$', '.html', self.html_filename)
        self.html_filename = str(self.subdir)[1:] + '_' + self.html_filename

        token.html_filename = self.html_filename
        token.parse()
        token.make_pog(pog)
        token.make_portrait(portrait)
        token.make_thumbnail()
        token.make_content_xml()


        if not os.path.exists(full_dir):
            os.makedirs(full_dir)

        rptok = zipfile.ZipFile(str(filename), 'w')
        rptok.writestr('properties.xml', token.properties_xml)
        rptok.writestr('content.xml', token.content_xml.toUtf8())

        output = StringIO.StringIO()
        token.pog.save(output, 'png')
        rptok.writestr('assets/' + token.pog_asset, output.getvalue())
        output.close()
        rptok.writestr('assets/' + token.pog_md5, token.pog_xml.toUtf8())

        output = StringIO.StringIO()
        token.portrait.save(output, 'png')
        rptok.writestr('assets/' + token.portrait_asset, output.getvalue())
        output.close()
        rptok.writestr('assets/' + token.portrait_md5, token.portrait_xml.toUtf8())

        output = StringIO.StringIO()
        token.thumbnail.save(output, 'png')
        rptok.writestr('thumbnail', output.getvalue())
        output.close()
        rptok.close()

        self.values = token.values


class HeroLabIndex:

    def __init__(self, input_folder, pog_folder, portrait_folder, token_folder):
        self.input_folder = str(input_folder)
        self.pog_folder = str(pog_folder)
        self.portrait_folder = str(portrait_folder)
        self.token_folder = str(token_folder)
        self.filenames = []

    def get_creatures(self):

        self.bad_files = []
       # Parse Por files
        for dirpath, dirnames, filenames in os.walk(self.input_folder):
            for filename in [f for f in filenames if f.endswith(".por")]:
                lab_file = os.path.join(dirpath, filename)
                subdir = string.replace(dirpath, self.input_folder, '')
                try:
                    lab_zip = zipfile.ZipFile(lab_file, 'r')
                    index_xml = lab_zip.open('index.xml')
                    tree = ET.parse(index_xml)
                    index_xml.close()
                    index_root = tree.getroot()
                    for index_char in index_root.find('characters').iter('character'):
                        if index_char.find('minions') is not None:
                            minions = index_char.find('minions')
                            index_char.remove(minions)
                            name = index_char.get('name')
                            summary = index_char.get('summary')
                            found = re.search(' CR (\d+/?\d*)/?M?R?\s*(\d*/?\d*)$', summary)
                            cr = ''
                            mr = ''
                            if found is not None:
                                cr = found.group(1)
                                if found.group(2) is not None:
                                    mr = found.group(2)
                            char_filename = ''
                            for statblock in index_char.iter('statblock'):
                                char_filename = statblock.get('filename')
                                char_filename = re.sub(r"\.\w\w\w$", "", char_filename)
                            pog_file = self._search_file(self.pog_folder, subdir, name)
                            portrait_file = self._search_file(self.portrait_folder, subdir, name)
                            token = self._token_name(subdir, name)
                            yield {"name": name, "summary": summary, "cr": cr, "source": filename,
                                   "filename": char_filename, "mr": mr, "subdir": subdir, "pog": pog_file,
                                   "portrait": portrait_file, "token": token}
                            for minion in minions.iter('character'):
                                minion_name = name + minion.get('name')
                                summary = minion.get('summary')
                                found = re.search(' CR (\d+/?\d*)/?M?R?\s*(\d*/?\d*)$', summary)
                                cr = ''
                                mr = ''
                                if found is not None:
                                    cr = found.group(1)
                                    if found.group(2) is not None:
                                        mr = found.group(2)
                                char_filename = ''
                                for statblock in minion.iter('statblock'):
                                    char_filename = statblock.get('filename')
                                    char_filename = re.sub(r"\.\w\w\w$", "", char_filename)
                                pog_file = self._search_file(self.pog_folder, subdir, minion_name)
                                portrait_file = self._search_file(self.portrait_folder, subdir, minion_name)
                                token = self._token_name(subdir, minion_name)
                                yield {"name": minion_name, "summary": summary, "cr": cr, "source": filename,
                                       "filename": char_filename, "mr": mr, "subdir": subdir, "pog": pog_file,
                                       "portrait": portrait_file, "token": token}
                        else:
                            name = index_char.get('name')
                            summary = index_char.get('summary')
                            found = re.search(' CR (\d+/?\d*)/?M?R?\s*(\d*/?\d*)$', summary)
                            cr = ''
                            mr = ''
                            if found is not None:
                                cr = found.group(1)
                                if found.group(2) is not None:
                                    mr = found.group(2)
                            char_filename = ''
                            for statblock in index_char.iter('statblock'):
                                char_filename = statblock.get('filename')
                                char_filename = re.sub(r"\.\w\w\w$", "", char_filename)
                            pog_file = self._search_file(self.pog_folder, subdir, name)
                            portrait_file = self._search_file(self.portrait_folder, subdir, name)
                            token = self._token_name(subdir, name)
                            yield {"name": name, "summary": summary, "cr": cr, "source": filename,
                                   "filename": char_filename, "mr": mr, "subdir": subdir, "pog": pog_file,
                                   "portrait": portrait_file, "token": token}

                    lab_zip.close()
                except zipfile.BadZipfile:
                    self.bad_files.append(filename)

    def _search_file(self, search_dir, subdir, char_name):

        paths = [search_dir + subdir + '/', search_dir + '/']

        for path in paths:
           # Full name search: Orc Chief
            filename = self._find_image_file(glob.glob(path + string.replace(char_name, ' ', '?') + '.*'))
            if filename:
                return filename
            filename = self._find_image_file(glob.glob(path + string.replace(char_name.lower(), ' ', '?') + '.*'))
            if filename:
                return filename

            # Search for partials: Orc, Chief
            for name in string.split(char_name, ' '):
                filename = self._find_image_file(glob.glob(path + name + '.*'))
                if filename:
                    return filename
                filename = self._find_image_file(glob.glob(path + name.lower() + '.*'))
                if filename:
                    return filename

            # Search for star partials: Orc*, Chief*
            for name in string.split(char_name, ' '):
                filename = self._find_image_file(glob.glob(path + name + '*'))
                if filename:
                    return filename
                filename = self._find_image_file(glob.glob(path + name.lower() + '*'))
                if filename:
                    return filename

            # Look for Default.* or default.*
            filename = self._find_image_file(glob.glob(path + 'Default.*'))
            if filename:
                return filename
            filename = self._find_image_file(glob.glob(path + 'default.*'))
            if filename:
                return filename

        # Fall through, grab *
        path = search_dir + '/'
        filename = self._find_image_file(glob.glob(path + '*'))

        return filename

    def _find_image_file(self, files):

        for filename in files:
            if os.path.isfile(filename):
                return filename

        return False

    def _token_name(self, subdir, name):

        full_dir = self.token_folder + subdir

        filename = full_dir + '/' + self.clean_name(name) + '.rptok'
        num = 1
        while filename in self.filenames:
            filename = full_dir + '/' + name + str(num) + '.rptok'
            num += 1

        self.filenames.append(filename)

        return filename

    @staticmethod
    def clean_name(name):

        name = string.replace(name, " (combat trained) ", "")
        name = string.replace(name, " (combat trained)", "")
        name = string.replace(name, "(combat trained)", "")
        name = re.sub(r'([^\s\w]|_)+', '', name)
        name = string.replace(name, "  ", "_")
        name = string.replace(name, " ", "_")

        return name
