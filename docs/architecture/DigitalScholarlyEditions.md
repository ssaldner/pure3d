# Abstract
#2022-08-10
We are entering a phase of heavy development, starting out with tech that we control now. But we must steer towards tech that is sustainable, and make sure that the products of Pure3D users are FAIR. How can we assure this in the specific context of 3D tech to represent and annotate data?

Themes:  
* The Digital Scholarly Edition according to Pure3D  
* The role of the Smithsonian Voyager in the current setup  
* 3D and sustainability 
* collaboratively editing annotations to 3D datasets
* Smithsonian Voyager as an "editing" tool
* Smithsonian Packrat versus Dataverse

Venue: Amsterdam, Spinhuis
# Introduction
The technique of presenting digital objects in 3D opens up new ways to represent the results of research. Art history, history, architecture, are among the disciplines that benefit the most of these new ways. However, including 3D data in conventional infrastructures for scholarly dissemination poses challenges. There is quite a bit of technology involved to turn 3D data into immersive experiences on a computer screen. How can these experiences be recreated after considerable time, when the technology has changed and the data is (hopefully) still the same? How can we annotate 3D models, add narratives to those models, and embed those models in bigger narratives?
Pure3D is meant to be an infrastructure where researchers can create, archive and disseminate Digital Scholarly Editions in which 3D models play a central part.

We are going to discuss how we can achieve that. It is not a trivial task, because we have to define new concepts that reflect new ways of working because of the things that 3D technology brings to the table. Yet these ways of working should deliver output to the scholarly record, and that brings its own tableful of familiar patterns and requirements.

# 3D Scholarly Digital Editions
You might expect that on a 3D infrastructure you want to preserve 3D data. But Pure3D is meant as a *research* infrastructure, and we want to preserve research output, which is a bit more that just data. Research data needs to be accounted, it will be subject to reasoning, commenting and discussing. The data may be needed later to verify or replicate conclusions, or to be used in answering different questions. A concept that summarizes this is that of the *Scholarly Edition*, which comes from the textual digital humanities. An edition of a significant text, handed over through history into our hands, consists of a rendering of that text to our best knowledge, with annotations that discuss uncertainties in the transmissions and things in those texts that cannot be understood without knowing the context. Such an edition used to be published in a book (series), and to become a source of knowledge of its own. Nowadays such editions can also be made and published digitally and published. There are new opportunities to visualize the variants that occur in the traditional work, the relationships with manuscripts and earlier editions, and bodies of annotation, sometimes machine generated.
What happens if we use 3D data as an edition? Think of an historic artefact, a work of art, a neighbourhood, a landscape, a ruin. A team of modellers has recreated the physical object and possibly some surrounding physical space into one or more 3D models, which may have become very detailed. With current technology these models come to live in desktop applications and even web browsers, so that viewers can interact with these models. They walk around the model, in the model, through the model. But this is not enough. Models on their own cannot do all the communication with the users. Users should be pointed out what the interesting points and perspectives are, how the models invoke context knowledge. There are tools to enrich models with exactly this kind of information: annotations, articles, tours. Some of these enrichments are closely tied to the geometry in the models (tours and annotations), other parts can exist outside the models (articles), although they still point to the geometry.
3D-Digital-Scholarly-Editions are the first-class citizens on the Pure3D infrastructure. In the same way as datasets function as the prime objects in a Dataverse repository. But we have not yet told how we think we are going to realize the DSE concept in Pure3D. Let's first consider what people do with them, and then come to a statement how we are going to realize them.
# 3D Scholarly Work Processes
It is important to have a mental model of how DSEs are developed, maintained, and (re)used. We use terms from the archiving world to classify these processes:
* **SIP** Submission Information Package: what a data-creator must prepare so that a repository can ingest a DSE;
* **AIP** Archival Information Package: how the archive stores DSEs;
* **DIP** Dissemination Information Package: how the archive disseminates DSEs.

## SIP
The hard work of digitizing something in the real world into a 3D model is out of scope here. We assume that researchers somehow have succeeded in doing this, and now they want to tell their research story about this piece of the real world by making use of this model.
This is the part we want to facilitate. As we see it now, we give them a workspace, centered around a single DSE. In that workspace, a team of editors can produce tours and overlays in the models of the DSE, they can write annotations pointed at specific objects in the models, they can write articles and link those to the models. They can include addtional content such as images and videos.
When they are done, they can submit the contents of their workspace to the Pure3D repository, which will perform checks, offer previews, etc. When all is well, the fresh DSE is safely archived. The editors can then issue the *publish* command after which the repository publishes the DSE to the outside world and gives it a persistent identifier.

## AIP
The task for the repository is to preserve DSEs as they are submitted. Preservation means that the experience that the editors have created can be reproduced from then on to the indefinite future. Of course, this is too ambitious, and we will water it down sensibly. Authors are asked to store a collection of pdfs, screenshots, videos that together give a representative picture of the 3D content. This can be a useful fall-back for times when there is no software anymore to open 3D models.
Nevertheless, the archive must keep track of the viewer software that has been used to create any of its DSEs.
The archive will also allow versioning, so that creators can add new versions with errata and newer insights.
Last but not least, but this is optional, the archive has the potential to let DSEs be annotated by others.
A special challenge is to maintain enrichments in ways that are independent of the technology that created them. More about this under the section "Annotation Tools".

## DIP
When users want to consult published DSEs, the repository must allow them to search and browse DSEs by their metadata, by the textual content of the enrichments, and possibly by characteristics of the models themselves (geotemporal coordinates, quality, number of objects, kinds of objects, etc.).
DSEs must be sent to the users' browsers where enriched models are presented in viewers selected by the user.

# 3D Annotation Tools
There are several 3D webviewers that allow users to annotate 3D data models. The Smithsonian Voyager, Virtual Interiors, and Aton, to name a few. They all offer the possibility to target parts of the model and stick annotations to those parts. However, they all have different interfaces and capabilities. And the format in which annotations are saved are not completely standardized. Different viewers might use different conventions, although the GLTF format for 3D data acts as a unifying principle. 
Desktop applications such as Blender also offer ways to put additional information into the model, but you really have to be an expert, and there are very little conventions how to do this in a standard way.

# Challenges
For the builders of Pure3D the main challenge is to implement the goals and ideas of Pure3D to structures and components that exist or can be built. The added challenge is that we cannot build everything from scratch, we have to select building blocks that exist now, and compose an infrastructure out of that.
Whenever we select existing building blocks we will face issues that their functionality will not match 100% of our desiderata.
Whenever we decide to build something from scratch, we will face the issue that it takes excessive time, and that the maintenance burden will be significantly increased.
These are all generic challenges. There are also some very specific challenges for Pure3D.

The preliminary question is: *what does a DSE look like, once the concept has been made operational on the Pure3D infrastructure?* We do not know yet, but let's keep this question in mind when we review some of the more concrete challenges below.

## Data entangled with tools
The fact that 3D Web Viewers play a crucial role in adding annotations means that research data becomes heavily entangled with the current technology of 3D viewers. The mixing up of data and tools is an anti-pattern in digital preservation. But at the moment we do not have an alternative. In fact, in developing Pure3D we must try to mitigate the entanglement and suggest ways in which the annotation of 3D resources can be more independent of the choice of 3D Viewer.

When all access to a DSE is channelled through a 3D viewer, which uses a heavy stack of hardware and software components, there is a real risk that in a few years it just does not work anymore that way. Either we must make sure that the current viewing experiences can be re-enacted later by emulation of existing viewers, or we must provide alternative ways to access annotated content. Note that the viewing of 3D models itself is the lesser problem: it is being standardized by the big players (the Khronos group) and coded into standard web technology. But the annotation mechanisms are currently volatile: all viewers are very much work-in-progress with regards to annotations.
## Single versus multiple 3D datasets
It is very likely that a subject of interest cannot be captured by a single 3D dataset. And if it could, it is likely that it is not practical. For example, if mine lamps are the subject of interest, it is possible to represent a collection of mine lamps in a single 3D set. But it is much more likely that a DSE on mine lamps contains 3D models of individual lamps, 3D models of spaces where they have been used, 3D models of locations where they have been collected, and so on. Such a DSE also needs a narrative that binds all these models together. It must be able to take a reader from narrative to model, from model to other model, and from model back to other points in the narrative.
## Inside the viewer or outside the viewer?
An enriched 3D dataset capable viewer can provide an immersive experience, once it is loaded in a capable 3D viewer. So, can we define a DSE by means of the experience of 3D dataset(s) in a viewer?

The first thing we bump into is: viewer dependence. If the immersive experience is the defining element of a DSE, then a DSE becomes heavily dependent on the choice of viewer. Different viewers give different experiences. Different versions of the same viewer give different experiences. If there is nothing else to a DSE, DSEs are very much in danger of getting obsolete in just a few years.

There are other considerations as well:

1. Reading: while the 3D viewers do offer immersive experiences, it remains to be seen what happens when the content of the annotations grows (note that annotations can contain whole rich-text articles). It may prove difficult to consume those annotations from within the viewer. Moreover, not all texts need to be read in the proximity of the 3D viewing experience. Interested readers will want to go back and forth between the world of hyperlinked text and the world of 3D scenes. Rather than locking readers up in a 3D scene, we should facilitate the jumping back and forth between the hyperlinked world of text and the immersive world of 3D scenes.
1. Research practice: researchers do not exclusively want immersive experiences, although that *is* one of the selling points of 3D data in the first place. They also engage in systematic analysis of data, and for that reason they may want to access the annotated material in other ways, outside the viewer. For example, they might want to do text-mining on the annotations across several DSEs.
1. Authoring: the collective annotations form a body of writing that may need review before publishing. Changes must be made to the material, some of which will be systematic, across all annotations (e.g. spelling mistakes, naming conventions, layout conventions). Some of them will mean a major rearrangement of the material, where texts of different annotations get merged, or annotations split in different texts. This is very hard to do from within the 3D viewers. 3D viewers are good in representing 3D models and providing anchor points, but they are very primitive in supporting the edit process of a family of texts.

## Provisional resolution
There are more challenges, but before we can even address them we need to make a choice about how we realize an edition.

**A 3D-Digital-Scholarly-Edition (DSE) is a set of models plus a scholarly narrative in which they are embedded, and which comes to live when viewing the models.**

The narrative texts and annotated models are all interlinked. The texts in the narratives and annotations can refer to media content, and such media content can also be included in the DSE.
