import bpy
class N3ST_RENAMER_OT_applyname_empty(bpy.types.Operator):
    bl_idname = "n3st_renamer.applyname_empty"
    bl_label = "Empty"
    bl_description = "Rename the selection of EMPTIES into a given prefix."
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        sel = context.selected_objects
        prefix = getattr(context.scene, 'newName_empty', "")
        any_renamed = False
        for obj in sel:
            if obj.type == 'EMPTY':
                if not obj.name.startswith(prefix):
                    obj.name = prefix + "_" + obj.name
                    any_renamed = True
        return {'FINISHED'} if any_renamed else {'CANCELLED'}
def register():
    bpy.types.Scene.newName_empty = bpy.props.StringProperty(name="Empty", default="EMPT")
    bpy.utils.register_class(N3ST_RENAMER_OT_applyname_empty)
def unregister():
    bpy.utils.unregister_class(N3ST_RENAMER_OT_applyname_empty)
    del bpy.types.Scene.newName_empty
