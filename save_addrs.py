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

def format_name(namein):
    from email.header import decode_header
    import re

    if not namein:
        return None

    nameout = None

    try:
        nameout = " ".join(unicode(s, c) if c else unicode(s) 
                           for s, c in decode_header(namein))
    except UnicodeEncodeError:
        nameout = unicode(namein)

    m = re.search(r'"([^()\[\]]*).*"', nameout)
    if m:
        nameout = m.group(1) 

    nameout = re.sub(r'\s*([^,]*[^,\s]),\s*(.*[^\s])\s*', r'\2 \1', nameout)

    m = re.search(r'".*\((.+)\).*"', namein)
    if m:
        nameout += " (" + m.group(1) + ")"

    m = re.search(r'".*\[(.+)\].*"', namein)
    if m:
        nameout += " [" + m.group(1) + "]"

    return nameout


def main(argv=None):
    from argparse import ArgumentParser
    from email.parser import Parser
    from email.utils import getaddresses
    from os.path import expanduser, isfile
    from sqlite3 import connect
    import sqlite3
    from sys import stdin

    argparser = ArgumentParser(description="Render a file using templates.")
    argparser.add_argument('-b', '--dbfile', default='~/.mutt/abook.db', 
                           help='database file')

    args = argparser.parse_args()

    database_file = expanduser(args.dbfile)

    if not isfile(database_file):
        raise SystemExit("ERROR: no such file '%s'!" % args.dbfile)

    msgparser = Parser()
    msg = msgparser.parse(stdin, True)
    froms = msg.get_all('from', []) 
    tos = msg.get_all('to', []) 
    ccs = msg.get_all('cc', []) 
    bccs = msg.get_all('bcc', [])

    try:
        con = connect(database_file)
        cur = con.cursor()

        for prename, email in getaddresses(froms + tos + ccs + bccs):

            name = format_name(prename)
            print name
            cur.execute("select name from addresses where email = '" + email + "';")
            row = cur.fetchone();

            if not row:
                if name and len(name) > 0:
                    cur.execute("insert into addresses (name, email, created, modified) values ('" + name + "', '" + email + "', datetime('now'), datetime('now'));")
                else:
                    cur.execute("insert into addresses (email, created, modified) values ('" + email + "', datetime('now'), datetime('now'));")
            elif name and len(name) > 0:
                cur.execute("update addresses set name = '" + name + "', modified = datetime('now') where email = '" + email +"';")

        con.commit()
    except sqlite3.Error, e:
        raise SystemExit("ERROR: %s" % e.args[0])

    finally:
        if con:
            con.close()

if __name__ == "__main__":
    main()
