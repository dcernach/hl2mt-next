import xml.etree.ElementTree as ET
import os
import re
import zipfile


class HeroLab:

    def __init__(self, folder, source, filename):
        self.html = ''
        self.text = ''
        self.xml = ''

        lab_zip = zipfile.ZipFile(str(folder) + '/' + str(source.toAscii()), 'r')
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

    def __init__(self, search_folder):
        self.search_folder = search_folder

    def get_creatures(self):

        self.bad_files = []
       # Parse Por/Stock files
        for filename in os.listdir(self.search_folder):
            if re.match('.*\.stock|.*\.por', filename):
                try:
                    lab_zip = zipfile.ZipFile(str(self.search_folder) + '/' + filename, 'r')
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
                            yield {"name": name, "summary": summary, "cr": cr, "source": filename,
                                   "filename": char_filename, "mr": mr}
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
                                yield {"name": minion_name, "summary": summary, "cr": cr, "source": filename,
                                       "filename": char_filename, "mr": mr}
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
                            yield {"name": name, "summary": summary, "cr": cr, "source": filename,
                                   "filename": char_filename, "mr": mr}

                    lab_zip.close()
                except zipfile.BadZipfile:
                    self.bad_files.append(filename)
