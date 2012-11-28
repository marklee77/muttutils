#!/usr/bin/python
import vobject
from argparse import ArgumentParser
from os.path import isfile
from sys import stdin, stdout

parser = ArgumentParser(description="Generate a replay to an iCal Invitation.")
parser.add_argument('-e', '--email', help='attendee email') 
parser.add_argument('-i', '--invite', default='-', 
                    help='invitation .ics file or - (for stdin)')
parser.add_argument('-o', '--output', default='-',
                    help='output file or - (for stdout)')
parser.add_argument('-f', '--format', choices=['ics', 'email'], default='ics', 
                    help='output format')
parser.add_argument('-r', '--response', 
                    choices=['accepted', 'declined', 'tentative'],
                    default='accepted', help='invitation response')

args = parser.parse_args()

if not args.email:
    raise SystemExit("error: can't send response without attendee email!")

mailto = "mailto:" + args.email.lower()

infile = None
if args.invite == "-":
    infile = stdin
elif isfile(args.invite):
    infile = open(args.invite, 'r')
else:
    raise SystemExit("must specify valid invitation file or stdin")

outfile = None
if args.output == "-":
    outfile = stdout
elif isfile(args.output):
    outfile = open(args.output, 'w')
else:
    raise SystemExit("must specify valid output file or stdout")

invite = vobject.readOne(infile.read())

invite.method.value = u'REPLY'
for vevent in invite.vevent_list:
    while vevent.attendee_list and \
            vevent.attendee_list[0].value.lower() != mailto:
        del vevent.attendee_list[0]
    while len(vevent.attendee_list) > 1:
        del vevent.attendee_list[1]
    if vevent.attendee:
        vevent.attendee.params[u'PARTSTAT'][0] = u'ACCEPTED'
        del vevent.attendee.params[u'RSVP']
    else:
        raise SystemExit("attendee email not found")

outfile.write(invite.serialize())
outfile.close()
