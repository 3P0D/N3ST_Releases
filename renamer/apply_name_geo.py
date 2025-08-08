import bpy
class N3ST_RENAMER_OT_applyname_geo(bpy.types.Operator):
    bl_idname = "n3st_renamer.applyname_geo"
    bl_label = "Mesh"
    bl_description = "Rename the selection of MESHES into a given prefix."
    bl_options = {'REGISTER', 'UNDO'}
    prefix: bpy.props.StringProperty(
        name="Mesh",
        default="GEO",
        description="Prefix to add to all selected MESH objects"
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
classes = [
    N3ST_RENAMER_OT_applyname_geo,
]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
