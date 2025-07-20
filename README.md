# N3ST - Blender Releases

##### Disclaimer
this tool is provided "as is" without warranty of any kind, express or implied. the authors and contributors take no responsibility for any issues, damages, or losses resulting from the use of this software. use at your own risk.
no official support or maintenance is guaranteed. while contributions and feedback are welcome, there is no commitment to fixing bugs, updating features, or answering support requests.
please review the documentation before use, and test thoroughly before applying it to your own environment.

##### Documentation
(see below) this tool is mostly a way for me to automate the actions that i find too repetitive and tedious in my workflow. i hope it can be useful to you too. please take some time to review the features below before any use.
each feature and button has its own tooltip describing its actions. in doubt, check the tooltips.

## TAB: N3ST CORE

### N3ST - 3DVIEW
##### → TRANSFORMS:
- apply a -90 rotation on rig (fix rig for Unity).
- apply all transforms.
- clear all transforms.
##### → GEOMETRY: 
- fix all normals (while in object mode).
- set origin to selected (in edit mode).
##### → PARENTS: 
- make singler user-data (break the link of instances).
- clear parents (and keep transforms).
##### → ADD OBJECTS:
- create an empty (in a 0,0,0 worldspace location).
- create a suzanne (in a 0,0,0 worldspace location).
##### → ADD MODIFIERS: 
- add a mirror (in X axis, with clipping and on cage options activated).
- add a bevel (with 'weight' limit method option activated).
- add a shrinkwrap + displ. (take the selected object as a target).
- apply transforms + modifiers, join meshes, and add a remesh modifier (following the value in the property box).

### N3ST - MATERIALS/TEXTURES:
##### → ADD CHECKER TEXTURE:
- 512, 1024, 2048, 4096.  
(all un-used textures and materials are cleared when reusing this option.)
##### → ADD DEBUG MATERIALS:
allows you to create debug materials on the go, either as placeholders or for fast IDmap assignment of materials.
- maximum: 24 colours. 8 colours per row. 0 colours by default.
- has a 'quick palette' option that generates a rainbow palette (optimal for idmapping).
- changing the colour within the palette will change the colour of the debug materials.

## TAB: N3ST OBJECTS

### N3ST - RENAMER:
you can now customise your naming convention. those are default value.  
it will skip the batch renaming action if you already had set a prefix on the object.
##### SET PREFIX: 
- GEO_  
- RIG_  
- EMPT_  
- CURV_
- BOOL_  

### N3ST - EXPORTER:
you can now export your assets in batches, in 3 preset formats: FBX(binary), GLB, GLTF(+bin+textures).
- the exporter allows you to set a prefix to your file name based on the prefix of your model name. if it doesn't have any, it will just export the model's name.
- allows you to reset the transform before export, putting your model to 0-0-1. untoggle the option if you don't want this to happen.
- allows you to preserve the hierarchy of your models: if there is a parent, will export as a bundle. untoggle the option if you don't want this to happen.
allows you to remove the textures from the export. only available for GLB/GLTF export.


## MENUS: VERTEX GROUPS
##### → REMOVE UNUSED VERTEX GROUPS 
- remove all the vertex groups of the selected object that are not assigned to any weight.
##### → BATCH RENAME VERTEX GROUPS 
- search for prefix, suffix, or specific words and replace them within the vertexgroups of the selected object.
