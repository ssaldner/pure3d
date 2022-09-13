import sys
import webbrowser


# browserType = "google-chrome"
browserType = None
browserRep = "default web browser" if browserType is None else browserType


def openWeb(url):
    browser = webbrowser.get(using=browserType)
    browser.open(url, new=2, autoraise=True)


def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"opening {url} in {browserRep} ...")
        openWeb(url)


if __name__ == "__main__":
    main()
else:
    print(__name__)
