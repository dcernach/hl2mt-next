import xml.etree.ElementTree as ET
import os
import re
import zipfile
import string
import glob


class HeroLab:

    def __init__(self, input_folder, subdir, source, filename):
        self.html = ''
        self.text = ''
        self.xml = ''

        lab_file = input_folder + subdir + '/' + source

        lab_zip = zipfile.ZipFile(str(lab_file.toAscii()), 'r')
        index_xml = lab_zip.open('index.xml')
        tree = ET.parse(index_xml)
        index_xml.close()
        index_root = tree.getroot()
        for index_char in index_root.find('characters').iter('character'):
            for statblock in index_char.iter('statblock'):
                if str(filename) in statblock.get("filename"):
                    if statblock.get("format") == "html":
                        html_file = statblock.get("folder") + "/" + statblock.get("filename")
                        self.html = lab_zip.read(html_file)
                    if statblock.get("format") == "text":
                        text_file = statblock.get("folder") + "/" + statblock.get("filename")
                        self.text = lab_zip.read(text_file)
                    if statblock.get("format") == "xml":
                        text_file = statblock.get("folder") + "/" + statblock.get("filename")
                        self.text = lab_zip.read(text_file)

        lab_zip.close()


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
                                if name.endswith('s'):
                                    minion_name = name + "' " + minion.get('name')
                                else:
                                    minion_name = name + "'s " + minion.get('name')

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
        name = string.replace(name, " (combat trained) ", "")
        name = string.replace(name, " (combat trained)", "")
        name = string.replace(name, "(combat trained)", "")
        name = re.sub(r'([^\s\w]|_)+', '', name)
        name = string.replace(name, "  ", "_")
        name = string.replace(name, " ", "_")


        filename = full_dir + '/' + name + '.rptok'
        num = 1
        while filename in self.filenames:
            filename = full_dir + '/' + name + str(num) + '.rptok'
            num += 1

        self.filenames.append(filename)

        return filename
