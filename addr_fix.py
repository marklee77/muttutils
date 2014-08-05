#!/usr/bin/env python
# addr_lookup.py
# Copyright (C) 2013 Mark Lee Stillwell
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

config_file_name = "~/.config/template-render/global_defaults.yaml"


import sqlite3
import sys
from email.header import decode_header
import re

con = None

try:

    con = sqlite3.connect('/home/marklee/.mutt/abook.db')
    cur = con.cursor()
    cur.execute("select name, email from addresses;") 

    for namestr, email in cur.fetchall():

        dnamestr = None
        if namestr:
            try:
                dnamestr = " ".join(unicode(s, c) if c else unicode(s) 
                                 for s, c in decode_header(namestr))
            except UnicodeEncodeError:
                dnamestr = unicode(namestr)

        name = dnamestr
        pcomment = None
        bcomment = None

        if dnamestr:
            m = re.search(r'"([^()\[\]]*).*"', dnamestr)
            if m:
                name = m.group(1) 

            name = re.sub(r'\s*([^,]*[^,\s]),\s*(.*[^\s])\s*', r'\2 \1', name)

        if dnamestr:
            m = re.search(r'".*\((.+)\).*"', dnamestr)
            if m:
                name += " (" + m.group(1) + ")"

        if dnamestr:
            m = re.search(r'".*\[(.+)\].*"', dnamestr)
            if m:
                name += " [" + m.group(1) + "]"

        if name:
            cur.execute("update addresses set name = '" + name + 
                        "' where email = '" + email + "';")
            con.commit()

except sqlite3.Error, e:
    print "Error: %s" % e.args[0]
    sys.exit(1)

finally:

    if con:
        con.close()



