#!/usr/bin/env python3
import os
import subprocess
import sys

def find_targets(targets):
    if len(targets) == 0:
        targets.append(os.getcwd())
    file_targets = []
    for target in targets:
        if os.path.isfile(target):
            file_targets.append(target)
        elif os.path.isdir(target):
            for root, dirs, files in os.walk(target):
                for f in files:
                    file_targets.append(os.path.join(root, f))
    return file_targets

colors = {
    "U": "\033[91m", # red
    "t": "\033[93m", # yellow
    "T": "\033[92m", # green
    "none": "\033[0m", # reset
}

def parse_nm_output(grep_stdout, target):
    line = grep_stdout.readline().decode('utf-8').strip()
    toks = line.split()
    ty = "U" if toks[0] == "U" else toks[1]
    color = colors.get(ty, colors["none"])
    print("%s%s %s" % (color, ty, target))

def nm(needle, haystack):
    print("found %s in:" % needle)
    with open(os.devnull, 'w') as devnull:
        for target in haystack:
            nm = subprocess.Popen(('nm', target),
                    stdout=subprocess.PIPE, stderr=devnull)
            filt = subprocess.Popen(('c++filt'), stdin=nm.stdout,
                    stdout=subprocess.PIPE)
            grep = subprocess.Popen(('grep', needle), stdin=filt.stdout,
                    stdout=subprocess.PIPE)
            grep.wait()
            if grep.returncode == 0:
                parse_nm_output(grep.stdout, target)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage = "Usage: ./find_symbol.py <symbol> [directories/files]"
        print(usage, file=sys.stderr)
    else:
        symbol = sys.argv[1]
        nm(symbol, find_targets(sys.argv[2:]))
