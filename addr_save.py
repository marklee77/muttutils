#!/usr/bin/env python
# addr_save.py
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

database_file = "~/.mutt/abook.db"



con = None

try:
    name = sys.argv[1];
    email = sys.argv[2];

    con = sqlite3.connect('/home/marklee/.mutt/abook.db')
    cur = con.cursor()
    cur.execute("insert into addresses (name, email) values ('" + name + "', '"
                + email + "');")
    con.commit()

except sqlite3.Error, e:
    print "Error: %s" % e.args[0]
    sys.exit(1)

finally:

    if con:
        con.close()

def main(argv=None):
    from argparse import ArgumentParser
    from os.path import abspath
    from sys import argv
    from sqlite3 import connect

    parser = ArgumentParser(description="Filter Email")
    parser.add_argument('-i', '--inputfile', help='input file')
    parser.add_argument('-e', '--engine', help='templating engine')
    parser.add_argument('-d', '--template_dirs',
                        help=': delimited template search path')
    parser.add_argument('-t', '--template',
                        help='template to apply to input file')
    parser.add_argument('-b', '--block', help='template block to override')
    parser.add_argument('-m', '--metafile', action='append',
                        help='metadata file in yaml format')
    parser.add_argument('-v', '--var', action='append', default=[],
                        help='name=value pairs to be added to metadata')
    parser.add_argument('-o', '--outputfile', default='-', help='output file')
    parser.add_argument('-ienc', '--input_encoding', help='input encoding')
    parser.add_argument('-oenc', '--output_encoding', help='output encoding')

    args = parser.parse_args()

if __name__ == "__main__":
    main()
 
