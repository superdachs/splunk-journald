#!/usr/bin/env python3

from systemd import journal

r = journal.Reader()

try:
    with open('last_entry', 'r') as f:
        last_entry = f.readline(1)
except:
    last_entry = None

r.seek_tail()

while r.get_next():
    for e in r:
        print(e['MESSAGE'])
        last_entry = e['MESSAGE']

with open("last_entry", "w") as f:
    f.write(last_entry)