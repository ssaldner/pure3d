import sys
import webbrowser


def openWeb(url):
    webbrowser.open(url, new=2, autoraise=True)


def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"opening {url} in default web browser ...")
        openWeb(url)


if __name__ == "__main__":
    main()
else:
    print(__name__)
