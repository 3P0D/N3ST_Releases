import bpy
class N3ST_RENAMER_OT_applyname_geo(bpy.types.Operator):
    bl_idname = "n3st_renamer.applyname_geo"
    bl_label = "Mesh"
    bl_description = "Rename the selection of MESHES into a given prefix."
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        sel = context.selected_objects
        prefix = getattr(context.scene, 'newName_geo', "")
        any_renamed = False
        for obj in sel:
            if obj.type == 'MESH':
                if not obj.name.startswith(prefix):
                    obj.name = prefix + "_" + obj.name
                    any_renamed = True
        return {'FINISHED'} if any_renamed else {'CANCELLED'}
def register():
    bpy.types.Scene.newName_geo = bpy.props.StringProperty(name="Mesh", default="GEO")
    bpy.utils.register_class(N3ST_RENAMER_OT_applyname_geo)
def unregister():
    bpy.utils.unregister_class(N3ST_RENAMER_OT_applyname_geo)
    del bpy.types.Scene.newName_geo
