#!/usr/bin/env python


############################################################################
#
# MODULE:        i.modis.download
# AUTHOR(S):     Luca Delucchi
# PURPOSE:       i.modis.download is an interface to pyModis for download
#                several tiles of MODIS produts from NASA ftp
#
# COPYRIGHT:     (C) 2011-2021 by Luca Delucchi
#                Fixes by Anika Weinmann, Markus Neteler
#
#                This program is free software under the GNU General Public
#                License (>=v2). Read the file COPYING that comes with GRASS
#                for details.
#
#############################################################################

# %module
# % description: Download single or multiple tiles of MODIS products using pyModis.
# % keyword: raster
# % keyword: import
# % keyword: MODIS
# %end
# %flag
# % key: d
# % description: Debug mode, writing more info into the log file
# %end
# %flag
# % key: g
# % description: Return the name of file containing the list of HDF tiles downloaded in shell script style
# %end
# %flag
# % key: c
# % description: Do not perform GDAL check on downloaded images
# %end
# %flag
# % key: l
# % description: List more info about the supported MODIS products
# %end
# %option G_OPT_F_INPUT
# % key: settings
# % label: Full path to settings file or '-' for standard input, empty for .netrc file
# % required: no
# % guisection: Define
# %end
# %option
# % key: product
# % type: string
# % label: Name of MODIS product(s)
# % multiple: yes
# % required: no
# % options: lst_terra_daily_1000, lst_aqua_daily_1000, lst_terra_eight_1000, lst_aqua_eight_1000, lst_terra_daily_5600, lst_aqua_daily_5600, lst_terra_monthly_5600, lst_aqua_monthly_5600, ndvi_terra_sixteen_250, ndvi_aqua_sixteen_250, ndvi_terra_sixteen_500, ndvi_aqua_sixteen_500, ndvi_terra_sixteen_1000, ndvi_aqua_sixteen_1000, ndvi_terra_sixteen_5600, ndvi_aqua_sixteen_5600, ndvi_terra_monthly_1000, ndvi_aqua_monthly_1000, ndvi_terra_monthly_5600, ndvi_aqua_monthly_5600, snow_terra_daily_500, snow_aqua_daily_500, snow_terra_eight_500, snow_aqua_eight_500, surfreflec_terra_daily_500, surfreflec_aqua_daily_500, surfreflec_terra_eight_500, surfreflec_aqua_eight_500, water_terra_250, aerosol_terra_aqua_daily_1000
# % answer: lst_terra_daily_1000
# %end
# %option
# % key: tiles
# % type: string
# % label: The name(s) of tile(s) to download (comma separated). If not set, all available tiles are downloaded
# % description: e.g.: h18v04
# % required: no
# %end
# %option
# % key: startday
# % type: string
# % label: First date to download
# % description: Format: YYYY-MM-DD. If not set the download starts from current date and goes back 10 days. If not endday is set, the download stops 10 days after the startday
# % required: no
# %end
# %option
# % key: endday
# % type: string
# % label: Last date to download
# % description: Format: YYYY-MM-DD. To use only with startday
# % required: no
# %end
# %option
# % key: folder
# % type: string
# % label: Folder to store the downloaded data
# % description: If not set, path to settings file is used
# % required: no
# %end


# import library
import os
import sys
from datetime import *
import grass.script as gs
from grass.pygrass.utils import get_lib_path


path = get_lib_path(modname="i.modis", libname="libmodis")
if path is None:
    gs.fatal("Not able to find the modis library directory.")
sys.path.append(path)


def check_folder(folder):
    """Check if a folder it is writable by the user that launch the process"""
    if not os.path.exists(folder) or not os.path.isdir(folder):
        gs.fatal(_("Folder <{}> does not exist").format(folder))

    if not os.access(folder, os.W_OK):
        gs.fatal(_("Folder <{}> is not writeable").format(folder))

    return True


def checkdate(options):
    """Function to check the data and return the correct value to download the
    the tiles
    """

    def check2day(second, first=None):
        """Function to check two date"""
        if not first:
            valueDay = None
            firstDay = date.today()
        else:
            valueDay = first
            firstSplit = first.split("-")
            firstDay = date(int(firstSplit[0]), int(firstSplit[1]), int(firstSplit[2]))
        lastSplit = second.split("-")
        lastDay = date(int(lastSplit[0]), int(lastSplit[1]), int(lastSplit[2]))
        if firstDay < lastDay:
            gs.fatal(_("End day has to be bigger then start day"))
        delta = firstDay - lastDay
        valueDelta = int(delta.days)
        return valueDay, second, valueDelta

    # no set start and end day
    if options["startday"] == "" and options["endday"] == "":
        return None, None, 10
    # set only end day
    elif options["startday"] != "" and options["endday"] == "":
        valueDelta = 10
        valueEnd = options["startday"]
        firstSplit = valueEnd.split("-")
        firstDay = date(int(firstSplit[0]), int(firstSplit[1]), int(firstSplit[2]))
        delta = timedelta(10)
        lastday = firstDay + delta
        valueDay = lastday.strftime("%Y-%m-%d")
    # set only start day
    elif options["startday"] == "" and options["endday"] != "":
        gs.fatal(
            _("It is not possible to use <endday> option without <startday> option")
        )
    # set start and end day
    elif options["startday"] != "" and options["endday"] != "":
        valueDay, valueEnd, valueDelta = check2day(
            options["startday"], options["endday"]
        )
    return valueDay, valueEnd, valueDelta


# main function
def main():
    try:
        from rmodislib import product
    except:
        gs.fatal("i.modis library is not installed")
    try:
        from pymodis.downmodis import downModis
    except:
        gs.fatal("pymodis library is not installed")
    # check if you are in GRASS
    gisbase = os.getenv("GISBASE")
    if not gisbase:
        gs.fatal(_("$GISBASE not defined"))
        return 0
    if flags["l"]:
        prod = product()
        prod.print_prods()
        return 0
    # empty settings and folder would collide
    if not options["settings"] and not options["folder"]:
        gs.fatal(
            _(
                "With empty settings parameter (to use the .netrc file) "
                "the folder parameter needs to be specified"
            )
        )
    # set username, password and folder if settings are insert by stdin
    if not options["settings"]:
        user = None
        passwd = None
        if check_folder(options["folder"]):
            fold = options["folder"]
        else:
            gs.fatal(
                _(
                    "Set folder parameter when using stdin for passing "
                    "the username and password"
                )
            )
    elif options["settings"] == "-":
        if options["folder"] != "":
            import getpass

            if check_folder(options["folder"]):
                fold = options["folder"]
            user = input(_("Insert username: "))
            passwd = getpass.getpass(_("Insert password: "))
        else:
            gs.fatal(
                _(
                    "Set folder parameter when using stdin for passing "
                    "the username and password"
                )
            )
    # set username, password and folder by file
    else:
        if not os.path.isfile(options["settings"]):
            gs.fatal(
                _("The settings parameter <{}> is not a file").format(
                    options["settings"]
                )
            )
        # open the file and read the the user and password:
        # first line is username
        # second line is password
        try:
            with open(options["settings"], "r") as filesett:
                fileread = filesett.readlines()
                user = fileread[0].strip()
                passwd = fileread[1].strip()
        except (FileNotFoundError, PermissionError) as e:
            gs.fatal(_("Unable to read settings: {}").format(e))
        if options["folder"] != "":
            if check_folder(options["folder"]):
                fold = options["folder"]
        # set the folder from path where settings file is stored
        else:
            path = os.path.split(options["settings"])[0]
            temp = os.path.split(gs.tempfile())[0]
            if temp in path:
                gs.warning(
                    _(
                        "You are downloading data into a temporary "
                        "directory. They will be deleted when you "
                        "close this GRASS GIS session"
                    )
                )
            if check_folder(path):
                fold = path
    # the product
    products = options["product"].split(",")
    # first date and delta
    firstday, finalday, delta = checkdate(options)
    # set tiles
    if options["tiles"] == "":
        tiles = None
        gs.warning(
            _("Option 'tiles' not set. Downloading all available tiles to <{}>").format(
                fold
            )
        )
    else:
        tiles = options["tiles"]
    # set the debug
    if flags["d"]:
        debug_opt = True
    else:
        debug_opt = False
    if flags["c"]:
        checkgdal = False
    else:
        checkgdal = True
    for produ in products:
        prod = product(produ).returned()
        # start modis class
        modisOgg = downModis(
            url=prod["url"],
            user=user,
            password=passwd,
            destinationFolder=fold,
            tiles=tiles,
            delta=delta,
            path=prod["folder"],
            product=prod["prod"],
            today=firstday,
            enddate=finalday,
            debug=debug_opt,
            checkgdal=checkgdal,
        )
        # connect to ftp
        modisOgg.connect()
        if modisOgg.nconnection <= 20:
            # download tha tiles
            gs.message(
                _("Downloading MODIS product <{}> ({})...").format(produ, prod["prod"])
            )
            modisOgg.downloadsAllDay()
            filesize = int(os.path.getsize(modisOgg.filelist.name))
            if flags["g"] and filesize != 0:
                gs.message("files=%s" % modisOgg.filelist.name)
            elif filesize == 0:
                gs.message(
                    _("No data download, probably they have been previously downloaded")
                )
            elif filesize != 0:
                gs.message(
                    _(
                        "All data have been downloaded, continue "
                        "with i.modis.import with the option 'files=%s'"
                    )
                    % modisOgg.filelist.name
                )
        else:
            gs.fatal(_("Error during connection"))


if __name__ == "__main__":
    options, flags = gs.parser()
    sys.exit(main())
