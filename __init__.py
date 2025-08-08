bl_info = {
    "name": "N3ST 1.0.2",
    "author": "3P0D",
    "version": (1, 0, 2),
    "blender": (4, 4, 0),
    "location": "View3D > Sidebar",
    "description": "Lots of repetitive commands to optimize my workflow. Distributed as is. Updated whenever I can.",
    "category": "Utilities",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/3P0D/N3ST_Releases/"
}

from .general import (
    add_modifier_bevel,
    add_modifier_mirror,
    add_modifier_preparesculpt,
    add_modifier_shrinkwrap,
    apply_transform_general,
    apply_transform_rotation_rig,
    clear_make_single,
    clear_transform,
    clear_parents,
    create_empty,
    create_suzanne,
    fix_normals,
    fix_origin_to_selected,
)

from .renamer import (
    apply_name_bool,
    apply_name_curve,
    apply_name_empty,
    apply_name_geo,
    apply_name_rig,
)

from .exporter import (
    to_fbx,
    to_glb,
    to_gltf,
)

from .textures import (
    add_debug_material,
    add_uvchecker,
)

from .datas import (
    batch_rename_vertex_groups,
    remove_unused_vertex_groups
)

from .uveditor import(
    grid_projection_uv_flat,
    grid_projection_uv_gradient
)

from .animation import(
    bake_new_action,
    select_keys_intervals,
)

from ._panels import (
    panel_3dview,
    panel_animation,
    panel_exporter,
    panel_renamer,
    panel_textures,
    panel_uveditor
)

import bpy

to_register = [

    # ---- GENERAL ----
    add_modifier_bevel,
    add_modifier_mirror,
    add_modifier_preparesculpt,
    add_modifier_shrinkwrap,
    apply_transform_general,
    apply_transform_rotation_rig,
    clear_parents,
    clear_make_single,
    clear_transform,
    create_empty,
    create_suzanne,
    fix_normals,
    fix_origin_to_selected,

    # ---- RENAMER ----
    apply_name_bool,
    apply_name_curve,
    apply_name_empty,
    apply_name_geo,
    apply_name_rig,
    
    # ---- EXPORTER ----
    to_fbx,
    to_glb,
    to_gltf,
    
    # ---- MAT/TEXTURES ----
    add_debug_material,
    add_uvchecker,

    # ---- DATAS ----
    remove_unused_vertex_groups,
    batch_rename_vertex_groups,

    # ---- UV EDITOR ----
    grid_projection_uv_flat,
    grid_projection_uv_gradient,

    # ---- ANIMATION ----
    bake_new_action,
    select_keys_intervals,

    
    # ---- PANELS ----
    panel_3dview,
    panel_renamer,
    panel_exporter,
    panel_textures,
    panel_uveditor,
    panel_animation,
    

]

def register():
    for cls in to_register:
        cls.register()

def unregister():
    for cls in reversed(to_register):
        cls.unregister()
