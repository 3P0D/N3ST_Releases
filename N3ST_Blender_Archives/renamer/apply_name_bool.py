import bpy
class N3ST_RENAMER_OT_applyname_bool(bpy.types.Operator):
    bl_idname = "n3st_renamer.applyname_bool"
    bl_label = "Bool"
    bl_description = "Rename the selection of BOOLS into a given prefix."
    bl_options = {'REGISTER', 'UNDO'}
    prefix: bpy.props.StringProperty(
        name="Bool",
        default="BOOL",
        description="Prefix to add to selected MESH objects used as bools"
    )
    def execute(self, context):
        sel = context.selected_objects
        prefix = self.prefix
        any_renamed = False
        for obj in sel:
            if obj.type == 'MESH':
                if not obj.name.startswith(prefix):
                    obj.name = prefix + "_" + obj.name
                    any_renamed = True
        return {'FINISHED'} if any_renamed else {'CANCELLED'}
classes = [N3ST_RENAMER_OT_applyname_bool]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
