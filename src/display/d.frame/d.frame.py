#!/usr/bin/env python

############################################################################
#
# MODULE:       d.frame
# AUTHOR(S):    Martin Landa <landa.martin gmail.com>
#               Based on d.frame from GRASS 6
# PURPOSE:      Manages display frames on the user's graphics monitor
# COPYRIGHT:    (C) 2014 by Martin Landa, and the GRASS Development Team
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
############################################################################
# %module
# % description: Manages display frames on the user's graphics monitor.
# % keyword: display
# % keyword: graphics
# % keyword: monitors
# % keyword: frame
# % overwrite: yes
# %end
# %flag
# % key: c
# % description: Create a new frame if doesn't exist and select
# %end
# %flag
# % key: e
# % description: Remove all frames, erase the screen and exit
# % suppress_required: yes
# %end
# %flag
# % key: p
# % description: Print name of current frame and exit
# % suppress_required: yes
# %end
# %flag
# % key: a
# % description: Print names of all frames including 'at' position and exit
# % suppress_required: yes
# %end
# %option
# % key: frame
# % type: string
# % required: yes
# % multiple: no
# % key_desc: name
# % description: Frame to be selected or created (if -c flag is given)
# %end
# %option
# % key: at
# % type: double
# % required: no
# % multiple: no
# % key_desc: bottom,top,left,right
# % label: Screen coordinates in percent where to place the frame (0,0 is lower-left)
# % options: 0-100
# % description: Implies only when -c or --overwrite flag is given
# %end

import os
import sys

from grass.script.core import (
    parser,
    read_command,
    fatal,
    debug,
    run_command,
    gisenv,
    warning,
)


# check if monitor is running
def check_monitor():
    return read_command("d.mon", flags="p", quiet=True).strip()


# read monitor file and return list of lines
def read_monitor_file(monitor, ftype="env"):
    mfile = check_monitor_file(monitor, ftype)
    try:
        fd = open(mfile, "r")
    except OSError as e:
        fatal(_("Unable to get monitor info. %s"), e)

    lines = []
    for line in fd.readlines():
        lines.append(line)

    fd.close()

    return lines


# check if monitor file exists
def check_monitor_file(monitor, ftype="env"):
    var = "MONITOR_%s_%sFILE" % (monitor.upper(), ftype.upper())
    mfile = gisenv().get(var, None)
    if mfile is None or not os.path.isfile(mfile):
        fatal(_("Unable to get monitor info (no %s found)") % var)

    return mfile


# write new monitor file
def write_monitor_file(monitor, lines, ftype="env"):
    mfile = check_monitor_file(monitor, ftype)

    try:
        fd = open(mfile, "w")
    except OSError as e:
        fatal(_("Unable to get monitor info. %s"), e)

    fd.writelines(lines)
    fd.close()


# remove all frames and erase screen
def erase(monitor):
    # remove frames
    lines = []
    for line in read_monitor_file(monitor):
        if "FRAME" not in line:
            lines.append(line)

    write_monitor_file(monitor, lines)

    # erase screen
    run_command("d.erase")


# find frame for given monitor
def find_frame(monitor, frame):
    for line in read_monitor_file(monitor):
        if "FRAME" in line:
            if get_frame_name(line) == frame:
                return True

    return False


# print frames name(s) to stdout
def print_frames(monitor, current_only=False, full=False):
    for line in read_monitor_file(monitor):
        if "FRAME" not in line:
            continue
        if current_only and line.startswith("#"):
            continue
        sys.stdout.write(get_frame_name(line))
        if full:
            sys.stdout.write(":" + line.split("=", 1)[1].rsplit("#", 1)[0])
        sys.stdout.write("\n")


# get frame name from line
def get_frame_name(line):
    return line.rstrip("\n").rsplit("#", 1)[1].strip(" ")


# calculate position of the frame in percent
def calculate_frame(frame, at, width, height):
    try:
        b, t, l, r = map(float, at.split(","))
    except:
        fatal(_("Invalid frame position: %s") % at)

    top = height - (t / 100.0 * height)
    bottom = height - (b / 100.0 * height)
    left = l / 100.0 * width
    right = r / 100.0 * width

    return "GRASS_RENDER_FRAME=%d,%d,%d,%d # %s%s" % (
        top,
        bottom,
        left,
        right,
        frame,
        "\n",
    )


# create new frame
def create_frame(monitor, frame, at, overwrite=False):
    lines = read_monitor_file(monitor)
    # get width and height of the monitor
    width = height = -1
    for line in lines:
        try:
            if "WIDTH" in line:
                width = int(line.split("=", 1)[1].rsplit(" ", 1)[0])
            elif "HEIGHT" in line:
                height = int(line.split("=", 1)[1].rsplit(" ", 1)[0])
        except:
            pass

    if width < 0 or height < 0:
        fatal(_("Invalid monitor size: %dx%d") % (width, height))

    if not overwrite:
        lines.append(calculate_frame(frame, at, width, height))
    else:
        for idx in range(len(lines)):
            line = lines[idx]
            if "FRAME" not in line:
                continue
            if get_frame_name(line) == frame:
                lines[idx] = calculate_frame(frame, at, width, height)

    write_monitor_file(monitor, lines)


# select existing frame
def select_frame(monitor, frame):
    lines = read_monitor_file(monitor)
    for idx in range(len(lines)):
        line = lines[idx]
        if "FRAME" not in line:
            continue
        if get_frame_name(line) == frame:
            if line.startswith("#"):
                lines[idx] = line.lstrip("# ")  # un-comment line
        elif not line.startswith("#"):
            lines[idx] = "# " + line  # comment-line

    write_monitor_file(monitor, lines)


def main():
    # get currently selected monitor
    monitor = check_monitor()
    if not monitor:
        fatal(_("No graphics device selected. Use d.mon to select graphics device."))
    if monitor not in ("png", "cairo"):
        fatal(_("Only Cairo or PNG monitors are currently supported"))

    if flags["e"]:
        # remove frames and erase monitor and exit
        erase(monitor)
        return

    if flags["p"]:
        # print current frame and exit
        print_frames(monitor, current_only=True)
        return

    if flags["a"]:
        # print all frames including their position and exit
        print_frames(monitor, current_only=False, full=True)
        return

    found = find_frame(monitor, options["frame"])
    if not found:
        if not flags["c"]:
            fatal(
                _(
                    "Frame <%s> doesn't exist, exiting. "
                    "To create a new frame use '-c' flag."
                )
                % options["frame"]
            )
        else:
            if not options["at"]:
                fatal(_("Required parameter <%s> not set") % "at")
            # create new frame if not exists
            create_frame(monitor, options["frame"], options["at"])
    else:
        if os.getenv("GRASS_OVERWRITE", "0") == "1":
            warning(
                _("Frame <%s> already exists and will be overwritten")
                % options["frame"]
            )
            create_frame(monitor, options["frame"], options["at"], overwrite=True)
        else:
            if options["at"]:
                warning(
                    _(
                        "Frame <%s> already found. An existing frame can be overwritten by '%s' flag."
                    )
                    % (options["frame"], "--overwrite")
                )

    # select givenframe
    select_frame(monitor, options["frame"])


if __name__ == "__main__":
    options, flags = parser()
    sys.exit(main())
