import bpy
class N3ST_3DVIEW_OT_prepsculpt(bpy.types.Operator):
    bl_idname = "n3st_3dview.prepsculpt"
    bl_label = "Autoremesh"
    bl_description = "Apply transforms, join, add a Remesh modifier (not applied)"
    remesh_voxel: bpy.props.FloatProperty(
        name='Remesh Voxel',
        default=0.01,
        min=0.0001,
        max=0.5
    ) 
    def execute(self, context):
        if not context.selected_objects:
            self.report({'WARNING'}, "N3ST: Select at least one object.")
            return {'CANCELLED'}
        for obj in context.selected_objects:
            context.view_layer.objects.active = obj
            bpy.ops.object.convert(target='MESH')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.join()
        obj = context.active_object
        bpy.ops.object.modifier_add(type='REMESH')
        remesh = obj.modifiers.get("Remesh")
        if remesh:
            remesh.voxel_size = self.remesh_voxel
        return {'FINISHED'}
def register():
    bpy.utils.register_class(N3ST_3DVIEW_OT_prepsculpt)
def unregister():
    bpy.utils.unregister_class(N3ST_3DVIEW_OT_prepsculpt)
