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

con = None

try:
    pattern = sys.argv[1];

    con = sqlite3.connect('/home/marklee/.mutt/abook.db')
    cur = con.cursor()
    cur.execute("select name, email from addresses where nick like '%" + 
                pattern + "%' or email like '%" + pattern +
                "%' or name like '%" + pattern + "%';")

    print sys.stdout.encoding
    for name, email in cur.fetchall():
        print name, email

except sqlite3.Error, e:
    print "Error: %s" % e.args[0]
    sys.exit(1)

finally:

    if con:
        con.close()
