=========
hl2mt: Hero Lab to Maptool
=========

About
-----

``hl2mt`` parses output from `Hero Lab <http://wolflair.com/index.php?context=hero_lab>`_ and converts it into
usable Maptool_ tokens that have basic die roll macros and text references. ``hl2mt`` is a Python_ application that has a
Qt_ graphical interface that will run under Linux, Mac and Windows. The application has a lot of configuration
options that should allow anyone to customize the created tokens so they work with existing Maptool_ frameworks.

Here you can see a demo of the application: `Quick Overview <http://www.youtube.com/watch?v=ZRYboqOyiyM>`_


.. image:: http://tarsis.org/images/hl2mt.png


Downloading
------------

There are binaries for Windows, Linux and Mac:

`Windows Binary <http://tarsis.org/builds/hl2mt.exe>`_

`Linux 32bit Binary <http://tarsis.org/builds/hl2mt.i386>`_

`Linux 64bit Binary <http://tarsis.org/builds/hl2mt.amd64>`_

`OS X Mountain Lion 64bit Binary <http://tarsis.org/builds/hl2mt.dmg>`_

Simply download the version for your platform and double click to run.

Video Tutorials
---------------

There are video tutorials covering the basic features ``hl2mt``

`Tutorial 1 - Basic Usage <http://www.youtube.com/watch?v=LXPJk72QUCs>`_

`Tutorial 2 - Folders <http://www.youtube.com/watch?v=gMPr0a2t5oI>`_

`Tutorial 3 - Making use of sub-folders <http://www.youtube.com/watch?v=maqZ5DoPUqg>`_

`Tutorial 4 - Token Properties <http://www.youtube.com/watch?v=TtzymzEyw2s>`_

`Tutorial 5 - Indexes <http://www.youtube.com/watch?v=nY3VXWjtM2U>`_

`Tutorial 6 - Using Dropbox to host indexes <https://www.youtube.com/watch?v=cGpZb1Fp7Vo>`_

`Tutorial 7 - The Community Bestiary <http://www.youtube.com/watch?v=_Eeq6XTIMaE>`_


Usage
-----

The basic usage concept behind ``hl2mt`` is you do up your encounters, PCs and monsters in Hero Lab and then save them
into a directory. ``hl2mt`` then opens the files, parses the data, pulls out the creatures and associates a portrait and
token image to them. It then saves the creature into a Maptool token. To do this ``hl2mt`` needs 4 directories:

- Input Directory: Where the Hero Lab save files are
- POG Directory: Where ``hl2mt`` will search for token images for each creature
- Portrait Directory: Where ``hl2mt`` will search for portrait images for each creature
- Output Directory: Where ``hl2mt`` will save the tokens

The filename on the Hero Lab file doesn't matter. It's the creature names that ``hl2mt`` works with. If you have an orcs.por
file with an Orc, Orc Champion and Chief Orc ``hl2mt`` will individually create "Orc", "Orc Champion" and "Chief Orc" tokens
and expect to find image files with those names in the POG and Portrait directories.

Image Files
-----------

A Maptool token has 2 images attached to it. It has a token image(which is called POG in ``hl2mt``) and a portrait image.
``hl2mt`` is designed to work with large batches of tokens so rather than click through and assign proper images to each
creature it attempts to intelligently associate token/portrait images to each creature created in Hero Lab.

Assuming your creature is named Kobold Champion, ``hl2mt`` will try to find images named the following way:

- Kobold?Champion.*
- Kobold.*
- Champion.*
- Kobold*
- Champion*
- Default.*

Note that if your Hero Lab file is in a sub-directory, ``hl2mt`` will first search for images in the same sub-directory
in the image folders. If ``hl2mt`` can't find a file, it'll use a random file in the parent image directory.

What this means is you can create tokens and portraits for basic types(skeleton, human, orc, elf) and create
Hero Lab encounters that reference Orc Champion, Elf Archer, Human Wizard and it'll find the basic type. Later
you could go back and add a POG/Portrait for Orc Champion and re-run ``hl2mt`` and it'll update your Orc Champion
token with the new images.

Also you're able to use sub-directories to further setup good defaults. You can create a Dragons directory and put
in a Default.png image for a generic dragon, and then later put in images for Gold, Red, Blue and so on.

To keep the token sizes down ``hl2mt`` will process any image you have in these directories. For portraits the
image is downsized to be within 200x200 pixels and converted to PNG. For POGs the image is downsized to be within
128x128 pixels and converted to PNG.


Token Properties
----------------

Within Maptool there's a `campaign properties <http://lmwcs.com/rptools/wiki/Introduction_to_Properties>`_ option
which allows you to set properties(variables) onto tokens. By default there's a simple Basic campaign property
that has a few simple settings on it. Most frameworks create their own campaign properties and assign a lot more
values to a token that the framework manipulates via macros.

``hl2mt`` allows you to customize how the Hero Lab data gets converted into token properties. Below are the properties
``hl2mt`` works with:

- Token Property Name: The campaign property name(Basic, Pathfinder, etc)
- Character Name: What property the character name in Hero Lab should be assigned to
- Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma: The numerical stat
- Race, Alignment, Player: Basic character information
- HP Current: The current hit points of the creature(after damage is applied)
- HP Max: The max hit points of the creature
- Speed, Reach: More basic stats
- AC Normal, AC flatfooted, AC touch: Basic defenses
- CMD, CMD Flatfooted: Maneuver defenses
- CMB: The creature's basic CMB
- Melee Attack, Ranged Attack, BAB: Basic attack values

If your framework requires other token properties please let me know and I can add them in.

Token Options
-------------

Not everyone wants all the same things on their tokens, so here you can optionally choose what you want on your
created tokens.

**Multiple Darkvision Ranges**

Basic campaign frameworks typically just have a single Darkvision vision property that's assumed to be 60ft in
range. Pathfinder however has races with different ranges of darkvision. If your framework supports these, you
can click this option and your token will output darkvision in the following way: Darkvision30, Darkvision60,
Darkvision120 and Lowlight, etc.

**Individual Maneuver Macros**

Hero Lab has individual values for all the maneuvers(trip, bull rush, etc). If you'd prefer to see a macro for
each maneuver in addition to the basic CMB macro, click this option. This can be useful if you have creatures
who have bonuses to certain maneuvers.

**Skill Macros**

This option will create a macro for every skill the creature has. These are very simple "d20 + skill" dice rolling
macros.

**Weapon Macros**

Hero Lab contains attack to hit and damage data for every weapon carried by creatures(including natural attacks).
If you'd like a weapon to-hit/damage roll macro created click this option. ``hl2mt`` will attempt to eliminate duplicate
items(if your PCs like to carry 20 daggers) and will also create a Thrown option for any weapon that can also be
thrown.

**Basic Dice Macros**

These are just macros for basic die rolls: d4, d6, d8, d10, d12 and d20

They can be useful if you have newer players who aren't using to typing die rolls into chat.

**Ability Check Macros**

These are d20 dice roll macros that add in the ability check modifier. They can be useful for things like strength
checks.

**Items Macro**

This is a simple list of every item carried by the creature. Unfortunately it's not editable as that requires forms
which would necessitate the use of library tokens.

**HP Change Macro**

This will create a very simple hit point change macro. If your token properties includes both current and max hp
fields then ``hl2mt`` will work with both and create a macro that uses a health bar over your tokens. If you only
have max hp on your framework then ``hl2mt`` will create a simpler macro which only works with that.

Indexing Options
-------------

Hero Lab outputs extremely detailed data on feats, traits, special abilities, spells and so on in the output it
generates for your creatures. This is too much data to store on each token. If your library has 100 spellcasters
all with magic missile it's wasteful to have 100 copies of magic missile described in your campaign. Also some
creatures might have hundreds of feats, special abilities and spells and trying to include very detailed descriptions
for each in a single token would make the token very unwieldy to work with in.

So by default when ``hl2mt`` creates tokens it doesn't include this detailed data. Instead it creates simple lists
on the token of feats, spells and so on, unless you turn on indexing.

Indexing requires the Nerps_ variant of Maptool which allows for the software to pull in data off of remote servers.
When you choose the HTML option for indexing hl2mt will create html pages of all the feats, spells, character
sheets and so on and zip them up into a file you can manually copy to a web server.

Simply choose this option, input the base URL of where you'll unpack the index files and ``hl2mt`` will pack all the html
pages into a zip file you can upload to your server.

As an example, my base URL is http://tarsis.org/maptool/ and when I'm finished running ``hl2mt`` I upload my zip file to
that directory and unpack it. I also make sure the files are world readable by running:

    chmod 644 *

Now in game when I link to a Feat or spell Maptool will fetch the data from that directory instead of trying to
keep it stored internally.

Unlike tables these remote HTML pages are pretty safe from breaking when you re-run ``hl2mt`` and create new tokens. So
you can upload new index zip files and unpack them without hurting existing token links to feats, spells and so on.


License
-------

``hl2mt`` is released under the GPLv3 license.

.. _maptool: http://www.rptools.net/?page=maptool
.. _python: http://www.python.org/
.. _Qt: http://www.riverbankcomputing.com/software/pyqt/download
.. _nerps: https://docs.google.com/file/d/0B2c01YG2XtiJTzA3Z2tEN0lIVk0/edit?usp=sharing