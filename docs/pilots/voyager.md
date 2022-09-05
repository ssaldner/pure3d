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
[app.py](https://github.com/CLARIAH/pure3d/tree/main/pilots/voyager-explorer/app.py)
and the template
[index.html](https://github.com/CLARIAH/pure3d/tree/main/pilots/voyager-explorer/templates/index.html).

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
[app.py](https://github.com/CLARIAH/pure3d/tree/main/pilots/webdav/app.py).

# Chaining

That is fine, but how can we combine the flask app with the webdav app?
A hopeful sign is that both are wsgi apps, so maybe we can chain them
somehow.

It turns out that flask has a
[tool](https://flask.palletsprojects.com/en/2.2.x/patterns/appdispatch/#combining-applications)
to do just that.

To show the idea, there is a pilot that chains to trivial flask apps:

```
./pilot.sh chaining
```

The source code is in 
[pilot webdav](https://github.com/CLARIAH/pure3d/tree/main/pilots/chaining), see in particular the controllers in
[app1.py](https://github.com/CLARIAH/pure3d/tree/main/pilots/chaining/app1.py)
and
[app2.py](https://github.com/CLARIAH/pure3d/tree/main/pilots/chaining/app2.py)
which are being chained in 
[app.py](https://github.com/CLARIAH/pure3d/tree/main/pilots/chaining/app.py)
and the template
[index.html](https://github.com/CLARIAH/pure3d/tree/main/pilots/chaining/templates/index.html)

# Voyager story

Now we can deploy a server that can handle voyager-story.

You can see it by doing

```
./pilot.sh voyager-story prod
```

A flask server is started, a web browser opens and loads a page
with the Voyager. After a bit of clicking you see something like
this:

![screenshot](https://github.com/CLARIAH/pure3d/blob/main/docs/pilots/images/story.jpg)

The idea is that the http commands that voyager-story sends to 
the server are intercepted by the webdav part of the chained server,
and everything else by the flask app part of the server.

There are still some problems with article editing,
but it seems that our chained server has the potential to
tame the voyager.
We have observed that new files have been created on the server
by WebDav commands emitted by the voyager while it was running
in the client.

The source code is in 
[pilot voyager-story](https://github.com/CLARIAH/pure3d/tree/main/pilots/voyager-story), see in particular the controllers in
[app.py](https://github.com/CLARIAH/pure3d/tree/main/pilots/voyager-story/app.py)
and
[webdavapp.py](https://github.com/CLARIAH/pure3d/tree/main/pilots/voyager-story/webdavapp.py)
and the template
[index.html](https://github.com/CLARIAH/pure3d/tree/main/pilots/voyager-story/templates/index.html).

## Problems

Articles do not load in the article editor.

An exception is raised in the Webdav code that is included in the Voyager-Story.


