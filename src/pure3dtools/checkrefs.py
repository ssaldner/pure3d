"""
# Check references in articles

All href and src references in articles will be checked.
Only html files are being searched.

They will be listed as

* online references
* local refererences resolvable in the media folder
* unresolvable references

Identical references are grouped, and its occurrences indicated.
"""


import sys
import os
import re
import collections


HELP = """
USAGE
checkrefs --help
checkrefs indir

EFFECT

If --help is present, prints this text and exits.

indir is the input directory, usually an articles directory

The report will be written to stdout.
"""


OUTFILE_DEFAULT = "refs.txt"


REF_RE = re.compile(
    r"""
    \b(src|href)
    =
    ['"]
    ([^'"]*)
    ['"]
    """,
    re.X | re.I,
)

ONLINE_RE = re.compile(r"""^https?://""", re.I)


def checkLinks(inDir, refs):
    links = collections.defaultdict(
        lambda: collections.defaultdict(lambda: collections.defaultdict(list))
    )

    for (fileName, ln, kind, url) in refs:
        status = None if ONLINE_RE.match(url) else os.path.exists(f"{inDir}/{url}")
        links[status][url][fileName].append(ln)

    printLinks(links)
    return 1 if False in links else 2 if None in links else 0


def printLinks(links):
    for (status, linkData) in sorted(links.items()):
        statusRep = "online" if status is None else "resolved" if status else "missing"
        print(statusRep)
        for (url, locData) in sorted(linkData.items()):
            if len(locData) == 1:
            print


def checkRef(inDir, fileName):
    path = f"{inDir}/{fileName}"

    results = []

    with open(path) as fh:
        for (i, line) in enumerate(fh):
            for (kind, url) in REF_RE.findall(line):
                results.append((fileName, i, kind, url))

    return results


def checkRefs(inDir):
    results = []

    with os.scandir(inDir) as dh:
        for entry in dh:
            fileName = entry.name
            if entry.is_file() and fileName.lower().endswith(".html"):
                results.extend(checkRef(inDir, fileName))

    return checkLinks(results)


def main():
    args = sys.argv[1:]
    if not args or "--help" in args:
        print(HELP)
        return 0

    inDir = None

    for arg in args:
        if inDir is None:
            inDir = arg
        else:
            print(HELP)
            print(f"Too many input directories: {arg}")
            return -1

    if inDir is None:
        print(HELP)
        print("No input file")
        return -1

    if not os.path.exists(inDir):
        print("Input directory does not exist: {inDir}")
        return -1

    return checkRefs(inDir)


if __name__ == "__main__":
    main()
