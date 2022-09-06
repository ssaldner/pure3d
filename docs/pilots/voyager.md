# Taming the Voyager

[Voyager](https://github.com/Smithsonian/dpo-voyager) is a web-based
3D viewer by which you can viewe annotated 3D models.
You can also edit those annotations and create new ones.

Here we show how we can serve the voyager, the 3D models, and the
annotations by a simple [flask](https://github.com/pallets/flask/) webserver.

The Voyager comes in various [flavours](https://smithsonian.github.io/dpo-voyager/introduction/getting-started/):

*   **explorer**: to just view a 3d model with its annotations
*   **story**: to view a 3d model and author/edit/delete annotations

We have made a collection of pilots to show how we can serve
these flavours of Voyagers.

In order to run them, clone this repository,
and on the command-line, `cd` into the top-level of the clone, and say

```
pip3 install -e .
```

(including the `.` at the end of the line)

Then 

```
cd scripts
```

# Voyager explorer

To view annotations in read-only mode, we use voyager-explorer.
This can be served by a minimal flask server without much ado.

You can see it by doing

```
./pilot.sh voyager-explorer prod
```

A flask server is started, a web browser opens and loads a page
with the Voyager. After a bit of clicking you see something like
this:

![screenshot](https://github.com/CLARIAH/pure3d/blob/main/docs/pilots/images/clanwilliam1-2.jpg)

The source code is in 
[pilot voyager-explorer](https://github.com/CLARIAH/pure3d/tree/main/pilots/voyager-explorer), see in particular the controllers in
[app.py](https://github.com/CLARIAH/pure3d/blob/main/pilots/voyager-explorer/app.py)
and the template
[index.html](https://github.com/CLARIAH/pure3d/blob/main/pilots/voyager-explorer/templates/index.html).

When you are done with the pilot, press `Ctrl+C`.

# WebDav

Before we can show the voyager-story we have to do some preparation.

The thing is, voyager-story expects to talk with a 
[webdav server](https://www.comparitech.com/net-admin/webdav/)

> WebDAV extends the set of standard HTTP methods and headers
to provide the ability to create a file or folder,
edit a file in place, copy or move or delete a file, etc.

This is the chosen way by which the voyager transmits user contributed data to the server: annotations, articles and media files.

Our flask app is not a WebDav server.

But we can easily fire up a WebDav server in Python, 
using the library [wsgidav](https://github.com/mar10/wsgidav).

You can see it in action by doing

```
./pilot.sh webdav
```

Your web-browser will open with a directory listing of the data directory,
which is served by this webdav browser.

The source code is in 
[pilot webdav](https://github.com/CLARIAH/pure3d/tree/main/pilots/webdav), see in particular the controller
[app.py](https://github.com/CLARIAH/pure3d/blob/main/pilots/webdav/app.py).

# Chaining

That is fine, but how can we combine the flask app with the webdav app?
A hopeful sign is that both are wsgi apps, so maybe we can chain them
somehow.

It turns out that flask has a
[tool](https://flask.palletsprojects.com/en/2.2.x/patterns/appdispatch/#combining-applications)
to do just that.

To show the idea, there is a pilot that chains to trivial flask apps:

```
./pilot.sh chainingstraight
```

The source code is in 
[pilot chainingstraight](https://github.com/CLARIAH/pure3d/tree/main/pilots/chainingstraight),
see in particular the controllers in
[app1.py](https://github.com/CLARIAH/pure3d/blob/main/pilots/chainingstraight/app1.py)
and
[app2.py](https://github.com/CLARIAH/pure3d/blob/main/pilots/chainingstraight/app2.py)
which are being chained in 
[app.py](https://github.com/CLARIAH/pure3d/blob/main/pilots/chainingstraight/app.py)
and the template
[index.html](https://github.com/CLARIAH/pure3d/blob/main/pilots/chainingstraight/templates/index.html)

However, there is a quirk with this chaining: after the initial part of the url has been
determined the app to which control should be dispatched, that initial part is stripped
from the url, and the remainder is what the target app sees.

We want to pass the full url, not the trimmed one, to the target app.

For that, we have customised the werkzeug library, by copying the DispatcherMiddleware class
to a local file, and modifying the class.

To see it, do:

```
./pilot.sh chaining
```

The Dispatcher source code is in
[dispatcher.py](https://github.com/CLARIAH/pure3d/blob/main/pilots/chaining/dispatcher.py)
used by
[app.py](https://github.com/CLARIAH/pure3d/blob/main/pilots/chaining/app.py).

The rest is equal to `chainingstraight`.


# Voyager story - attempt 1

Now we can deploy a server that can handle voyager-story.

You can see it by doing

```
./pilot.sh voyager-story-attempt1
```

A flask server is started, a web browser opens and loads a page
with the Voyager. After a bit of clicking you see something like
this:

![screenshot](https://github.com/CLARIAH/pure3d/blob/main/docs/pilots/images/story.jpg)

The idea is that the http commands that voyager-story sends to 
the server are intercepted by the webdav part of the chained server,
and everything else by the flask app part of the server.


The source code is in 
[pilot voyager-story-attempt1](https://github.com/CLARIAH/pure3d/tree/main/pilots/voyager-story),
see in particular the controllers in
[app.py](https://github.com/CLARIAH/pure3d/blob/main/pilots/voyager-story-attempt1/app.py)
and
[webdavapp.py](https://github.com/CLARIAH/pure3d/blob/main/pilots/voyager-story-attempt1/webdavapp.py)
and the template
[index.html](https://github.com/CLARIAH/pure3d/blob/main/pilots/voyager-story-attempt1/templates/index.html).

## Problematic journey

If the WebDAV setup is not exactly right, you are bound to get problems.
In this attempt we use the wrong chaining, see
[pilot voyager-story-attempt1](https://github.com/CLARIAH/pure3d/tree/main/pilots/voyager-story-attempt1).

The tricky thing is that an awful lot goes right, but not everything.
First I could fix a number of problems by fixing something in the Voyager code,
but subtle bugs kept appearing.

Then I discovered that I should also fix by WebDAV server setup.

# Voyager story

Now we can deploy a server that can handle voyager-story *properly*.

You can see it by doing

```
./pilot.sh voyager-story
```

These are the differences:

*   We use the customised dispatcher (like in pilot `chaining` and unlike before as in `chainingstraight`).
    See [app.py](https://github.com/CLARIAH/pure3d/blob/main/pilots/voyager-story/app.py) and
    See [webdavapp.py](https://github.com/CLARIAH/pure3d/blob/main/pilots/voyager-story/webdavapp.py) and
*   I patched one remaining little issue in the Voyager code, both in
    [voyager-story.dev.patch.js](https://github.com/CLARIAH/pure3d/blob/master/pilots/static/dist/js/voyager-story.dev.patch.js) and
    [voyager-story.min.patch.js](https://github.com/CLARIAH/pure3d/blob/master/pilots/static/dist/js/voyager-story.min.patch.js).
    See more in [issue 159 in the voyager repo](https://github.com/Smithsonian/dpo-voyager/issues/159).

In the process we also sanitized the data organization of articles and media files in our example dataset.
The images are in a `media` folder, and this folder now resides inside the `articles` folder instead next of it.

# Voyager roundtrip

Now we can show a voyager roundtrip, where we load a model, and view its annotations,
then modify an article in an other tab, and observe the changes in the first viewer.

Let's walk through this scenario screenshot by screenshot.
If you do it yourself, do

```
./pilot.sh voyager-roundtrip prod
```

You're in the viewer (Voyager-Explorer):

![screenshot](https://github.com/CLARIAH/pure3d/blob/main/docs/pilots/images/round1.jpg)

Click on the edit link and you get a new tab where you're in Voyager-Story:

![screenshot](https://github.com/CLARIAH/pure3d/blob/main/docs/pilots/images/round2.jpg)

Now make an edit in the title (an extra `XXXX`) and in the text (an extra `XXXX`).
Note that we have changed the title as it appears in the metadata on the left,
but not as it appears in the heading of the article itself.

Make sure you save the article and the whole story (there are two save buttons).
The latter is in order to save the metadata into the scene file, i.e. the clanwilliam.json file.

![screenshot](https://github.com/CLARIAH/pure3d/blob/main/docs/pilots/images/round3.jpg)

Go back to the previous tab where the viewer is still open.
Do a refresh. Navigate to the articles. You'll see the change in the metadata.

![screenshot](https://github.com/CLARIAH/pure3d/blob/main/docs/pilots/images/round4.jpg)

Click on the article. You'll see the change in the body text.

![screenshot](https://github.com/CLARIAH/pure3d/blob/main/docs/pilots/images/round5.jpg)





