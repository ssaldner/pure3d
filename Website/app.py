from flask import Flask, render_template, request, url_for  # for flask
import os

# create and configure app
app = Flask(__name__)
title = "PURE3D: An Infrastructure for Publication and Preservation of 3D Scholarship"
heading = "Pure 3D: Web Interface for Annotations"


def redirect_url():
    return (
        request.args.get("next") or request.referrer or url_for("home")
    )  # redirect to index page


def select_edition():
    data = []
    for root, dirs, files in os.walk("./editions"):
        for file in files:
            if file == "name.txt":
                filename = os.path.join(root, file)
                # print(filename)

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
    return render_template("edition.html", n=n)


if __name__ == "__main__":
    app.run()
