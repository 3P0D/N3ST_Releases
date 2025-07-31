# N3ST | Blender Releases >  1.0.1

<br>

this tool is primarily designed to automate the repetitive and tedious actions in my workflow. i hope it will be useful to you as well. updated whenever i can. i'm a beginner dev' so some conventions might not be followed.

<br>

#### DISCLAIMER
> this tool is provided "as is" without warranty of any kind, express or implied. the authors and contributors take no responsibility for any issues, damages, or losses resulting from the use of this software. use at your own risk. no official support or maintenance is guaranteed. while contributions and feedback are welcome, there is no commitment to fixing bugs, updating features, or answering support requests. please review the documentation before use, and test thoroughly before applying it to your own environment. 

#### DOCUMENTATION
> please take some time to review the features before using the tool. each feature and button includes a tooltip explaining its function. all features are also described in detail below. if you are unsure how a feature works, please refer to the tooltips.

---  

# TAB: N3ST CORE
Find this tab in the following editor(s): **3DVIEW**  

<br>  

## N3ST - 3DVIEW
#### → TRANSFORMS:
- apply a -90 rotation on rig (fix rig for Unity).
- apply all transforms.
- clear all transforms.
#### → GEOMETRY: 
- fix all normals (while in object mode).
- set origin to selected (in edit mode).
#### → PARENTS: 
- make singler user-data (break the link of instances).
- clear parents (and keep transforms).
#### → ADD OBJECTS:
- create an empty (in a 0,0,0 worldspace location).
- create a suzanne (in a 0,0,0 worldspace location).
#### → ADD MODIFIERS: 
- add a mirror (in X axis, with clipping and on cage options activated).
- add a bevel (with 'weight' limit method option activated).
- add a shrinkwrap + displ. (take the selected object as a target).
- apply transforms + modifiers, join meshes, and add a remesh modifier (following the value in the property box).

## N3ST - MATERIALS/TEXTURES:
#### → ADD CHECKER TEXTURE:
- 512, 1024, 2048, 4096.  
(all un-used textures and materials are cleared when reusing this option.)
#### → ADD DEBUG MATERIALS:
allows you to create debug materials on the go, either as placeholders or for fast IDmap assignment of materials.
- maximum: 24 colours. 8 colours per row. 0 colours by default.
- has a 'quick palette' option that generates a rainbow palette (optimal for idmapping).
- changing the colour within the palette will change the colour of the debug materials.

---  

# TAB: N3ST OBJECTS
Find this tab in the following editor(s): **3DVIEW**  

<br>  

## N3ST - RENAMER:
you can now customise your naming convention. those are default value.  
it will skip the batch renaming action if you already had set a prefix on the object.
#### SET PREFIX: 
- GEO_  
- RIG_  
- EMPT_  
- CURV_
- BOOL_  

## N3ST - EXPORTER:
you can now export your assets in batches, in 3 preset formats: FBX(binary), GLB, GLTF(+bin+textures).
- the exporter allows you to set a prefix to your file name based on the prefix of your model name. if it doesn't have any, it will just export the model's name.
- allows you to reset the transform before export, putting your model to 0-0-1. untoggle the option if you don't want this to happen.
- allows you to preserve the hierarchy of your models: if there is a parent, will export as a bundle. untoggle the option if you don't want this to happen.
allows you to remove the textures from the export. only available for GLB/GLTF export.

---  

# TAB: N3ST UVs 
Find this tab in the following editor(s): **3DVIEW**  

<br>  

## N3ST - UVs EDIT:
#### → UV PROJECTION: "FLAT"
a tool to make it easier for you move the UVs of your objects within texture made of a grid of colours.
- create a grid: you can choose independently the number of rows and columns of your grid.
- two options for the grid: either cell coordinates (A1, H8, etc...) or color preview cells.
- allows you to load an image texture and generate icons from its colors (taking the center of each cells of a grid).
- you can clear the image previews if you don't want them anymore. it does not delete them from your computer.
- a button allows you to open the file exporer where the images were saved (allowing you to delete or move them).
- clicking on a cell within the UI will move the selected faces to the corresponding cell in the UV grid.
###### WARNING: these icons are saved as 8x8 px PNG images within a folder where your file was last saved.

#### → UV PROJECTION: "GRADIENT"
a tool to make it easier for you project the UVs of your objects within a axis (X, Y, or Z) as "project from view" and move them within texture made of a grid of gradients.
- create a 'grid': you can choose independently the number of columns of your grid.
- each axis has its own row of cells to use. each cell correspond to a column.
- once you click on a cell, there will be a project from view unwrapping of the selected faces, made on the chosen axis, taking the whole height of the UV grid.
- the result of the action will then be moved to the corresponding column within the UV grid.
- the island will be scaled of 0.5 in X, and 0.99 in Y, taking most of the UV space.

---  

# TAB: N3ST ANIM
Find this tab in the following editor(s): **DOPESHEET**  

<br>  

## N3ST - ANIM:
#### → FRAME MANAGER
allows you to select the keyframes of a timeline given a specific interval of frames. also adds the first and last frame to the selection.

#### → BAKE ANIMATION
bake a new action from the selected frames within the dopesheet timeline. allows your to give it a name directly from the interface.

---  

# WITHIN MENUS: VERTEX GROUPS
#### → REMOVE UNUSED VERTEX GROUPS 
- remove all the vertex groups of the selected object that are not assigned to any weight.
#### → BATCH RENAME VERTEX GROUPS 
- search for prefix, suffix, or specific words and replace them within the vertexgroups of the selected object.

---  
