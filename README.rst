=========
hl2mt: Hero Lab to Maptool
=========

About
-----

``hl2mt`` parses XML output from `Hero Lab <http://wolflair.com/index.php?context=hero_lab>`_ and converts it into
usable Maptool_ tokens that have basic die roll macros and text references. hl2mt is a Python_ application that has a
Tkinter_ graphical interface that will run under Linux, Mac and Windows. The application has a lot of configuration
options that should allow anyone to customize the created tokens so they work with existing Maptool_ frameworks.


Installation
------------

First you're going to need to install Python_ if you don't already have it installed. hl2mt uses Python 2.7 and on
Windows you'll need to download PIL_, the Python Imaging Library. If you're running 64bit Windows I'd highly recommend
installing the 32bit versions of Python_ and PIL_. The 64bit version of PIL_ doesn't install correctly.

On Linux systems you'll need the following libraries:

    python-tk

    python-imaging

Once you have Python_ installed you can download_ the zip file for hl2mt, unzip it and double click on the main.py
file. That should bring up the application.


Running
-------

In Windows after installing Python_ and PIL_, double click on the main.py file.

In Linux run it as per the below:

    python main.py


Usage
-----

The basic usage concept behind hl2mt is you do up your encounters, PCs and monsters in Hero Lab and then save them
into a directory. hl2mt then opens the files, parses the XML, pulls out the creatures and associates a portrait and
token image to them. It then saves the creature into a Maptool token. To do this hl2mt needs 4 directories:

- Input Dir: Where the Hero Lab XML, por or stock files are
- POG Dir: Where hl2mt will search for token images for each creature
- Portrait Dir: Where hl2mt will search for portrait images for each creature
- Token Dir: Where hl2mt will save the tokens

The filename on the Hero Lab file doesn't matter. It's the creature names that hl2mt works with. If you have an orcs.por
file with an Orc, Orc Champion and Chief Orc hl2mt will individually create "Orc", "Orc Champion" and "Chief Orc" tokens
and expect to find image files with those names in the POG and Portrait directories.

Image Files
-----------

A Maptool token has 2 images attached to it. It has a token image(which is called POG in hl2mt) and a portrait image.
hl2mt is designed to work with large batches of tokens so rather than click through and assign proper images to each
creature it attempts to intelligently associate token/portrait images to each creature created in Hero Lab.

Assuming your creature is named Kobold Champion, hl2mt will try to find images named the following way:

- Kobold?Champion.*
- Kobold.*
- Champion.*
- Kobold*
- Champion*
- Default.*

Note that if your Hero Lab file is in a sub-directory, hl2mt will first search for images in the same sub-directory
in the image folders. If hl2mt can't find a file, it'll use a random file in the parent image directory.

What this means is you can create tokens and portraits for basic types(skeleton, human, orc, elf) and create
Hero Lab encounters that reference Orc Champion, Elf Archer, Human Wizard and it'll find the basic type. Later
you could go back and add a POG/Portrait for Orc Champion and re-run hl2mt and it'll update your Orc Champion
token with the new images.

Also you're able to use sub-directories to further setup good defaults. You can create a Dragons directory and put
in a Default.png image for a generic dragon, and then later put in images for Gold, Red, Blue and so on.

To keep the token sizes down hl2mt will process any image you have in these directories. For portraits the
image is downsized to be within 200x200 pixels and converted to PNG. For POGs the image is downsized to be within
128x128 pixels and converted to PNG.


Token Properties
----------------

Within Maptool there's a `campaign properties <http://lmwcs.com/rptools/wiki/Introduction_to_Properties>`_ option
which allows you to set properties(variables) onto tokens. By default there's a simple Basic campaign property
that has a few simple settings on it. Most frameworks create their own campaign properties and assign a lot more
values to a token that the framework manipulates via macros.

hl2mt allows you to customize how the Hero Lab data gets converted into token properties. Below are the properties
hl2mt works with:

- Property Name: The campaign property name(Basic, Pathfinder, etc)
- Character Name: What property the character name in Hero Lab should be assigned to
- Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma: The numerical stat
- Race, Alignment, Player: Basic character information
- HP Current: The current hit points of the creature(after damage is applied)
- HP Max: The max hit points of the creature
- Initiative, Speed, Reach: More basic stats
- AC Normal, AC flatfooted, AC touch: Basic defenses
- CMD, CMD Flatfooted: Maneuver defenses
- CMB: The creature's basic CMB
- Melee Attack, Ranged Attack, BAB: Basic attack values

Each field can take multiple inputs. For example if you wanted a creature's Max HP to show up under HP and HP_MAX
token properties, you'd use

    HP Max: HP,HP_MAX

Do not put spaces between the comma and property names.

If your framework requires other token properties please let me know and I can add them in.

Token Options
-------------

Not everyone wants all the same things on their tokens, so here you can optionally choose what you want on your
created tokens.

**Multiple Darkvision Ranges**

Basic campaign frameworks typically just have a single Darkvision vision property that's assumed to be 60ft in
range. Pathfinder however has races with different ranges of darkvision. If your framework supports these, you
can click this option and your token will output darkvision in the following way: Darkvision30, Darkvision60,
Darkvision120 and Lowlight, etc. It'll read proper darkvision ranges from Hero Lab and append it to "Darkvision".

**Individual Maneuver Macros**

Hero Lab has individual values for all the maneuvers(trip, bull rush, etc). If you'd prefer to see a macro for
each maneuver in addition to the basic CMB macro, click this option. This can be useful if you have creatures
who have bonuses to certain maneuvers.

**Skill Macros**

This option will create a macro for every skill the creature has. These are very simple "d20 + skill" dice rolling
macros.

**Weapon Macros**

Hero Lab contains attack to hit and damage data for every weapon carried by creatures(including natural attacks).
If you'd like a weapon to-hit/damage roll macro created click this option. hl2mt will attempt to eliminate duplicate
items(if your PCs like to carry 20 daggers) and will also create a Thrown option for any weapon that can also be
thrown.

**Basic Dice Macros**

These are just macros for basic die rolls: d4, d6, d8, d10, d12 and d20

They can be useful if you have newer players who aren't using to typing die rolls into chat.

**Items Macro**

This is a simple list of every item carried by the creature. Unfortunately it's not editable as that requires forms
which would necessitate the use of library tokens.

**HP Change Macro**

This will create a very simple hit point change macro. If your token properties includes both current and max hp
fields then hl2mt will work with both and create a macro that uses a health bar over your tokens. If you only
have max hp on your framework then hl2mt will create a simpler macro which only works with that.

Indexing Options
-------------

Hero Lab outputs extremely detailed data on feats, traits, special abilities, spells and so on in the output it
generates for your creatures. This is too much data to store on each token. If your library has 100 spellcasters
all with magic missile it's wasteful to have 100 copies of magic missile described in your campaign. Also some
creatures might have hundreds of feats, special abilities and spells and trying to include very detailed descriptions
for each in a single token would make the token very unwieldy to work with in.

So by default when hl2mt creates tokens it doesn't include this detailed data. Instead it creates simple lists
on the token of feats, spells and so on, unless you turn on master indexing.

** Maptool Table indexing **

If you turn on table indexing hl2mt will build a master index table of all your parsed creature's feats, spells,
specials and so on and when it finishes it'll save all of that data into a
`Maptool table <http://www.youtube.com/watch?v=Lqfi0-5CEF4>`_ file(in the token directory) which you'll then need
to import into Maptool whenever you run hl2mt.

hl2mt will read in an existing created master index table and re-parse old index data, so old tokens shouldn't break
when you add new ones. However if you ever delete your old index table file and run hl2mt with new creatures you'll
likely break your old tokens.

For example, let's say I have a skeleton on the map and my index table looks like:

    1: Your quick reflexes allow you to react rapidly to danger...

This is the skeleton's improved initiative feat. When I click on his feats macro and click on improved initiative
it points to the 1st row in my master index table.

If I leave a skeleton token on the map, delete my on disk table file and run hl2mt with an orc and skeleton in the XML
dir, the orc feats/specials will come first and the first row in my index table will no longer be improved initiative.
My skeleton, on the table, will be broken when I load in the new index table(which has the orc data). New skeletons
in the token library will work fine, they've been built with the new index, it's old tokens on the map that'll be
out of date.

For this reason it can be a good idea to work with multiple indexes. For example when creating a Crypt of the
Everflame campaign file I use a CryptEverFlame index with XML/Token dirs that are only for crypt creatures. I can
build my module using that, save it, and in play I can use a different index and not have to worry about
breaking any of my old crypt module creatures that I've placed. In fact once this module is done the tokens I've
created in it should never go stale, since they're referencing the static CryptEverFlame table in the saved campaign
file. So you can keep a module around for years, or mail to other people, and the tokens saved within it should
always work.

Another example of use, let's say I'm a player and my DM is running a Maptool game but doesn't use hl2mt. If my
PC name is Buddy Jesus I can create a BuddyJ index, use BuddyJ campaign properties and create my token against those.
Then I can email to the DM my token, index and campaign properties file and he can import all three into any campaign
and I can use my token the way I want to.

** Remote HTML: Zip **

While table indexes work pretty well and have the benefit that they create self contained campaigns, tables can grow
to become excessively large. For example in my current install with 240 tokens hl2mt builds a table with nearly 800
entries. This can potentially slow down Maptools on a slow computer. As an option if you download and use the Nerps_
variant of Maptool you can store all the index information in html pages on a remote web server.

Simple choose this option, input the base URL of where you'll unpack the index files and hl2mt will pack all the html
pages into a zip file you can upload to your server.



Plans
-----

Generally there are no plans to add in advanced macro functions. The goal of hl2mt is to instead try to be as
compatible as possible for existing frameworks. If you have a framework and you want it to work with hl2mt please
let me know and I'll try to work with you to export the data from Hero Lab into a format your framework can use.


License
-------

``hl2mt`` is released under the GPLv3 license.

.. _maptool: http://www.rptools.net/?page=maptool
.. _python: http://www.python.org/
.. _tkinter: http://docs.python.org/2/library/tkinter.html
.. _download: http://hg.tarsis.org/hl2mt/archive/tip.zip
.. _pil: http://www.pythonware.com/products/pil/
.. _nerps: https://docs.google.com/file/d/0B2c01YG2XtiJTzA3Z2tEN0lIVk0/edit?usp=sharing