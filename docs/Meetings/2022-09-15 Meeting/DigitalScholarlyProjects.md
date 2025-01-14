# Themes:  
* The Digital Scholarly Project according to Pure3D  
* The role of the [Smithsonian Voyager](https://smithsonian.github.io/dpo-voyager/document/overview/) in the current setup  
* 3D and sustainability 
* collaboratively editing annotations to 3D datasets
* Smithsonian Voyager as an "editing" tool
* [Smithsonian Packrat](https://smithsonian.github.io/dpo-packrat/) versus Dataverse versus [Netlify](https://www.netlifycms.org/docs/intro/)



# Introduction
The technique of presenting digital objects in 3D opens up new ways to represent the results of research. Art history, history, architecture, are among the disciplines that benefit the most of these new ways. However, including 3D data in conventional infrastructures for scholarly dissemination poses challenges. There is quite a bit of technology involved to turn 3D data into immersive experiences on a computer screen. How can these experiences be recreated after considerable time, when the technology has changed and the data is (hopefully) still the same? How can we annotate 3D models, add narratives to those models, and embed those models in bigger narratives?
Pure3D is meant to be an infrastructure where researchers can create, archive and disseminate Digital Scholarly Projects in which 3D models play a central part.

We are going to discuss how we can achieve that. It is not a trivial task, because we have to define new concepts that reflect new ways of working because of the things that 3D technology brings to the table. Yet these ways of working should deliver output to the scholarly record, and that brings its own tableful of familiar patterns and requirements.

# 3D Scholarly Digital Projects
You might expect that on a 3D infrastructure you want to preserve 3D data. But Pure3D is meant as a *research* infrastructure, and we want to preserve research output, which is a bit more than just data. Research data needs to be accounted for, it will be subject to reasoning, commenting and discussing. The data may be needed later to verify or replicate conclusions, or to be used in answering different questions. A concept that summarizes this is that of the *Scholarly Edition*, which comes from the textual digital humanities. An edition of a significant text, handed over through history into our hands, consists of a rendering of that text to our best knowledge, with annotations that discuss uncertainties in the transmissions and things in those texts that cannot be understood without knowing the context. Such an edition used to be published in a book or in a series of volumes, and to become a source of knowledge of its own. Nowadays such editions can also be made and published digitally. There are new opportunities to visualize the variants that occur in the traditional work, the relationships with manuscripts and earlier editions, and bodies of annotation, sometimes machine generated.
What happens if we use 3D data as an edition? Think of an historic artefact, a work of art, a neighbourhood, a landscape, a ruin. A team of modellers has recreated the physical object and possibly some surrounding physical space into one or more 3D models, which may have become very detailed. With current technology these models come to life in desktop applications and even web browsers, so that users can interact with these models. They walk around the model, inside the model, through the model. But this is not enough. Models on their own cannot do all the communication with the users. Users should be pointed out what the interesting points and perspectives are, how the models invoke context knowledge. There are tools to enrich models with exactly this kind of information: annotations, articles, tours, overlays. Some of these enrichments are closely tied to the geometry in the models (tours, overlays and annotations), other parts can exist outside the models (articles), although they still point to the geometry. Such a collection of information we call a (3D) Digital Scholarly Edition (DSE).
The first-class citizens on the pure3D infrastructure will be 3D-Digital-Scholarly-Projects, which are collections of DSEs plus a connecting narrative. DSPs are like datasets in a Dataverse repository.

**A 3D-Digital-Scholarly-Edition (DSE) is a set of models plus a set of linked information in the form of annotations, articles, tours, overlays which all come to life when viewing the models in a 3D viewer that supports the extra information.**

Several DSEs can be combined in a Digital Scholarly Project.

**A 3D-Digital-Scholarly-Project (DSP) is a set of DSEs plus a scholarly narrative in which they are embedded.**

The narrative texts and the editions are all interlinked. The texts in the narratives and articles and annotations can refer to media content, and such media content can also be included in the DSEs and the DSP.

In order to arrive at how we are going to realise the DSP/DSE concepts in Pure3D, we consider what people will do with them.

# 3D Scholarly Work Processes
It is important to have a mental model of how DSPs are developed, maintained, and (re)used. We use terms from the archiving world to classify these processes:
* **SIP** Submission Information Package: what a data-creator must prepare so that a repository can ingest a DSP;
* **AIP** Archival Information Package: how the archive stores DSPs;
* **DIP** Dissemination Information Package: how the archive disseminates DSPs.

## SIP
The hard work of digitising something in the real world into a 3D model is out of scope here. We assume that researchers somehow have succeeded in doing this, and now they want to tell their research story about this piece of the real world by making use of this model.
This is the part we want to facilitate. As we see it now, we give them a workspace, centered around a single DSP. In that workspace, a team of editors can create DSEs centered around 3D models, and then produce tours and overlays for them, as well as annotations targeted at specific objects in the models or even complete articles. They can include additional content such as images and videos.
When they are done, they can submit the contents of their workspace to the Pure3D repository, which will perform checks, offer previews, etc. When all is well, the fresh DSP is safely archived. The editors can then issue the *publish* command after which the repository publishes the DSE to the outside world and gives it a persistent identifier. After publishing the workspace can be deleted.
Should a new version of a DSP be needed, users can ask for a new workspace, loaded with the latest version of a DSP. They can then edit the project, until they publish it as a new version.

## AIP
The task for the repository is to preserve DSPs as they are submitted. Preservation means that the experience that the editors have created can be reproduced from then on to the indefinite future. Of course, this is too ambitious, and we will water it down sensibly. Authors are asked to store a collection of pdfs, screenshots, videos that together give a representative picture of the 3D content. This can be a useful fall-back for times when there is no software anymore to open 3D models.
Nevertheless, the archive must keep track of the viewer software that has been used to create any of its DSPs.
The archive will also allow versioning, so that creators can add new versions with errata and newer insights.
Last but not least, but this is optional, the archive has the potential to let DSPs be annotated by others.
A special challenge is to maintain enrichments in ways that are independent of the viewer technology that created them. More about this under the section "Annotation Tools".

## DIP
When users want to consult published DSPs, the repository must allow them to search and browse DSPs by their metadata, by the textual content of the enrichments, and possibly by characteristics of the models themselves (geo-temporal coordinates, quality, number of objects, kinds of objects, etc.). Once a user has found a particular DSE, it must be sent to the user's browser where it can be rendered in a 3D viewer selected by the user. It would also be nice if users can view articles and annotations outside any 3D viewer.

# 3D Annotation Tools
There are several 3D webviewers that allow users to annotate 3D data models. The [Smithsonian Voyager](https://smithsonian.github.io/dpo-voyager/), [Virtual Interiors](https://www.virtualinteriorsproject.nl), and [Aton](http://osiris.itabc.cnr.it/aton/), to name a few. They all offer the possibility to target parts of the model and stick annotations to those parts. However, they all have different interfaces and capabilities. And the format in which annotations are saved are not completely standardized. Different viewers might use different conventions, although the glTF format for 3D data acts as a unifying principle. 
Desktop applications such as Blender also offer ways to put additional information into the model, but you really have to be an expert, and there are very few conventions how to do this in a standard way.

# Challenges
For the builders of Pure3D the main challenge is to implement the goals and ideas of Pure3D to structures and components that exist or can be built. The added challenge is that we cannot build everything from scratch, we have to select building blocks that exist now, and compose an infrastructure out of that.
Whenever we select existing building blocks we will face issues that the functionality will not match 100% of our desiderata.
Whenever we decide to build something from scratch, we will face the issue that it takes excessive time, and that the maintenance burden will be significantly increased.
These are all generic challenges. There are also some very specific challenges for Pure3D.

The question is: *what does a DSP look like, once the concept has been made operational on the Pure3D infrastructure?* We do not know yet, but let's keep this question in mind when we review some of the more concrete challenges below.

## Data entangled with tools
The fact that 3D Web Viewers play a crucial role in adding annotations means that research data becomes heavily entangled with the current technology of 3D viewers. The mixing up of data and tools is an [anti-pattern](https://en.wikipedia.org/wiki/Anti-pattern) in digital preservation. But at the moment we do not have an alternative. In fact, in developing Pure3D we must try to mitigate the entanglement and suggest ways in which the annotation of 3D resources can be more independent of the choice of 3D Viewer.

When all access to a DSE is channelled through a 3D viewer, which uses a long stack of hardware and software components, there is a real risk that in a few years it just does not work anymore that way. Either we must make sure that the current viewing experiences can be re-enacted later by emulation of existing viewers, or we must provide alternative ways to access annotated content. Note that the viewing of 3D models itself is the lesser problem: it is being standardized into the [glTF](https://www.khronos.org/gltf/) format by the big players (the [Khronos group](https://www.khronos.org)) and coded into standard web technology. But the annotation mechanisms are currently volatile: all 3d-viewers are very much work-in-progress with regards to annotations.

## DSE versus DSPs
It is to be expected that a subject of interest cannot be captured by a single DSE. And if it could, it is likely that it is not practical. For example, if mine lamps are the subject of interest, it is possible to represent a collection of mine lamps in a single DSE. But it is much more convenient to create a DSP with several DSEs: DSEs for individual lamps, DSEs for spaces where they have been used, for locations where they have been collected, and so on. These DSEs need a narrative that binds all these models together. It must be able to take a reader from narrative to model, from model to other model, and from model back to other points in the narrative. The DSEs plus the narrative form the DSP.

## Inside the viewer or outside the viewer?
A DSE can provide an immersive experience, once it is loaded in a capable 3D viewer. So, can we define a DSE by means of the experience of 3D dataset(s) in a viewer?

The first thing we bump into is: viewer dependence. If the immersive experience is the defining element of a DSE, then a DSE becomes heavily dependent on the choice of viewer. Different viewers give different experiences. Different versions of the same viewer give different experiences. If we do nothing about it, DSEs are very much in danger of getting obsolete in just a few years.

There are other considerations as well:

1. Reading: while the 3D viewers do offer immersive experiences, it remains to be seen what happens when the content of the annotations grows (note that annotations can contain whole rich-text articles). It may prove difficult to consume those annotations from within the viewer. Moreover, not all texts need to be read in the proximity of the 3D viewing experience. Interested readers will want to go back and forth between the world of hyperlinked text and the world of 3D scenes. Rather than locking readers up in a 3D scene, we should facilitate the jumping back and forth between the hyperlinked world of text and the immersive world of 3D scenes.
1. Research practice: researchers do not exclusively want immersive experiences, although that *is* undoubtedly one of the selling points of 3D data. They also engage in systematic analysis of data, and for that reason they may want to access the annotated material in other ways, outside the viewer. For example, they might want to do text-mining on the annotations across several DSEs or even DSPs.
1. Authoring: the collective annotations form a body of writing that may need review before publishing. Changes must be made to the material, some of which will be systematic, across all annotations (e.g. spelling mistakes, naming conventions, layout conventions). Some of them will mean a major rearrangement of the material, where texts of different annotations get merged, or annotations split in different texts. This is very hard to do from within the 3D viewers. 3D viewers are good in representing 3D models and providing anchor points, but they are very primitive in supporting the edit process of a family of texts.

# Facilitating DSPs
Pure3D has to facilitate DSEs as research output. Its support ranges from creating the annotations to storing all the data of the editions and to making the editions usable to the readers.
This is not a specification document where we describe those processes in detail. Here we only give a broad sketch but we do get into some detail where we expect bumps in the road.

## Creating DSPs
Above we described the notion of workspaces, one for each DSP during its creation process. Here is a list of things that deserve special attention:

### Collaboration
Each workspace should be workable by a team of people without intervention of the management of Pure3D. CLARIAH users are allowed to request workspaces that they then can administer. They can invite other CLARIAH users to the workspace, change their roles, and remove them from the workspace. Admin users of the workspace can *archive* and *publish* its content and finally delete the workspace.

### Metadata
The DSP as a whole needs metadata. For now we take Dublin Core as our lead. But its individual DSEs also need dedicated metadata. This goes on: the 3D models at the heart of the DSEs require metadata; the media files used in articles and narrative texts need metadata. Even the articles themselves and the individual annotations need metadata. For now our approach is: we start with Dublin Core and extra vocabulary when needed. We must take care that
* the metadata vocabulary is standardized, so that it can be recognized by other systems that use metadata harvested from Pure3D;
* there should not be an excessive burden on the users to provide metadata;
* DSEs inherit some metadata from their DSP, 3D models inherit some metadata from their DSE, annotations, articles and media may inherit metadata from the surrounding DSE and DSP.

### Provenance
A special case of metadata is provenance. The workspace must assist in keeping track of who contributed to models, annotations and texts. A light-weight way of doing that is to generate the list of admins of the workspace as creators and the the list of editors of a workspace as contributors.
More involved is the annotation process: it would be nice that when annotations are saved, the writer of the annotation ends up in the annotation's provenance metadata.

### Annotating
When editors save annotations they have created in a 3D viewer, we have to intercept the saved annotation and do intelligent things with it. 

1. **Format normalization**. Every viewer has a different data format for saved annotations and we would really like to be as viewer-independent as possible. This calls for a conversion of saved annotation data to a canonical format. We also must be able to be able to convert from the canonical format to every viewer specific format. That way we can show annotations made by one viewer (version) in another viewer (version). This becomes really important when viewers become obsolete. There will be cases when we need to open annotations in another viewer (version) than the one in which they have been created.
2. **Adding provenance metadata**. There are more things that have to happen: the author/editor of the annotation should be added to the annotation data. This is especially important if we choose to give the opportunity to annotate editions after they have been published, by later readers and users. Maybe the annotation is part of a group of related annotations, so it would be nice to be able to add that as well.
3. **Make annotations searchable**. And we want to be able to search annotations, so we need to make the content of annotations available to search engines.

Viewers tend to save rich text annotations in HTML, but we would rather like to use Markdown as an authoring format of rich text throughout Pure3D, not only for annotations, but also for articles, help texts, descriptions, etc. However, we need to extend Markdown in order to write links that open 3d-models in a selected 3d-viewer with a selected set of annotations loaded. The issue here is that we want to include widget-like things that contain 3d-models presented in a 3d viewer, and that can be switched to full-screen by the user. That means, we need an `<iframe>` rather than a plain markdown links.
An interesting way of extending Markdown is [mdx](https://github.com/micromark/mdx-state-machine#72-deviations-from-markdown). 

There is a technical stumbling block in intercepting saved annotations from viewers. The viewers that we know use the WebDav protocol to get data from the server to the client and back. That is good and handy for demo setups, but when the business-logic becomes more complex  we have to deal with that.

**Update**
The Voyager viewer does not make use of WebDav when used in *explorer* mode, i.e. readonly mode where the user can view annotations and articles. Only in *story* mode, where the user can write annotations and articles, WebDav is used. We managed the technique of enhancing an arbitrary Flask application with WebDav functionalitiy and get Voyager to work with it in *story* mode. See [voyager](../pilots/voyager.md).
Concerning ATON, at the moment of writing it seems that WebDAV is required in all cases.

### Authoring
A DSP is a complex piece of information. It is more like a website than a document. So how do we let editors author a DSP?
We could use familiar frameworks to author website content, known as content management systems, such as Wordpress. The disadvantage is that we have to support an instance of it for the very long term. There are more sustainable ways to do it: static page generators. Authors write their content in a set of markdown files, and the generator creates a set of static html pages out of it, that can be served indefinitely, without the burden of actively maintaining and securing additional software such as databases and content management systems. 

Moreover, it is also possible to use a version control system for the DSP. This is what git/GitHub/GitHub Pages offers in the wild. We could offer such an environment by means of GitLab-on-premise. However, git is not the most intuitive way to facilitate collaborative text writing. So either we should streamline that experience greatly, or we should look for alternative systems in the [Jamstack](https://jamstack.org) that offer version control together with a good collaborative experience.
A source of inspiration is [DARIAH-Campus](https://github.com/DARIAH-ERIC/dariah-campus/tree/main/src/pages). They tackle the problem of streamlining git operations so that users no longer see them, to the extent that even non-github users can create commits and pull-requests without being aware of it. 

## Storing DSPs
We need a repository system to store the DSPs. The system must be able to ingest the contents of a finished workspace and store it as an archival package.
That package will look like an exact copy of the workspace, with some minor differences:
* a persistence identifier is added
* a version number is added, and a link to the main landing page is added, and the main landing page will link to this version
* all the markdown has undergone a fresh rendering into HTML

Possibly some index material will be generated and stored with the DSP.
The big question here is: what do we use as repository system? GitLab, Dataverse, Fedora, Archivematica, PackRat?

Do we need a separate system for ingest (the workspaces) and dissemination, or can we do that using the capabilities of the chosen repository system?

## Disseminating DSPs
When users browse the repository and have selected a DSP to enter, they arrive at its home page (landing page). From there they will be linked to all DSEs in it. 
Readers must be able to open DSEs in a selection of viewers, including the original viewer version that was used to create the resource.
The default should be the original viewer but in the latest version. If a user is not satisfied with that, (s)he should be able to select other options.

If we want to make it possible to annotate DSEs after they have been published, here is the place where we have to make that possible. Authenticated users will then see annotation controls in their viewer, and when they save their work, the data should go to a dedicated place.
There are several options from here:
1. the archive stores such user-contributed data, and makes it available to subsequent users (only if users want to see them)
2. users are responsible to find a place to store their annotations. When they save them to a place that is accessible online (e.g. in a repository), they should able to call them up later, and also users should be given that possibility. In that case the software that disseminates the DSE must offer controls to import such data on the fly. A bit like the [nbviewer service](https://nbviewer.org) that renders online Jupyter notebooks, but does not store them in a repository. 

# FAIR
So far we have not mentioned the [FAIR principles](https://fairaware.dans.knaw.nl) (findable, accessible, interoperable, reusable) explicitly. But they are all over the place. When Pure3D users contribute DSPs to the infrastructure, they should encounter various points at which they have to provide metadata and narrative texts. In that way, their DSPs comply with the **FA** bits of **FAIR**. When they make annotations, the Pure3D system must take action that those annotations comply with i**IR** as well, i.e. that other viewer software can work with them and that they can be used for other purposes as well, e.g. data mining.
