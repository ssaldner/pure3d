 # PURE3D - tech-demo day 
17-08-2022
**getting started with FAIR**

[Agenda and introduction](https://github.com/CLARIAH/pure3d/blob/main/docs/architecture/DigitalScholarlyEditions.md) 
*   11:00 - 11:30 Coffee, welcome, introduction of participants
*   11:30 - 12:00 Current state of Pure3D, with a demo of the "sandboxes"
*   12:00 - 12:30 Towards Pure3D as an infrastructure
*   12:30 - 13:30 Lunch
*   13:30 - 14:00 Agenda setting: which talking points do we have?
*   14:00 - 14:30 Discussion of 3D viewers as annotation tools
*   14:30 - 15:00 Discussion of reposystems? What can Dataverse do for us?
*   15:00 - 15:30 Next steps for the DANS involvement in Pure3D

# Participants:
University Maastricht:
*   Costas Papadopoulos (online)
*   Kelly Schoueri, Sohini Mallick

KNAW/HuC:
* Mario Mieldijk (partly)
* Dirk Roorda (chair)

DANS:
*   Jerry de Vries (Pure3D lead for DANS contribution)
*   Simon Saldner (Data expert)
*   René van Horik (Data expert, researcher, participates in 4CH)
*   Eko Indarto (Software developer, Java, Python)

# Themes:
* The Digital Scholarly Edition according to Pure3D
* The role of the Smithsonian Voyager in the current setup
* 3D and sustainability: 
* collaboratively editing annotations to 3D datasets
* Smithsonian Voyager as an "editing" tool
* Smithsonian Packrat versus Dataverse

# Minutes
In the morning Kelly and Sohini gave a demo of current 3D annotating in practice.
In the afternoon, Dirk introduced his document on Digital Scholarly Editions.
We organize the minutes by subject, and not by when we discussed it.

## Mount street bridge demo
Kelly gave a demo of the Mount Street Bridge dataset plus it annotations and indicated how these annotations have been created and by whom. It started with a sandbox setup where for each user a dedicated online filesystem and a dedicated Voyager viewer were connected, so that a users could save their own annotations on their own filesystem.
Mario reported that they were working on a shared filesystem, with backups, as a move to be protected from data-loss, and a step towards a real infrastructure.
Dirk remarked that in the end the infrastructure would send Voyager instances to the users' browsers and capture the saved annotations and store them somewhere on the infrastructure.
Now the saved data flows as json to the Nextcloud, later the webserver will receive the annotation data and process it according to which user made the annotations and to which edition (s)he is working on. It will end up in the user's workspace, which might be a GitLab repository!
The demo setting uses Nextcloud as a data backend for the Voyager, but in a webserver context that need not be the case, there will be much more control over the transactions between client and server.

## Viewer dependency
We discussed viewer dependency. The fact is that the choice of 3D viewer very much defines the annotation experience, even the shape of the annotation data. We must limit the viewer dependency and try to get basic interoperability between viewers (with viewer A you can view annotations made by viewer B).
There is a clear link with the **I** of **FAIR** here.

## Authoring annotations
Another point of interest: **authoring** annotations. The Voyager allows authors to enter text by means of a built-in rich-text editor which produces HTML. But if you want to insert a Sketchfab link, you have to edit the HTML output outside the viewer and fiddle an `<iframe>` element in. 
Dirk indicated that in a more mature Pure3D all texts should be writable as Markdown, plus extensions to enter links to 3D resources. Arbitrary HTML is less sustainable, more risky, and is a gateway to no end of complications later on (think of `<script>` tags!
Another consideration is that the editing environment within Voyager is not a good tool to manage many and lengthy annotations. Especially when annotations are the product of multiple authors, working collaboratively, we need something outside Voyager to facilitate that.

## Viewers as VREs
Voyager itself has indications how to use it in a VRE context. The Smithsonian uses it with Packrat, their 3D ingest system. We could use Packrat, but that is not trivial. If we use something else, then we have to dive deeper into Voyager in order to see how it interacts with backends. Possibly we need to add/modify some of its code to make it suitable for our purposes.

## Different types of user
Another thing that popped up is at the users' side. There seem to be at least two kind of users: researchers and museums, and their use cases differ.
Jerry:  the demo looks more like a museum use case than a researcher use case.
Costas: the museum partners of Pure3D are predominantly museums. That's why we started with Voyager.
If our partners were predominantly scholars, we would have gone for other interfaces, like Virtual Interiors, but then we would have to augment VI with editing capabilities.. 

## Virtual Interiors
There is yet another viewer in the picture: Virtual Interiors, which is attractive to researchers. But VI is still work in progress, and it needs additional development (e.g. editing functionality) by third parties to integrate it in whatever infrastructure.
    
## Deep linking and persistent identifiers
Persistent identifiers. It is one thing to persistently link to an edition as a whole, but how do you link persistently to the elements of an edition, or even to the parts of a 3D model?
You could use persistent identifiers with a resolution infrastructure to point to the edition as a whole, and make a system of fragment identifiers to point to parts of the edition.

## Fragment identifiers and standards
When you descend to parts of a 3D model, the `glTF` format provides ways to address them. The Voyager viewer uses these ways (but slightly modified) to do that for the targets of their annotations.
Other viewers, such as ATON seem to do the same, so we hope that the interoperability between viewers is a tractable problem.
And we have to solve it in order to be able to preserve annotations for the long term.
One use case for which this linking is particularly important is when researchers want to add observations and comments to existing editions and models: annotation in the wild after the creation process.

## Management of wild annotations
There are several choices for storing those annotations: let researchers store them in whatever online location; or let Pure3D store them on its own infrastructure. In both cases, Pure3D needs functionality to display models with annotation sets on demand by the user.
Jerry stresses the point that because of the immersive views that 3D models offer, later researchers can develop new insights that they want to share on top of an existing edition. A finished DSE is then still *living data*.
Also Kelly mentions the point that readers may want to leave annotations.

## The Digital Scholarly Edition concept
Dirk advocated a working definition of DSE, since we have to design the Pure3D infrastructure as an archive of DSEs, with its functions of (collaborative) ingest, archive management (with preservation planning), and dissemination.
The working definition is (still a bit vaguely):
*A collection of (markdown) texts that forms a narrative, together with a set of 3D models and their annotations, in such a way that the narrative can link to (elements) of the models, and the models can link via their annotations to parts of the narrative. Narrative and annotations may contain arbitrary media elements, such as images, videos and other 3D models.*
A DSE is a complex beast, not a single entity, and the task of preserving such a thing is not unlike preserving a website.
However, rather than preserving arbitrary websites, it is in our power to constrain DSEs in ways that make it easier to preserve them: eventually they will be converted to static HTML pages, where search controls are defined and implemented Pure3D wide, not per DSE.

### Wireframes
Sohini showed the wireframe diagram for the Pure3D component that will disseminate editions to the public. This triggered a number of ahas and remarks.

### Definition of a DSE
Both René and Jerry remarked that it would be nice to have a real definition of what a DSE can contain, expressed in metadata as well.
Dirk was a bit hesitant on this, because before you know you are over-analysing a problem, and then losing time to implement the result. Instead we should start with what we oversee now, and then refine when the need arises. What a DSE may contain might also be dependent on how exactly we will implement it, and that choice is not totally determined by top-down considerations, but also by bottom-up ones: what tools do we have, and what tools can we manage?
A first step in formalizing a DSE is defining the [workspace structure](https://github.com/CLARIAH/pure3d/blob/main/docs/architecture/SIP.md#workspace-structure) in which a DSE is being created. That will show quite a bit of the ingredients and organization of a DSE.
If we define too much, we run the risk to give researchers a straightjacket, instead of a platform on which they can do surprising things.

## Repository backends
### DANS and Dataverse
It is easy for DANS, using Dataverse, to store all the files that make up a DSE. But what is difficult, is to regenerate the experience of walking through the DSE, jumping from narrative to 3D models, even deeply inside them, and back. And it remains to be seen how we can do a well-organized ingest process on the basis of Dataverse.

### Repository as viewer backend
A 3D viewer is a piece of Javascript software that comes to live in the browser of the end-user. So it should be served by the backend. If a user writes an annotation, the viewer sends the saved annotation to the backend.
The backend must be able to handle serving out the viewer and receiving the saved data.
Repositories such a Dataverse can be augmented with viewers for specific data types, but to my knowledge they have no logic to capture user contributed content from those viewers.
So if we use Dataverse, we need extra middleware between Dataverse and the user that supports an annotating viewer.

### Workspaces for authoring
However, when a DSE is being authored, the process is much more complex than a series of sessions with Voyager. Several people work on the narrative, the media content, the annotations, and others do specialized tasks, such as proof-reading, correcting, supplying links to sources, etc.
For this we need a workspace per edition.
It is unlikely that generic repository systems like Dataverse offer workspaces in the ways we want. Packrat is a system that does offer such a workspace. And there are systems that are good in offering workspaces to people. Content management systems do that, but also GitHub/GitLab are good examples. Content management systems usually offer authoring environments, while GitHub/GitLab are best for authoring on distributed, local computers, with frequent merging of content.

### Where does Dataverse fit among these systems
Here is the real puzzle: suppose find a suitable workspace solution, and suppose that solution is also good for long-term preservation and for dissemination, what is then the remaining need for a proper archiving repository such as Dataverse?

DARIAH-Campus is an example of a headless content management system based on git data. In other words: it is based on GitHub/GitLab repositories, and it disseminates through static page generation (very sustainable) with some dynamic functions being implemented outside the individual repositories.
A system like this is good for ingest (workspace), good for long-term preservation (it also preserves the history of the creation quite well), and good for dissemination. 
The remaining archival functions could also be achieved by exporting the metadata to a trusted digital repository such as DANS, so that the contents of Pure3D is also findable by DANS users.
Dirk proposes to have a good look at DARIAH-Campus, to see what tools they have used, and consider the possibility to build up a backend with the help of those tools, e.g. Netlify.

## Metadata
René and Costas mention a few books on 3D data curation and metadata:
See: [curation-community-standards-for-3d-data-preservation/](https://acrl.ala.org/acrlinsider/3d-data-creation-to-curation-community-standards-for-3d-data-preservation/) (there is an open-access link at the bottom of the page that avoids the paywall) and [study-quality-3d-digitisation-tangible-cultural-heritage](https://digital-strategy.ec.europa.eu/en/library/study-quality-3d-digitisation-tangible-cultural-heritage)

## Fallbacks
Costas mentioned the [Electronic writing association - ELO](https://eliterature.org/) for its idea to produce lower-tech approximations of 3D models and DSEs that remain viewable over time, even if specific features of 3D rendering that we use have become obsolete. We have then a fall-back. Not only gives that an impression of the original resource, it can also help in the process of creating migrations of the original data, or emulators of the original tools. These materials then function as a check on the quality of the migrations/emulations.

# Takeaways

## Jerry
Good progress, but things are still flexible.
The wireframes were really helpful to gain more insight in scholarly editions. With my DANS hat I am interested in preserving DSEs, so I would like to delineate the concept of DSE more in order to be able to better preserve it.
With my researcher's hat I am very interested to find an infrastructure to realize these ideas, but that's more something for the HuC/CLARIAH party.
Best things happen if you discover things by accident, and for that you must keep trying new things. Let's keep each other informed. 
* [x] invite DANSers to Slack

## Eko
Look at B2SAVE (EUDAT) for storing (large binary data) using IRODS. Because while GitLab sounds very attractive, it is not optimal for large binary data, although LTS (large file support) could be sufficient.

## Simon
A useful meeting.
Suggestion: try to digest the findings of today into next steps, directions forward. Good better best (3D standards)
* [x] Will share my minutes.
* [ ] Will condense meeting into key conclusions, steps ahead etc
* [x] Dirk: merge in Simon's minutes.

## René
Learned a lot, thankfully. Good to see that concrete steps are taken. The DSE concept reminds me of SURF's *enriched publications*. The next step after defining such a concept is to get a huge community adopting it.

## Sohini 
The workspace structure is not exactly clear. The next step is: make that more clear, especially the relation between the individual DSEs and the aggregated structure of Pure3D.
* [-] Work together with Dirk in implementing a view on the workspace contents. This will gradually make most of the details clear. Work in progress.

## Kelly
It was good to be able to have a substantial meeting with the DANS people. Excited to move the partnership forward.
* [ ] I am a bridge between developer and parters. How can I teach the partners how to write a DSE? A workshop in DSE writing? With texts, metadata fields. Or a document?
* [ ] Use the Good/Better/Best format
That comes from the book [curation-community-standards-for-3d-data-preservation/](https://acrl.ala.org/acrlinsider/3d-data-creation-to-curation-community-standards-for-3d-data-preservation/)
Quote:
> Good/Better/Best (GBB) recommendations are offered as guidelines to address
>    *   the level of documentation to target based on audience and use
>    *   recommendations for file formats in consideration of access and/or preservation
>    *   PIPs (preservation intervention points) at which to save and preserve the 3D data
>    *   databases or repositories that target the needs of the intended audience

## Costas
Useful meeting. 
* [ ] I am already planning a series of workshops to help users a bit more on the editions. Introduce metadata to them. Definitive metadata schema. Even if preliminary.
Would like to see next:
* [ ] how do you DANS people see yourself within Pure3D? What new goals do you identify?

## Mario
Useful. The idea was to speed up the DANS people. Looks like it succeeded.
* [-] I am trying to arrange a sprint week for working together at a nice central location. For specific goals.
* [ ] Question to DANS: what are you able to deliver, what you want to deliver, and what do you need to deliver?

## Dirk
Good to see the 100% intense presence of everybody.
* [ ] Let's agree on a working concept of a DSE, so that we can implement an infrastructure for it.