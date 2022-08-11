import sys
import os
import re

# from markdownify import markdownify as md

from markdownify import MarkdownConverter
from markdown import markdown


HELP = """Convert between HTML and Markdown.

Converts HTML files and directories to Markdown or vice versa.

USAGE

Single file
-----------

mdhtml --help
    Prints this message and exits

mdhtml --tomd file
    Converts html file to markdown.

mdhtml --tohtml file
    Converts markdown file to html.

When converting files, the destination file is put next to the
source file, with the source file extension replaced by the proper
destination extension.
If the source file does not have a proper extension,
the destination file name is the source file name with the proper
destination extension appended to it.

-o dst
    Explicit destination file. Can be arbitrary file location.
    If it is an existing directory, the output will be placed in that
    directory.

--keep will prevent overwriting destination files by not executing
       the conversion (a message will be generated then)

Directories
-----------

mdhtml --tomd dir
mdhtml --tohtml dir
    Converts all files with the right extension in dir (recursively) to
    The converted files end up next to their
    corresponding source files.

-o dst
    Explicit destination directory. Can be arbitrary directory location.
    The directory will be cleared before the conversion operation.

--keep has the same meaning as for single files.
"""


CUSTOM_IMG_RE = re.compile(
    r"""
    \b
    (?:
        style | width | height
    )
    =
    (?:
        '[^']
        |
        "[^"]
    )
""",
    re.X | re.S,
)

STRIP_IMG_RE = re.compile(
    r"""
    \s+
    (?:
        style | width | height
    )
    =
    (?:
        ''
        |
        ""
    )
""",
    re.X | re.S,
)


class CustomConverter(MarkdownConverter):
    """Customize the markdown converter.

    Images are not converted to markdown because of their width attributes.
    """

    def convert_img(self, el, text, convert_as_inline):
        elStr = str(el)
        if CUSTOM_IMG_RE.search(elStr):
            return STRIP_IMG_RE.sub("", elStr)
        return super().convert_img(el, text, convert_as_inline)

    def convert_iframe(self, el, *args, **kwargs):
        return str(el)


def md(html, **options):
    return CustomConverter(**options).convert(html)


def dm(mdStr, **options):
    return markdown(mdStr)


MD_OPTIONS = dict(
    heading_style="ATX",
    sub_symbol="~",
    sup_symbol="^",
    wrap=True,
    wrap_width=80,
)


MEDIA_RE = re.compile(
    r"""
    (=['"])
    Media
    /
""",
    re.X | re.S,
)


def clearTree(path):
    """Remove all files from a directory, recursively, but leave subdirs.

    Reason: we want to inspect output in an editor.
    But if we remove the directories, the editor looses its current directory
    all the time.

    Parameters
    ----------
    path:
        The directory in question. A leading `~` will be expanded to the user's
        home directory.
    """

    subdirs = []
    path = os.path.expanduser(path)

    with os.scandir(path) as dh:
        for (i, entry) in enumerate(dh):
            name = entry.name
            if name.startswith("."):
                continue
            if entry.is_file():
                os.remove(f"{path}/{name}")
            elif entry.is_dir():
                subdirs.append(name)

    for subdir in subdirs:
        clearTree(f"{path}/{subdir}")


def tweak(html):
    return MEDIA_RE.sub(r"\1../media/", html)


def convertFile(direction, fileIn, locOut, keep=False):
    """Converts a file in the specified direction.

    Parameters
    ----------
    direction: str
        `tohtml`: from markdown to html;
        `tomd`: from html to md;
    fileIn: str
        Input file
    fileOut: str
        Output file. If the directory for this file does not exist, it will be created.
    keep: boolean, optional False
        If the output file already exists, it will be overwritten if keep is False.
        If it is True, the conversion will be skipped and a message will be generated.

    Returns
    -------
    int
        0 if successfule, else 1
    """

    good = True
    baseIn = os.path.basename(fileIn)
    baseOut = os.path.basename(locOut)
    (srcExt, dstExt) = getExt(direction)
    if fileIn.endswith(srcExt):
        inExtension = srcExt
    else:
        inExtension = ""

    if os.path.exists(locOut):
        if os.path.isdir(locOut):
            baseIn = os.path.basename(locOut)
            fileOut = f"{locOut}/{baseIn.removesuffix(inExtension)}{dstExt}"
        elif os.path.isfile(locOut):
            fileOut = locOut
        else:
            print(f"{locOut} exists and is not a file or directory")
            return 1
        if keep:
            print(f"\t{baseIn:<50} skipped {baseOut:<50} exists")
            return 0
    else:
        dirOut = os.path.dirname(locOut)
        if os.path.exists(dirOut):
            if os.path.isdir(dirOut):
                fileOut = locOut
            elif os.path.isfile(dirOut):
                print(f"{dirOut} exists already as file")
                return 1
            else:
                print(f"{dirOut} exists and is not a file or directory")
                return 1
        else:
            try:
                os.makedirs(dirOut, exist_ok=True)
                fileOut = locOut
            except Exception:
                print(f"Could not create directory {dirOut}")
                return 1

    with open(fileIn, "r") as inh:
        srcStr = inh.read()
    if direction == "tomd":
        srcNew = tweak(srcStr)
        dstStr = md(srcNew, **MD_OPTIONS)
        if srcNew != srcStr:
            with open(fileIn, "w") as outh:
                outh.write(srcNew)
                print(f"\t{baseIn:<50} tweaked")
    elif direction == "tohtml":
        dstStr = dm(srcStr)
    else:
        print(f"Not a valid direction: {direction}")
        return 1

    print(f"\t{baseIn:<50} ==> {baseOut:<50} {len(srcStr):>7} => {len(dstStr):>7}")
    with open(fileOut, "w") as outh:
        outh.write(dstStr)
    return 0 if good else 1


def getExt(direction):
    srcExt = ".md" if direction == "tohtml" else ".html"
    dstExt = ".html" if direction == "tohtml" else ".md"
    return (srcExt, dstExt)


def convertDir(direction, dirIn, dirOut, keep=False):
    """Converts a directory recursively in the specified direction.

    Parameters
    ----------
    direction: str
        `tohtml`: from markdown to html;
        `tomd`: from html to md;
    dirIn: str
        Input directory
    dirOut: str
        Output directory. If it does not exist, it will be created.
        If it exists, it will be emptied.
    keep: boolean, optional False
        If an output file already exists, it will be overwritten if keep is False.
        If it is True, the conversion will be skipped and a message will be generated.

    Returns
    -------
    int
        0 if successfule, else 1
    """
    print(f"{dirIn}")

    if direction not in {"tohtml", "tomd"}:
        print(f"Not a valid direction: {direction}")
        return 1

    good = True

    (srcExt, dstExt) = getExt(direction)

    with os.scandir(dirIn) as it:
        for entry in it:
            name = entry.name
            if name.startswith("."):
                continue
            if entry.is_dir():
                thisGood = convertDir(
                    direction, f"{dirIn}/{name}", f"{dirOut}/{name}", keep=keep
                )
                if thisGood != 0:
                    good = False
            elif entry.is_file():
                if name.endswith(srcExt):
                    thisGood = convertFile(
                        direction,
                        f"{dirIn}/{name}",
                        f"{dirOut}/{name.removesuffix(srcExt)}{dstExt}",
                        keep=keep,
                    )
                    if thisGood != 0:
                        good = False
    return 0 if good else 1


def main():
    args = sys.argv[1:]
    if not args or "--help" in args:
        print(HELP)
        return 0

    direction = None
    keep = False
    seenO = False
    locOut = None
    fileIn = None
    dirIn = None
    srcExt = None
    dstExt = None

    for arg in args:
        if arg == "--keep":
            keep = True
        elif arg in {"--tohtml", "--tomd"}:
            if direction is not None:
                print(HELP)
                print(f"Multiple direction flag: {arg}")
                return -1
            direction = arg[2:]
            (srcExt, dstExt) = getExt(direction)
        elif arg == "-o":
            if seenO:
                print(HELP)
                print("Multiple -o in a row")
                return -1
            else:
                seenO = True
        else:
            if seenO:
                if locOut is None:
                    locOut = arg
                    seenO = False
                else:
                    print(HELP)
                    print(f"Too many output files: {arg}")
                    return -1
            else:
                if fileIn is None and dirIn is None:
                    if not os.path.exists(arg):
                        print(f"{arg} does not exist")
                        return -1

                    if os.path.isdir(arg):
                        dirIn = arg
                    elif os.path.isfile(arg):
                        fileIn = arg
                    else:
                        print(f"{arg} exists but is not a regular file or directory")
                        return -1
                else:
                    print(HELP)
                    print(f"Too many input files/directories: {arg}")
                    return -1

    if direction is None:
        print(HELP)
        print("No conversion direction specified: --tohtml or --tomd")
        return -1
    if fileIn is None and dirIn is None:
        print(HELP)
        print("No input file or directory")
        return -1

    if fileIn is not None:
        if fileIn.endswith(srcExt):
            inExtension = srcExt
        else:
            inExtension = ""

        if locOut is None:
            locOut = f"{fileIn.removesuffix(inExtension)}{dstExt}"

        return convertFile(direction, fileIn, locOut, keep=keep)

    elif dirIn is not None:
        dirIn = os.path.abspath(dirIn)
        if locOut is None:
            locOut = dirIn
        return convertDir(direction, dirIn, locOut, keep=keep)


if __name__ == "__main__":
    main()
