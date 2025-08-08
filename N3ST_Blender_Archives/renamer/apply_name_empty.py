import bpy
class N3ST_RENAMER_OT_applyname_empty(bpy.types.Operator):
    bl_idname = "n3st_renamer.applyname_empty"
    bl_label = "Empty"
    bl_description = "Rename the selection of EMPTIES into a given prefix."
    bl_options = {'REGISTER', 'UNDO'}
    prefix: bpy.props.StringProperty(
        name="Empty",
        default="EMPT",
        description="Prefix to add to all selected EMPTY objects"
    )
    def execute(self, context):
        sel = context.selected_objects
        prefix = self.prefix
        any_renamed = False
        for obj in sel:
            if obj.type == 'EMPTY':
                if not obj.name.startswith(prefix):
                    obj.name = prefix + "_" + obj.name
                    any_renamed = True
        return {'FINISHED'} if any_renamed else {'CANCELLED'}
classes = [
    N3ST_RENAMER_OT_applyname_empty,
]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
