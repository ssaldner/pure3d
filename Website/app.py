from flask import Flask, render_template  # for flask
import os

# create and configure app
app = Flask(__name__)
title = "PURE3D: An Infrastructure for Publication and Preservation of 3D Scholarship"
heading = "Pure 3D: Web Interface for Annotations"

def render_md():
    import markdown

    for root, dirs, files in os.walk("./data/editions"):
        for file in files:
            if file == 'about.md':
                filename = os.path.join(root, file)

                with open(filename, 'r') as f:
                    text = f.read()
                    html = markdown.markdown(text)
                    return html

def select_edition():
    data = []
    for root, dirs, files in os.walk("./data/editions"):
        for file in files:
            if file == "name.txt":
                filename = os.path.join(root, file)

                with open(filename) as f:
                    data.append(f.readline())

    return data


def wrapEditions():
    html = []
    for (n, e) in enumerate(select_edition()):
        html.append(f"""<a href="/{n + 1}">{e}</a>""")
    return "<br>".join(html)


@app.route("/")
@app.route("/home")
# Display home page
def home():
    editions = wrapEditions()
    return render_template("index.html", editions=editions)


@app.route("/about")
# Display the About page
def about():
    return render_template("about.html")


@app.route("/<n>")
def edition_page(n):
    n = select_edition()
    a_md = render_md()
    return render_template("edition.html", n=n, a_md=a_md)


if __name__ == "__main__":
    app.run()
