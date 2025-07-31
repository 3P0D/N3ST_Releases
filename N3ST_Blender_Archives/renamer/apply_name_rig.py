import bpy
class N3ST_RENAMER_OT_applyname_rig(bpy.types.Operator):
    bl_idname = "n3st_renamer.applyname_rig"
    bl_label = "Rig"
    bl_description = "Rename the selection of ARMATURES into a given prefix."
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        sel = context.selected_objects
        prefix = getattr(context.scene, 'newName_rig', "")
        any_renamed = False
        for obj in sel:
            if obj.type == 'ARMATURE':
                if not obj.name.startswith(prefix):
                    obj.name = prefix + "_" + obj.name
                    any_renamed = True
        return {'FINISHED'} if any_renamed else {'CANCELLED'}
def register():
    bpy.types.Scene.newName_rig = bpy.props.StringProperty(name="Rig", default="RIG")
    bpy.utils.register_class(N3ST_RENAMER_OT_applyname_rig)
def unregister():
    bpy.utils.unregister_class(N3ST_RENAMER_OT_applyname_rig)
    del bpy.types.Scene.newName_rig
