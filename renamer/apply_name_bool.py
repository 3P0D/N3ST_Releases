import bpy
class N3ST_RENAMER_OT_applyname_bool(bpy.types.Operator):
    bl_idname = "n3st_renamer.applyname_bool"
    bl_label = "Bool"
    bl_description = "Rename the selection of BOOLS into a given prefix."
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        sel = context.selected_objects
        prefix = getattr(context.scene, 'newName_bool', "")
        any_renamed = False
        for obj in sel:
            if obj.type == 'MESH':
                if not obj.name.startswith(prefix):
                    obj.name = prefix + "_" + obj.name
                    any_renamed = True
        return {'FINISHED'} if any_renamed else {'CANCELLED'}
def register():
    bpy.types.Scene.newName_bool = bpy.props.StringProperty(name="Bool", default="BOOL")
    bpy.utils.register_class(N3ST_RENAMER_OT_applyname_bool)
def unregister():
    bpy.utils.unregister_class(N3ST_RENAMER_OT_applyname_bool)
    del bpy.types.Scene.newName_bool
