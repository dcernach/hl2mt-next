import Tkinter as tk
import ttk
import xml.etree.ElementTree as ET
import tkFileDialog
import ConfigParser
import argparse
import os
import glob
import string
import re
import zipfile
from pathfinder import Token, MasterIndex


class App:
    def __init__(self, master, config_file):

        config = ConfigParser.ConfigParser()
        if os.path.isfile(config_file):
            config.read(config_file)
            if 'app' in config._sections:
                self.options = config._sections['app']
            else:
                self.options = {}
            if 'properties' in config._sections:
                self.properties = config._sections['properties']
            else:
                self.properties = {}
            if 'colors' in config._sections:
                self.colors = config._sections['colors']
            else:
                self.colors = {}

        self.check_defaults()

        self.filenames = []
        self.config_file = config_file

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

        self.entry_input = ttk.Entry(frame, width=50)
        self.entry_input.grid(row=1, column=1)
        self.entry_input.insert(0, self.options['input_dir'])

        self.button_ask_input = ttk.Button(frame, text='Input Dir', command=self.ask_input)
        self.button_ask_input.grid(row=1, column=0)

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

        self.button_index_frame = ttk.Button(frame, text='Indexing Options', command=self.index_frame)
        self.button_index_frame.grid(row=7, column=0, columnspan=2)

        self.button_color_frame = ttk.Button(frame, text='Macro Colors', command=self.color_frame)
        self.button_color_frame.grid(row=8, column=0, columnspan=2)

        self.button_process = ttk.Button(frame, text="Create Tokens", command=self.process_xml)
        self.button_process.grid(row=9, column=0, padx=5, pady=5)

        self.button_quit = ttk.Button(frame, text="Quit", command=frame.quit)
        self.button_quit.grid(row=9, column=1, padx=5, pady=5, sticky=tk.E)

    def check_defaults(self):

        for opt in ['input_dir', 'pog_dir', 'token_dir', 'portrait_dir']:
            if opt not in self.options:
                self.options[opt] = os.getcwd()

        for opt in ['vision', 'maneuvers', 'weapons', 'skills', 'hp', 'basic dice', 'items']:
            if opt not in self.options:
                self.options[opt] = 0

        if 'index' not in self.options:
            self.options['index'] = 'None'

        types = ['None', 'Maptool Table', 'Remote HTML: Zip', 'Remote HTML: SSH']
        if self.options['index'] not in types:
            self.options['index'] = 'None'

        if 'table_name' not in self.options:
            self.options['table_name'] = 'HeroLabIndex'

        if 'zipfile' not in self.options:
            self.options['zipfile'] = 'HeroLabIndex.zip'

        for opt in ['http_base', 'ssh_host', 'ssh_user', 'ssh_dir']:
            if opt not in self.options:
                self.options[opt] = ''

        if 'property name' not in self.properties:
            self.properties['property name'] = 'Basic'
        if 'character name' not in self.properties:
            self.properties['character name'] = 'Name'
        if 'hp max' not in self.properties:
            self.properties['hp max'] = 'HP'
        if 'speed' not in self.properties:
            self.properties['speed'] = 'Movement'

        for opt in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'race', 'alignment']:
            if opt not in self.properties:
                self.properties[opt] = opt.title()

        for opt in ['player', 'hp current', 'initiative', 'reach', 'ac normal', 'ac flatfooted', 'ac touch', 'cmd',
                    'cmd flatfooted', 'cmb', 'melee attack', 'ranged attack', 'bab']:
            if opt not in self.properties:
                self.properties[opt] = ''

        for opt in ['sheet', 'skills', 'attacks', 'hp', 'init', 'cmb', 'saves', 'specials', 'basic die', 'maneuvers',
                    'submacros']:
            if opt + ' background' not in self.colors:
                self.colors[opt + ' background'] = 'white'
            if opt + ' font' not in self.colors:
                self.colors[opt + ' font'] = 'black'

    def config_change(self, index, value, op):

        config_file = self.option_file.var.get()
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        self.config_file = config_file
        if 'app' in config._sections:
            self.options = config._sections['app']
        else:
            self.options = {}
        if 'properties' in config._sections:
            self.properties = config._sections['properties']
        else:
            self.properties = {}
        if 'colors' in config._sections:
            self.colors = config._sections['colors']
        else:
            self.colors = {}

        self.check_defaults()
        self.entry_input.delete(0, tk.END)
        self.entry_input.insert(0, self.options['input_dir'])
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
        self.properties['melee attack'] = self.propFrame.attk_melee.get()
        self.properties['ranged attack'] = self.propFrame.attk_range.get()
        self.properties['bab'] = self.propFrame.attk_bab.get()

        tk.Toplevel.destroy(self.propFrame)

        self.button_prop_frame['state'] = tk.NORMAL

    def color_frame(self):

        self.button_color_frame['state'] = tk.DISABLED

        self.colorFrame = tk.Toplevel()
        self.colorFrame.title('Macro Colors')

        self.colorFrame.sheet_f, self.colorFrame.sheet_b = self.color_frame_entry(0, 'Sheet')
        self.colorFrame.skills_f, self.colorFrame.skills_b = self.color_frame_entry(1, 'Skills')
        self.colorFrame.attacks_f, self.colorFrame.attacks_b = self.color_frame_entry(2, 'Attacks')
        self.colorFrame.hp_f, self.colorFrame.hp_b = self.color_frame_entry(3, 'HP')
        self.colorFrame.init_f, self.colorFrame.init_b = self.color_frame_entry(4, 'Init')
        self.colorFrame.cmb_f, self.colorFrame.cmb_b = self.color_frame_entry(5, 'CMB')
        self.colorFrame.saves_f, self.colorFrame.saves_b = self.color_frame_entry(6, 'Saves')
        self.colorFrame.specials_f, self.colorFrame.specials_b = self.color_frame_entry(7, 'Specials')
        self.colorFrame.basic_f, self.colorFrame.basic_b = self.color_frame_entry(8, 'Basic Die')
        self.colorFrame.maneuv_f, self.colorFrame.maneuv_b = self.color_frame_entry(9, 'Maneuvers')
        self.colorFrame.sub_f, self.colorFrame.sub_b = self.color_frame_entry(10, 'Submacros')

        self.colorFrame.button_save = ttk.Button(self.colorFrame, text="Save", command=self.color_frame_save)
        self.colorFrame.button_save.grid(row=11, column=0, padx=5, pady=5, columnspan=5)

    def color_frame_entry(self, row, text):

        colors = sorted(['white', 'black', 'cyan', 'aqua', 'blue', 'darkgray', 'fuchsia', 'gray', 'green', 'lightgray',
                         'lime', 'magenta', 'maroon', 'navy', 'olive', 'orange', 'pink', 'purple', 'red', 'silver',
                         'teal', 'yellow', 'gray25', 'gray50', 'gray75'])

        ttk.Label(self.colorFrame, text=text).grid(row=row, column=0, sticky=tk.W)

        ttk.Label(self.colorFrame, text='  Font:').grid(row=row, column=1)
        v = tk.StringVar()
        entry1 = ttk.Combobox(self.colorFrame, textvariable=v, state='readonly', width=10)
        entry1.var = v
        entry1.var.set(self.colors[text.lower() + ' font'])
        entry1['values'] = colors
        entry1.grid(row=row, column=2, sticky=tk.W)

        ttk.Label(self.colorFrame, text='  Background:').grid(row=row, column=3)
        v = tk.StringVar()
        entry2 = ttk.Combobox(self.colorFrame, textvariable=v, state='readonly', width=10)
        entry2.var = v
        entry2.var.set(self.colors[text.lower() + ' background'])
        entry2['values'] = colors
        entry2.grid(row=row, column=4, sticky=tk.W)

        return entry1, entry2

    def color_frame_save(self):
        self.colors['sheet font'] = self.colorFrame.sheet_f.get()
        self.colors['sheet background'] = self.colorFrame.sheet_b.get()
        self.colors['skills font'] = self.colorFrame.skills_f.get()
        self.colors['skills background'] = self.colorFrame.skills_b.get()
        self.colors['attacks font'] = self.colorFrame.attacks_f.get()
        self.colors['attacks background'] = self.colorFrame.attacks_b.get()
        self.colors['hp font'] = self.colorFrame.hp_f.get()
        self.colors['hp background'] = self.colorFrame.hp_b.get()
        self.colors['init font'] = self.colorFrame.init_f.get()
        self.colors['init background'] = self.colorFrame.init_b.get()
        self.colors['cmb font'] = self.colorFrame.cmb_f.get()
        self.colors['cmb background'] = self.colorFrame.cmb_b.get()
        self.colors['saves font'] = self.colorFrame.saves_f.get()
        self.colors['saves background'] = self.colorFrame.saves_b.get()
        self.colors['specials font'] = self.colorFrame.specials_f.get()
        self.colors['specials background'] = self.colorFrame.specials_b.get()
        self.colors['basic die font'] = self.colorFrame.basic_f.get()
        self.colors['basic die background'] = self.colorFrame.basic_b.get()
        self.colors['maneuvers font'] = self.colorFrame.maneuv_f.get()
        self.colors['maneuvers background'] = self.colorFrame.maneuv_b.get()
        self.colors['submacros font'] = self.colorFrame.sub_f.get()
        self.colors['submacros background'] = self.colorFrame.sub_b.get()

        tk.Toplevel.destroy(self.colorFrame)

        self.button_color_frame['state'] = tk.NORMAL

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

        v = tk.IntVar()
        self.optionsFrame.basic = ttk.Checkbutton(self.optionsFrame, text='Create Basic Dice Macros',
                                                  variable=v, onvalue=1, offvalue=0)
        self.optionsFrame.basic.grid(row=8, column=0, sticky=tk.W)
        self.optionsFrame.basic.var = v
        self.optionsFrame.basic.var.set(self.options['basic dice'])

        self.optionsFrame.button_save = ttk.Button(self.optionsFrame, text="Save", command=self.options_frame_save)
        self.optionsFrame.button_save.grid(row=9, column=0, padx=5, pady=5, columnspan=2)

    def options_frame_save(self):

        self.options['vision'] = self.optionsFrame.vision.var.get()
        self.options['maneuvers'] = self.optionsFrame.maneuvers.var.get()
        self.options['weapons'] = self.optionsFrame.weapons.var.get()
        self.options['skills'] = self.optionsFrame.skills.var.get()
        self.options['hp'] = self.optionsFrame.hp.var.get()
        self.options['basic dice'] = self.optionsFrame.basic.var.get()
        self.options['items'] = self.optionsFrame.items.var.get()

        tk.Toplevel.destroy(self.optionsFrame)

        self.button_option_frame['state'] = tk.NORMAL

    def index_frame(self):

        self.button_index_frame['state'] = tk.DISABLED

        self.indexFrame = tk.Toplevel()
        self.indexFrame.title('Index Options')

        # Currently 2 supported options, table and remote html indexes

        types = ['None', 'Maptool Table', 'Remote HTML: Zip']

        ttk.Label(self.indexFrame, text='Index Option').grid(row=0, column=0)
        v = tk.StringVar()
        self.indexFrame.index = ttk.Combobox(self.indexFrame, textvariable=v, state='readonly', width=20)
        self.indexFrame.index.var = v
        self.indexFrame.index.var.set(self.options['index'])
        self.indexFrame.index['values'] = types
        self.indexFrame.index.var.trace('w', self.index_change)
        self.indexFrame.index.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(self.indexFrame, text='Maptool Table Name:').grid(row=1, column=0)
        self.indexFrame.table_name = ttk.Entry(self.indexFrame, width=20)
        self.indexFrame.table_name.grid(row=1, column=1, sticky=tk.W)
        self.indexFrame.table_name.insert(0, self.options['table_name'])

        ttk.Label(self.indexFrame, text='Base HTTP URL:').grid(row=2, column=0)
        self.indexFrame.http_base = ttk.Entry(self.indexFrame, width=20)
        self.indexFrame.http_base.grid(row=2, column=1, sticky=tk.W)
        self.indexFrame.http_base.insert(0, self.options['http_base'])

        ttk.Label(self.indexFrame, text='Zip Filename:').grid(row=3, column=0)
        self.indexFrame.zipfile = ttk.Entry(self.indexFrame, width=20)
        self.indexFrame.zipfile.grid(row=3, column=1, sticky=tk.W)
        self.indexFrame.zipfile.insert(0, self.options['zipfile'])

        # ttk.Label(self.indexFrame, text='SSH Host:').grid(row=4, column=0)
        # self.indexFrame.ssh_host = ttk.Entry(self.indexFrame, width=20)
        # self.indexFrame.ssh_host.grid(row=4, column=1, sticky=tk.W)
        # self.indexFrame.ssh_host.insert(0, self.options['ssh_host'])
        #
        # ttk.Label(self.indexFrame, text='SSH Username:').grid(row=5, column=0)
        # self.indexFrame.ssh_user = ttk.Entry(self.indexFrame, width=20)
        # self.indexFrame.ssh_user.grid(row=5, column=1, sticky=tk.W)
        # self.indexFrame.ssh_user.insert(0, self.options['ssh_user'])
        #
        # ttk.Label(self.indexFrame, text='SSH Directory:').grid(row=6, column=0)
        # self.indexFrame.ssh_dir = ttk.Entry(self.indexFrame, width=20)
        # self.indexFrame.ssh_dir.grid(row=6, column=1, sticky=tk.W)
        # self.indexFrame.ssh_dir.insert(0, self.options['ssh_dir'])

        self.indexFrame.button_save = ttk.Button(self.indexFrame, text="Save", command=self.index_frame_save)
        self.indexFrame.button_save.grid(row=7, column=0, padx=5, pady=5, columnspan=2)

        self.index_change(0, 0, 0)

    def index_change(self, index, value, op):
        index_type = self.indexFrame.index.var.get()

        if index_type == 'Maptool Table':
            self.indexFrame.table_name['state'] = tk.NORMAL
            self.indexFrame.http_base['state'] = tk.DISABLED
            self.indexFrame.zipfile['state'] = tk.DISABLED
            # self.indexFrame.ssh_host['state'] = tk.DISABLED
            # self.indexFrame.ssh_user['state'] = tk.DISABLED
            # self.indexFrame.ssh_dir['state'] = tk.DISABLED
        elif index_type == 'Remote HTML: Zip':
            self.indexFrame.table_name['state'] = tk.DISABLED
            self.indexFrame.http_base['state'] = tk.NORMAL
            self.indexFrame.zipfile['state'] = tk.NORMAL
            # self.indexFrame.ssh_host['state'] = tk.DISABLED
            # self.indexFrame.ssh_user['state'] = tk.DISABLED
            # self.indexFrame.ssh_dir['state'] = tk.DISABLED
        # elif index_type == 'Remote HTML: SSH':
        #     self.indexFrame.table_name['state'] = tk.DISABLED
        #     self.indexFrame.http_base['state'] = tk.NORMAL
        #     self.indexFrame.zipfile['state'] = tk.DISABLED
        #     self.indexFrame.ssh_host['state'] = tk.NORMAL
        #     self.indexFrame.ssh_user['state'] = tk.NORMAL
        #     self.indexFrame.ssh_dir['state'] = tk.NORMAL
        else:
            self.indexFrame.table_name['state'] = tk.DISABLED
            self.indexFrame.http_base['state'] = tk.DISABLED
            self.indexFrame.zipfile['state'] = tk.DISABLED
            # self.indexFrame.ssh_host['state'] = tk.DISABLED
            # self.indexFrame.ssh_user['state'] = tk.DISABLED
            # self.indexFrame.ssh_dir['state'] = tk.DISABLED

    def index_frame_save(self):

        self.options['index'] = self.indexFrame.index.var.get()
        self.options['table_name'] = self.indexFrame.table_name.get()
        self.options['http_base'] = self.indexFrame.http_base.get()
        self.options['zipfile'] = self.indexFrame.zipfile.get()
        # self.options['ssh_host'] = self.indexFrame.ssh_host.get()
        # self.options['ssh_user'] = self.indexFrame.ssh_user.get()
        # self.options['ssh_dir'] = self.indexFrame.ssh_dir.get()

        tk.Toplevel.destroy(self.indexFrame)

        self.button_index_frame['state'] = tk.NORMAL

    def options_close(self):
        tk.Toplevel.destroy(self.optionsFrame)
        self.button_option_frame['state'] = tk.NORMAL

    def progress_close(self):
        tk.Toplevel.destroy(self.progressFrame)
        self.button_process['state'] = tk.NORMAL

    def ask_input(self):
        result = tkFileDialog.askdirectory(initialdir=self.options['input_dir'])
        if result:
            self.options['input_dir'] = result
            self.entry_input.delete(0, tk.END)
            self.entry_input.insert(0, result)

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

        self.button_process['state'] = tk.DISABLED

        config = ConfigParser.ConfigParser()
        config._sections['app'] = self.options
        config._sections['properties'] = self.properties
        config._sections['colors'] = self.colors

        with open(self.config_file, 'wb') as cf:
            config.write(cf)
            cf.close()

        self.progressFrame = tk.Toplevel()
        self.progressFrame.title('Conversion Progress')

        self.progressFrame.sbar = tk.Scrollbar(self.progressFrame)
        self.progressFrame.text = tk.Text(self.progressFrame, relief=tk.SUNKEN)
        self.progressFrame.text.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        self.progressFrame.sbar.config(command=self.progressFrame.text.yview)
        self.progressFrame.text.config(yscrollcommand=self.progressFrame.sbar.set)
        self.progressFrame.sbar.grid(row=0, column=1, sticky=tk.N + tk.S)
        tk.Grid.rowconfigure(self.progressFrame, 0, weight=1)
        tk.Grid.columnconfigure(self.progressFrame, 0, weight=1)

        self.progressFrame.text.insert(tk.INSERT, 'Processing files...\n')

        self.progressFrame.button_done = ttk.Button(self.progressFrame, text="Close",
                                                    command=self.progress_close)
        self.progressFrame.button_done.grid(row=1, column=0, columnspan=2)
        self.progressFrame.button_done['state'] = tk.DISABLED

        self.progressFrame.update()

        self.master_index = MasterIndex(self.options)
        self.filenames = []

        for dirpath, dirnames, filenames in os.walk(self.options['input_dir']):
            for filename in [f for f in filenames if f.endswith(".xml")]:
                xml_file = os.path.join(dirpath, filename)
                subdir = string.replace(dirpath, self.options['input_dir'], '')
                self.progressFrame.text.insert(tk.INSERT, '\nParsing ' + xml_file + '\n')
                self.progressFrame.update()
                self.progressFrame.text.see(tk.END)
                tree = ET.parse(xml_file)
                root = tree.getroot()

                for char in root.iter('character'):
                    minions = char.find('minions')
                    char.remove(minions)
                    self.make_token(char, subdir)

                    for minion in minions.iter('character'):
                        self.make_token(minion, subdir)

            # Parse Por/Stock files
            for filename in [f for f in filenames if f.endswith(".por") or f.endswith(".stock")]:
                lab_file = os.path.join(dirpath, filename)
                subdir = string.replace(dirpath, self.options['input_dir'], '')
                self.progressFrame.text.insert(tk.INSERT, '\nReading ' + lab_file + '\n')
                self.progressFrame.update()
                self.progressFrame.text.see(tk.END)

                try:
                    lab_zip = zipfile.ZipFile(lab_file, 'r')
                    for name in lab_zip.namelist():
                        if re.search('statblocks_xml.*\.xml', name):
                            xml_file = lab_zip.open(name)
                            self.progressFrame.text.insert(tk.INSERT, '\nParsing ' + name + '\n')
                            self.progressFrame.update()
                            self.progressFrame.text.see(tk.END)
                            tree = ET.parse(xml_file)
                            xml_file.close()
                            root = tree.getroot()

                            for char in root.iter('character'):
                                minions = char.find('minions')
                                char.remove(minions)
                                self.make_token(char, subdir)

                                for minion in minions.iter('character'):
                                    self.make_token(minion, subdir)
                    lab_zip.close()
                except zipfile.BadZipfile:
                    self.progressFrame.text.insert(tk.INSERT, '!!! ' + filename +
                                                              ' does not appear to be in zip format\n')
                    self.progressFrame.text.see(tk.END)

        if self.options['index'] == 'Maptool Table':
            self.progressFrame.text.insert(tk.INSERT, '\nSaving ' + self.options['token_dir'] +
                                                      '/' + self.options['table_name'] + '.mttable' + '\n')
            self.progressFrame.update()
            self.progressFrame.text.see(tk.END)
            self.master_index.save()
        elif self.options['index'] == 'Remote HTML: Zip':
            self.progressFrame.text.insert(tk.INSERT, '\nSaving ' + self.options['token_dir'] + '/' +
                                                      self.options['zipfile'] + '\n')
            self.progressFrame.update()
            self.progressFrame.text.see(tk.END)
            self.master_index.save()

        self.progressFrame.text.insert(tk.INSERT, '\nCompleted')
        self.progressFrame.update()
        self.progressFrame.text.see(tk.END)
        self.progressFrame.button_done['state'] = tk.NORMAL

    def make_token(self, char, subdir):
        token = Token(char, self.master_index)
        token.properties = self.properties
        token.options = self.options
        token.colors = self.colors
        token.filenames = self.filenames
        token.save(subdir)
        self.progressFrame.text.insert(tk.INSERT, '   Writing ' + token.filename + '\n')

        self.filenames.append(token.filename)

parser = argparse.ArgumentParser(
    prog='main',
    description='''This is the Hero Lab to Token converter.

This script will parse a directory of HeroLab exports and convert any characters/monsters there into token files.
Each character in the XML file should have a portrait and POG image that matches the character name.''')

parser.add_argument('--config', help="Alternate config file.", default='default.conf', dest='config')

options = parser.parse_args()

root = tk.Tk()
app = App(root, options.config)
root.mainloop()