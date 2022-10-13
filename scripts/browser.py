import sys
import mywebbrowser


# browserType = "google-chrome"
# browserType = None
# browserRep = "default web browser" if browserType is None else browserType


def openWeb(url):
    # webbrowser.open(url, new=2, autoraise=True)
    browser = mywebbrowser.get(using="chrome")
    browser.open(url, new=2, autoraise=True)


def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
        # print(f"opening {url} in {browserRep} ...")
        print(f"opening {url} in default web browser ...")
        openWeb(url)


if __name__ == "__main__":
    # print(webbrowser.get(using="chrome"))
    main()
else:
    print(__name__)
