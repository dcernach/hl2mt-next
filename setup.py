__version__ = '0.85rc1'
__zipfile__ = 'hl2mt-next-%s.zip' % __version__
# http://cx-freeze.readthedocs.org/en/latest/overview.html
# http://stackoverflow.com/questions/15486292/cx-freeze-doesnt-find-all-dependencies
# build with: C:\> python setup.py  build

import sys
import shutil
import zipfile
import os

from cx_Freeze import setup, Executable

# Remove the existing folders folder

shutil.rmtree("dist", ignore_errors=True)
shutil.rmtree("dist.temp", ignore_errors=True)
shutil.rmtree("build", ignore_errors=True)

# Define Plataform infromation
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

########################################
# List of the Executable options
########################################

# "script":               # the name of the file containing the script which is to be frozen
# "initScript":           # the name of the initialization script that will be executed before the actual script is
#                           executed; this script is used to set up the environment for the executable; if a name is
#                           given without an absolute path the names of files in the initscripts subdirectory of the
#                           cx_Freeze package is searched
#
# "base":                 # the name of the base executable; if a name is given without an absolute path the names of
#                           files in the bases subdirectory of the cx_Freeze package is searched
#
# "path":                 # list of paths to search for modules
# "targetDir":            # the directory in which to place the target executable and any dependent files
# "targetName":           # the name of the target executable; the default value is the name of the script with the
#                           extension exchanged with the extension for the base executable

# "includes":             # list of names of modules to include
# "excludes":             # list of names of modules to exclude
# "packages":             # list of names of packages to include, including all of the package's submodules
# "replacePaths":         # Modify filenames attached to code objects, which appear in tracebacks. Pass a list of
#                           2-tuples containing paths to search for and corresponding replacement values. A search
#                           for '*' will match the directory containing the entire package, leaving just the relative
#                           path to the module.
#
# "compress":             # boolean value indicating if the module bytecode should be compressed or not
# "copyDependentFiles":   # boolean value indicating if dependent files should be copied to the target directory or not
# "appendScriptToExe":    # boolean value indicating if the script module should be appended to the executable itself
# "appendScriptToLibrary":# boolean value indicating if the script module should be appended to the shared library
#                           zipfile
# "icon":                 # name of icon which should be included in the executable itself on Windows or placed in the
#                           target directory for other platforms
# "namespacePackages":    # list of packages to be treated as namespace packages (path is extended using pkgutil)
# "shortcutName":         # the name to give a shortcut for the executable when included in an MSI package
# "shortcutDir":          # the directory in which to place the shortcut when being installed by an MSI package; see
#                           the MSI Shortcut table documentation for more information on what values can be placed here.
########################################

executables = [
    Executable(
        # what to build
        script="hl2mt.py",
        initScript=None,
        base=base,
        targetDir=r"dist",
        targetName="hl2mt.exe",
        compress=True,
        copyDependentFiles=True,
        appendScriptToExe=False,
        appendScriptToLibrary=False,
        icon=None)
]

########################################
# Here is a list of the build_exe options
########################################
# 1) append the script module to the executable
append_script_to_exe = False

# 2) the name of the base executable to use which, if given as a relative path, will be joined with the bases
# subdirectory of the cx_Freeze installation; the default value is "Console"
base = base  # "Console"

# 3) list of names of files to exclude when determining dependencies of binary files that would normally be included;
# note that version numbers that normally follow the shared object extension are stripped prior to performing the
# comparison
bin_excludes = []

# 4) list of names of files to include when determining dependencies of binary files that would normally be excluded;
# note that version numbers that normally follow the shared object extension are stripped prior to performing the
# comparison
bin_includes = []

# 5) list of paths from which to exclude files when determining dependencies of binary files
bin_path_excludes = []

# 6) list of paths from which to include files when determining dependencies of binary files
bin_path_includes = []

# 7) directory for built executables and dependent files, defaults to build/
build_exe = "dist/"

# 8) create a compressed zip file
compressed = False

# 9) comma separated list of constant values to include in the constants module called BUILD_CONSTANTS in
# form <name>=<value>
constants = []

# 10) copy all dependent files
copy_dependent_files = True

# 11) create a shared zip file called library.zip which will contain all modules shared by all executables which are
# built
create_shared_zip = True

# 12) comma separated list of names of modules to exclude (sample)
excludes = []

# 13) include the icon in the frozen executables on the Windows platform and alongside the frozen executable on other
# platforms
icon = False

# 14) comma separated list of names of modules to include (sample)
includes = []

# 15) list containing files to be copied to the target directory;
#  it is expected that this list will contain strings or 2-tuples for the source and destination;
#  the source can be a file or a directory (in which case the tree is copied except for .svn and CVS directories);
#  the target must not be an absolute path
#
# NOTE: INCLUDE FILES MUST BE OF THIS FORM OTHERWISE freezer.py line 128 WILL TRY AND DELETE dist/. AND FAIL!!!
# Here is a list of ALL the DLLs that are included in Python27\Scripts
# #include_files = [(r"C:\Python27\Scripts\mk2ifcoremd.dll", "mk2ifcoremd.dll")]


# 16) include the script module in the shared zip file
include_in_shared_zip = True

# 17) include the Microsoft Visual C runtime DLLs and (if necessary) the manifest file required to run the executable
# without needing the redistributable package installed
include_msvcr = False

# 18) the name of the script to use during initialization which, if given as a relative path, will be joined with the
# initscripts subdirectory of the cx_Freeze installation; the default value is "Console"
init_script = ""

# 19) comma separated list of packages to be treated as namespace packages (path is extended using pkgutil)
namespace_packages = []

# 20) optimization level, one of 0 (disabled), 1 or 2
optimize = 0

# 21) comma separated list of packages to include, which includes all submodules in the package
packages = []

# 22) comma separated list of paths to search; the default value is sys.path
path = []

# 23) Modify filenames attached to code objects, which appear in tracebacks. Pass a comma separated list of paths in
# the form <search>=<replace>. The value * in the search portion will match the directory containing the entire
# package, leaving just the relative path to the module.
replace_paths = []

# 24) Suppress all output except warnings (True/False)
silent = True

# 25) list containing files to be included in the zip file directory; it is expected that this list will contain
# strings or 2-tuples for the source and destination
zip_includes = []

options = {"build_exe": {
    # "append_script_to_exe":   append_script_to_exe,
    # "base":                   base,
    # "bin_excludes":           bin_excludes,
    # "bin_includes":           bin_includes,
    # "bin_path_excludes":      bin_path_excludes,
    # "bin_path_includes":      bin_path_includes,
    "build_exe": build_exe,
    "compressed": compressed,
    # "constants":              constants,
    "copy_dependent_files": copy_dependent_files,
    # "create_shared_zip":      create_shared_zip,
    "excludes": excludes,
    # "icon":                   icon,
    "includes": includes,
    # "include_files":          include_files,
    # "include_in_shared_zip":  include_in_shared_zip,
    # "include_msvcr":          include_msvcr,
    # "init_script":            init_script,
    # "namespace_packages":     namespace_packages,
    # "optimize":               optimize,
    "packages": packages,
    "path": path,
    # "replace_paths":          replace_paths,
    # "silent"                  : silent,
    # "zip_includes":           zip_includes,
}}

setup(
    name='hl2mt',
    version='0.85rc',
    url='https://bitbucket.org/dcernach/hl2mt',
    license='GPLv3',
    description='hl2mt: Hero Lab to Maptool fork',
    author='Dalton Andrade',
    author_email='',

    packages=['ui', 'macros', 'templates'],
    options=options,
    executables=executables
)


def zipdir(path, file):
    os.chdir(path)
    path = '.'
    zf = zipfile.ZipFile(os.path.join(path, file), "w", zipfile.ZIP_DEFLATED)

    for dirname, subdirs, files in os.walk(path):
        print('Compressing Dir  -> ' + dirname)

        for filename in files:
            print('Compressing File -> ' + os.path.join(dirname, filename))
            if (filename != file):
                zf.write(os.path.join(dirname, filename))

        if (dirname != '.'):
            zf.write(dirname)

    zf.close()
    os.chdir('..')


print('Cleaning up...')
shutil.rmtree("build", ignore_errors=True)

print('Compressing files...')
zipdir('dist', __zipfile__)

print('Done...')
shutil.move(os.path.join('dist', __zipfile__), __zipfile__)
os.rename('dist', 'dist.temp')
os.makedirs('dist', exist_ok=True)
shutil.rmtree('dist.temp', ignore_errors=True)
shutil.move(__zipfile__, os.path.join('dist', __zipfile__))
