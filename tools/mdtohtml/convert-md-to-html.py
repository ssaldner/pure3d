import markdown

# import sys

# fileIn = sys.argv[1]
# fileOut = sys.argv[2]

with open("file.md", "r") as f:
    text = f.read()
    html = markdown.markdown(text)

with open("file.html", "w") as f:
    f.write(html)
