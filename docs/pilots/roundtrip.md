
# Voyager roundtrip

Based on the preparations in the pilots described in the [voyager document](voyager.md),
we can show a voyager roundtrip, where we load a model, and view its annotations,
then modify an article in an other tab, and observe the changes in the first viewer.

## On your own computer
You can do this on your own computer, provided you can do the following:
* clone a GitHub repository
* work with the bash shell (Linux) or zsh shell (macos)
* run and install python things

Do this: start a command line and create a suitable directory to clone this repo and go there.

``` sh
git clone https://github.com/CLARIAH/pure3d
cd pure3d
pip3 install -e .
cd scripts
```

Now you're ready to run the roundtrip pilot by continuing with the command:

```
./pilot.sh voyager-roundtrip prod
```

Your default browser will open and display the *Clan William* scene file and model in the Voyager-Explorer viewer.
Click on the building and click on the `Articles` button. On the right you see a list of articles.
Click on the first article.

![screenshot](https://github.com/CLARIAH/pure3d/blob/main/docs/pilots/images/round1.jpg)

Now we are going to change that article. We have to open it in Voyager-Story.
Click on the edit link below the viewer and you get a new tab where you're seeing the same model in Voyager-Story.
Again, click on the building, click on the `Articles` button.
You get a list of articles on the left. Click on the first one.

![screenshot](https://github.com/CLARIAH/pure3d/blob/main/docs/pilots/images/round2.jpg)

Now make a change in the title (an extra `XXXX`) and in the text (also an extra `XXXX`).
Note that we have changed the title as it appears in the metadata on the left,
but not as it appears in the heading of the article itself.

Make sure you save the article and the whole story (there are two save buttons).
The latter is in order to save the metadata into the scene file, i.e. the `clanwilliam.json` file.

![screenshot](https://github.com/CLARIAH/pure3d/blob/main/docs/pilots/images/round3.jpg)

Go back to the previous tab where the viewer is still open.
Do a refresh. Navigate to the articles. You'll see the change in the metadata.

![screenshot](https://github.com/CLARIAH/pure3d/blob/main/docs/pilots/images/round4.jpg)

Click on the article. You'll see the change in the body text.

![screenshot](https://github.com/CLARIAH/pure3d/blob/main/docs/pilots/images/round5.jpg)

This completes the roundtrip.

## Observation
What you just saw is a little website, served by a simple webserver on your computer.
The webserver is capable of serving you a model plus scene inside the voyager-explorer, and it can
also serve you the same material in voyager-editor where you can edit the scene.

The webapp that does this, is a little Flask app, written in a few lines of Python.

We can now make that webapp bigger, so that we can serve many scenes and models to many users.
We do that by changing the logic of the webapp, instead of adding new installations of sandbox systems.

This step from sandbox to pilot is just the next step on the road to the Pure3D infrastructure.




