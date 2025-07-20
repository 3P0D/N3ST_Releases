# N3ST - Blender Toolbox

## CATEGORIES:
### 3D View (General)

#### APPLY CHANGES ON OBJECTS:
##### TRANSFORMS:
- apply a -90 rotation (fix rig for Unity).
- apply all transforms.
- clear all transforms.
##### GEOMETRY: 
- fix all normals (while in object mode).
- set origin to selected (in edit mode).
##### PARENTS: 
- make singler user-data (break the link of instances).
- clear parents (and keep transforms).

#### ADD MODIFIERS AND OBJECTS:
##### ADD OBJECTS:
- create an empty (in a 0,0,0 worldspace location).
- create a suzanne (in a 0,0,0 worldspace location).
##### ADD MODIFIERS: 
- add a mirror (in X axis, with clipping and on cage options activated).
- add a bevel (with 'weight' limit method option activated).
- add a shrinkwrap + displ. (take the selected object as a target).
- apply transforms + modifiers, join meshes, and add a remesh modifier (following the value in the property box).

### TEXTURES + MATERIALS:
#### ADD TEXTURES AND MATERIALS:
##### ADD CHECKER TEXTURE:
- 512, 1024, 2048, 4096.  
(all un-used textures and materials are cleared when reusing this option.)  

### BATCH RENAMER:
#### SET OBJECT NAMES:  
you can now customise your naming convention. those are default value.  
it will skip the renaming action if you already had set a prefix.
##### SET PREFIX: 
- GEO_  
- RIG_  
- EMPT_  
- CURV_
- BOOL_  
