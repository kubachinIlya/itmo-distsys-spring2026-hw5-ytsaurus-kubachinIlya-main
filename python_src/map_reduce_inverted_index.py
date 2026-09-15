#!/usr/bin/python

import re
import sys
import operator
import itertools

def do_decode(iterable):
    for line in iterable:
        row = line.rstrip("\r\n").split("\t")
        row = dict(map(lambda x: x.split("=", 1), row))
        yield row

def do_encode(iterable):
    for row in iterable:
        yield "\t".join("{0}={1}".format(*item) for item in row.items())

def do_map(iterable):
    for row in iterable:
        lineno = int(row["lineno"])
        text = row["text"].lower()
        for word in re.findall(r"\w+", text, re.U):
            yield {"word": word, "lineno": lineno}

def do_reduce(iterable):
    for key, group in itertools.groupby(iterable, operator.itemgetter("word")):
        lines = sorted(set(int(row["lineno"]) for row in group))
        yield {"word": key, "lines": ",".join(str(l) for l in lines)}

def do_print(iterable):
    for line in iterable:
        sys.stdout.write(line)
        sys.stdout.write("\n")

if __name__ == "__main__":
    wf = sys.stdin
    wf = do_decode(wf)

    if len(sys.argv) >= 2 and sys.argv[1] == "map":
        wf = do_map(wf)
    elif len(sys.argv) >= 2 and sys.argv[1] == "reduce":
        wf = do_reduce(wf)
    else:
        print("Please, specify either 'map' or 'reduce' as the first argument", file=sys.stderr)
        sys.exit(1)

    wf = do_encode(wf)
    wf = do_print(wf)