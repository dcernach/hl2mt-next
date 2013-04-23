import Tkinter as tk
import ttk
import xml.etree.ElementTree as ET
import tkFileDialog
import ConfigParser
import argparse
import os
import glob
import string
from pathfinder import Token, Table


class App:
    def __init__(self, master, config_file):

        config = ConfigParser.ConfigParser()
        config.read(config_file)
        self.config_file = config_file
        self.options = config._sections['app']
        self.properties = config._sections['properties']
        self.master_index = []

        frame = tk.Frame(master)
        master.title('Hero Lab Converter')
        frame.grid()

        option_files = glob.glob('*.conf')

        v = tk.StringVar()
        self.option_file = ttk.Combobox(frame, textvariable=v, state='readonly', width=20)
        self.option_file.var = v
        self.option_file.var.set(self.config_file)
        self.option_file.var.trace('w', self.config_change)
        self.option_file['values'] = tuple(option_files)
        self.option_file.grid(row=0, column=0, columnspan=2)

        self.entry_xml = ttk.Entry(frame, width=50)
        self.entry_xml.grid(row=1, column=1)
        self.entry_xml.insert(0, self.options['xml_dir'])

        self.button_ask_xml = ttk.Button(frame, text='XML Dir', command=self.ask_xml)
        self.button_ask_xml.grid(row=1, column=0)

        self.entry_pog = ttk.Entry(frame, width=50)
        self.entry_pog.grid(row=2, column=1)
        self.entry_pog.insert(0, self.options['pog_dir'])

        self.button_ask_pog = ttk.Button(frame, text='POG Dir', command=self.ask_pog)
        self.button_ask_pog.grid(row=2, column=0)

        self.entry_portrait = ttk.Entry(frame, width=50)
        self.entry_portrait.grid(row=3, column=1)
        self.entry_portrait.insert(0, self.options['portrait_dir'])

        self.button_ask_portrait = ttk.Button(frame, text='Portrait Dir', command=self.ask_portrait)
        self.button_ask_portrait.grid(row=3, column=0)

        self.entry_token = ttk.Entry(frame, width=50)
        self.entry_token.grid(row=4, column=1)
        self.entry_token.insert(0, self.options['token_dir'])

        self.button_ask_token = ttk.Button(frame, text='Token Dir', command=self.ask_token)
        self.button_ask_token.grid(row=4, column=0)

        self.button_prop_frame = ttk.Button(frame, text='Token Properties', command=self.prop_frame)
        self.button_prop_frame.grid(row=5, column=0, columnspan=2)

        self.button_option_frame = ttk.Button(frame, text='Token Options', command=self.options_frame)
        self.button_option_frame.grid(row=6, column=0, columnspan=2)

        self.button_process = ttk.Button(frame, text="Create Tokens", command=self.process_xml)
        self.button_process.grid(row=9, column=0, padx=5, pady=5)

        self.button_quit = ttk.Button(frame, text="Quit", command=frame.quit)
        self.button_quit.grid(row=9, column=1, padx=5, pady=5, sticky=tk.E)

    def config_change(self, index, value, op):

        config_file = self.option_file.var.get()
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        self.config_file = config_file
        self.options = config._sections['app']
        self.properties = config._sections['properties']
        self.entry_xml.delete(0, tk.END)
        self.entry_xml.insert(0, self.options['xml_dir'])
        self.entry_pog.delete(0, tk.END)
        self.entry_pog.insert(0, self.options['pog_dir'])
        self.entry_portrait.delete(0, tk.END)
        self.entry_portrait.insert(0, self.options['portrait_dir'])
        self.entry_token.delete(0, tk.END)
        self.entry_token.insert(0, self.options['token_dir'])

    def prop_frame(self):

        self.button_prop_frame['state'] = tk.DISABLED

        self.propFrame = tk.Toplevel()
        self.propFrame.title('Token Properties')

        self.propFrame.type = self.prop_frame_entry(0, 'Property Name')
        self.propFrame.name = self.prop_frame_entry(1, 'Character Name')
        self.propFrame.str = self.prop_frame_entry(2, 'Strength')
        self.propFrame.dex = self.prop_frame_entry(3, 'Dexterity')
        self.propFrame.con = self.prop_frame_entry(4, 'Constitution')
        self.propFrame.int = self.prop_frame_entry(5, 'Intelligence')
        self.propFrame.wis = self.prop_frame_entry(6, 'Wisdom')
        self.propFrame.cha = self.prop_frame_entry(7, 'Charisma')
        self.propFrame.race = self.prop_frame_entry(8, 'Race')
        self.propFrame.align = self.prop_frame_entry(9, 'Alignment')
        self.propFrame.pc = self.prop_frame_entry(10, 'Player')
        self.propFrame.hpc = self.prop_frame_entry(11, 'HP Current')
        self.propFrame.hpm = self.prop_frame_entry(12, 'HP Max')
        self.propFrame.speed = self.prop_frame_entry(13, 'Speed')
        self.propFrame.reach = self.prop_frame_entry(14, 'Reach')
        self.propFrame.ac = self.prop_frame_entry(15, 'AC Normal')
        self.propFrame.ac_flat = self.prop_frame_entry(16, 'AC Flatfooted')
        self.propFrame.ac_touch = self.prop_frame_entry(17, 'AC Touch')
        self.propFrame.cmd = self.prop_frame_entry(18, 'CMD')
        self.propFrame.cmd_flat = self.prop_frame_entry(19, 'CMD Flatfooted')
        self.propFrame.cmb = self.prop_frame_entry(20, 'CMB')
        self.propFrame.attk_melee = self.prop_frame_entry(21, 'Melee Attack')
        self.propFrame.attk_range = self.prop_frame_entry(22, 'Ranged Attack')
        self.propFrame.attk_bab = self.prop_frame_entry(23, 'BAB')

        self.propFrame.button_save = ttk.Button(self.propFrame, text="Save", command=self.prop_frame_save)
        self.propFrame.button_save.grid(row=24, column=0, padx=5, pady=5, columnspan=2)

    def prop_frame_entry(self, row, text):

        ttk.Label(self.propFrame, text=text + ':').grid(row=row, column=0)
        entry = ttk.Entry(self.propFrame, width=20)
        entry.grid(row=row, column=1, sticky=tk.W)
        entry.insert(0, self.properties[text.lower()])

        return entry

    def prop_frame_save(self):
        self.properties['property name'] = self.propFrame.type.get()
        self.properties['character name'] = self.propFrame.name.get()
        self.properties['strength'] = self.propFrame.str.get()
        self.properties['dexterity'] = self.propFrame.dex.get()
        self.properties['constitution'] = self.propFrame.con.get()
        self.properties['intelligence'] = self.propFrame.int.get()
        self.properties['wisdom'] = self.propFrame.wis.get()
        self.properties['charisma'] = self.propFrame.cha.get()
        self.properties['alignment'] = self.propFrame.align.get()
        self.properties['player'] = self.propFrame.pc.get()
        self.properties['hp current'] = self.propFrame.hpc.get()
        self.properties['hp max'] = self.propFrame.hpm.get()
        self.properties['speed'] = self.propFrame.speed.get()
        self.properties['reach'] = self.propFrame.reach.get()
        self.properties['ac normal'] = self.propFrame.ac.get()
        self.properties['ac flatfooted'] = self.propFrame.ac_flat.get()
        self.properties['ac touch'] = self.propFrame.ac_touch.get()
        self.properties['cmd'] = self.propFrame.cmd.get()
        self.properties['cmd flatfooted'] = self.propFrame.cmd_flat.get()
        self.properties['cmb'] = self.propFrame.cmb.get()
        self.properties['Melee Attack'] = self.propFrame.attk_melee.get()
        self.properties['Ranged Attack'] = self.propFrame.attk_range.get()
        self.properties['BAB'] = self.propFrame.attk_bab.get()

        tk.Toplevel.destroy(self.propFrame)

        self.button_prop_frame['state'] = tk.NORMAL

    def options_frame(self):

        self.button_option_frame['state'] = tk.DISABLED

        self.optionsFrame = tk.Toplevel()
        self.optionsFrame.title('Token Options')

        v = tk.IntVar()
        self.optionsFrame.vision = ttk.Checkbutton(self.optionsFrame, text='Use Multiple Darkvision Ranges',
                                                   variable=v, onvalue=1, offvalue=0)
        self.optionsFrame.vision.grid(row=0, column=0, sticky=tk.W)
        self.optionsFrame.vision.var = v
        self.optionsFrame.vision.var.set(self.options['vision'])

        v = tk.IntVar()
        self.optionsFrame.index = ttk.Checkbutton(self.optionsFrame, text='Create a Master Index Table',
                                                  variable=v, onvalue=1, offvalue=0)
        self.optionsFrame.index.grid(row=1, column=0, sticky=tk.W)
        self.optionsFrame.index.var = v
        self.optionsFrame.index.var.set(self.options['index'])

        ttk.Label(self.optionsFrame, text='Master Index Name:').grid(row=2, column=0)
        self.optionsFrame.index_name = ttk.Entry(self.optionsFrame, width=20)
        self.optionsFrame.index_name.grid(row=2, column=1, sticky=tk.W)
        self.optionsFrame.index_name.insert(0, self.options['index_name'])

        v = tk.IntVar()
        self.optionsFrame.maneuvers = ttk.Checkbutton(self.optionsFrame, text='Create Individual Maneuver Macros',
                                                      variable=v, onvalue=1, offvalue=0)
        self.optionsFrame.maneuvers.grid(row=3, column=0, sticky=tk.W)
        self.optionsFrame.maneuvers.var = v
        self.optionsFrame.maneuvers.var.set(self.options['maneuvers'])

        v = tk.IntVar()
        self.optionsFrame.weapons = ttk.Checkbutton(self.optionsFrame, text='Create Weapon Macros',
                                                    variable=v, onvalue=1, offvalue=0)
        self.optionsFrame.weapons.grid(row=4, column=0, sticky=tk.W)
        self.optionsFrame.weapons.var = v
        self.optionsFrame.weapons.var.set(self.options['weapons'])

        v = tk.IntVar()
        self.optionsFrame.skills = ttk.Checkbutton(self.optionsFrame, text='Create Skill Macros',
                                                   variable=v, onvalue=1, offvalue=0)
        self.optionsFrame.skills.grid(row=5, column=0, sticky=tk.W)
        self.optionsFrame.skills.var = v
        self.optionsFrame.skills.var.set(self.options['skills'])

        v = tk.IntVar()
        self.optionsFrame.hp = ttk.Checkbutton(self.optionsFrame, text='Create HP Change Macro',
                                               variable=v, onvalue=1, offvalue=0)
        self.optionsFrame.hp.grid(row=6, column=0, sticky=tk.W)
        self.optionsFrame.hp.var = v
        self.optionsFrame.hp.var.set(self.options['skills'])

        v = tk.IntVar()
        self.optionsFrame.items = ttk.Checkbutton(self.optionsFrame, text='Create Items Macro',
                                                  variable=v, onvalue=1, offvalue=0)
        self.optionsFrame.items.grid(row=7, column=0, sticky=tk.W)
        self.optionsFrame.items.var = v
        self.optionsFrame.items.var.set(self.options['items'])

        self.optionsFrame.button_save = ttk.Button(self.optionsFrame, text="Save", command=self.options_frame_save)
        self.optionsFrame.button_save.grid(row=8, column=0, padx=5, pady=5, columnspan=2)

    def options_frame_save(self):

        self.options['vision'] = self.optionsFrame.vision.var.get()
        self.options['index'] = self.optionsFrame.index.var.get()
        self.options['maneuvers'] = self.optionsFrame.maneuvers.var.get()
        self.options['index_name'] = self.optionsFrame.index_name.get()
        self.options['weapons'] = self.optionsFrame.weapons.var.get()
        self.options['skills'] = self.optionsFrame.skills.var.get()
        self.options['hp'] = self.optionsFrame.hp.var.get()
        self.options['items'] = self.optionsFrame.items.var.get()

        tk.Toplevel.destroy(self.optionsFrame)

        self.button_option_frame['state'] = tk.NORMAL

    def ask_xml(self):
        result = tkFileDialog.askdirectory(initialdir=self.options['xml_dir'])
        if result:
            self.options['xml_dir'] = result
            self.entry_xml.delete(0, tk.END)
            self.entry_xml.insert(0, result)

    def ask_token(self):
        result = tkFileDialog.askdirectory(initialdir=self.options['token_dir'])
        if result:
            self.options['token_dir'] = result
            self.entry_token.delete(0, tk.END)
            self.entry_token.insert(0, result)

    def ask_portrait(self):
        result = tkFileDialog.askdirectory(initialdir=self.options['portrait_dir'])
        if result:
            self.options['portrait_dir'] = result
            self.entry_portrait.delete(0, tk.END)
            self.entry_portrait.insert(0, result)

    def ask_pog(self):
        result = tkFileDialog.askdirectory(initialdir=self.options['pog_dir'])
        if result:
            self.options['pog_dir'] = result
            self.entry_pog.delete(0, tk.END)
            self.entry_pog.insert(0, result)

    def process_xml(self):

        config = ConfigParser.ConfigParser()
        config._sections['app'] = self.options
        config._sections['properties'] = self.properties

        with open(self.config_file, 'wb') as cf:
            config.write(cf)
            cf.close()

        self.progressFrame = tk.Toplevel()
        self.progressFrame.title('Conversion Progress')

        self.progressFrame.sbar = tk.Scrollbar(self.progressFrame)
        self.progressFrame.text = tk.Text(self.progressFrame, relief=tk.SUNKEN)
        self.progressFrame.text.grid(row=0, column=0)
        self.progressFrame.sbar.config(command=self.progressFrame.text.yview)
        self.progressFrame.text.config(yscrollcommand=self.progressFrame.sbar.set)
        self.progressFrame.sbar.grid(row=0, column=1, sticky=tk.N + tk.S)

        self.progressFrame.text.insert(tk.INSERT, 'Processing files...\n')

        self.progressFrame.button_done = ttk.Button(self.progressFrame, text="Close",
                                                    command=self.progressFrame.destroy)
        self.progressFrame.button_done.grid(row=1, column=0, columnspan=2)

        table = Table(self.options['token_dir'], self.options['index_name'])
        self.master_index = table.master_index
        if int(self.options['index']):
            self.progressFrame.text.insert(tk.INSERT, '\nSearching for and reading in old master index\n')

        for dirpath, dirnames, filenames in os.walk(self.options['xml_dir']):
            for filename in [f for f in filenames if f.endswith(".xml")]:
                xml_file = os.path.join(dirpath, filename)
                subdir = string.replace(dirpath, self.options['xml_dir'], '')
                self.progressFrame.text.insert(tk.INSERT, '\nParsing' + xml_file + '\n')
                tree = ET.parse(xml_file)
                root = tree.getroot()

                for char in root.iter('character'):
                    minions = char.find('minions')
                    char.remove(minions)
                    self.make_token(char, subdir, table.index_name)

                    for minion in minions.iter('character'):
                        self.make_token(minion, subdir, table.index_name)

        if int(self.options['index']):
            self.progressFrame.text.insert(tk.INSERT, '\nSaving master index: ' + table.index_name + '\n')
            table.save()
        self.progressFrame.text.insert(tk.INSERT, '\nCompleted')

    def make_token(self, char, subdir, index_name):
        token = Token(char, self.master_index, index_name)
        token.properties = self.properties
        token.options = self.options
        token.save(subdir)
        if subdir:
            self.progressFrame.text.insert(tk.INSERT, '   Creating ' + token.name + ' within folder ' + subdir[1:] + '\n')
        else:
            self.progressFrame.text.insert(tk.INSERT, '   Creating ' + token.name + '\n')

        self.master_index = token.master_index


def batch_mode(config_file):
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        options = config._sections['app']
        properties = config._sections['properties']
        print "Using config file: " + config_file + '\n'

        table = Table(options['token_dir'], options['index_name'])
        if int(options['index']):
            print 'Searching for and reading in old master index'

        for dirpath, dirnames, filenames in os.walk(options['xml_dir']):
            for filename in [f for f in filenames if f.endswith(".xml")]:
                xml_file = os.path.join(dirpath, filename)
                subdir = string.replace(dirpath, options['xml_dir'], '')
                print '\nParsing' + xml_file
                tree = ET.parse(xml_file)
                root = tree.getroot()

                for char in root.iter('character'):
                    minions = char.find('minions')
                    char.remove(minions)
                    table.master_index = make_token(char, subdir, table.index_name, table.master_index, properties,
                                                    options)

                    for minion in minions.iter('character'):
                        table.master_index = make_token(minion, subdir, table.index_name, table.master_index,
                                                        properties, options)

        if int(options['index']):
            print '\nSaving master index: ' + table.index_name
            table.save()
        print '\nCompleted'


def make_token(char, subdir, index_name, master_index, properties, options):
    token = Token(char, master_index, index_name)
    token.properties = properties
    token.options = options
    token.save(subdir)
    if subdir:
        print '   Creating ' + token.name + ' within folder ' + subdir[1:]
    else:
        print '   Creating ' + token.name

    return token.master_index

parser = argparse.ArgumentParser(
    prog='main',
    description='''This is the Hero Lab to Token converter.

This script will parse a directory of HeroLab exports and convert any characters/monsters there into token files.
Each character in the XML file should have a portrait and POG image that matches the character name.''')

parser.add_argument('--config', help="Alternate config file.", default='default.conf', dest='config')
parser.add_argument('--batch', help="Run in batch mode.", action='store_true')

options = parser.parse_args()

if options.batch:
    batch_mode(options.config)
else:
    root = tk.Tk()
    app = App(root, options.config)
    root.mainloop()