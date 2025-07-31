import bpy
class N3ST_DATAS_OT_remove_unused_vertex_groups(bpy.types.Operator):
    bl_idname = "n3st_datas.remove_unused_vertex_groups"
    bl_label = "Remove Unused Vertex Groups"
    bl_description = "Removes all vertex groups without assigned vertices with weight > 0."
    bl_options = {'REGISTER', 'UNDO'}
    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj is not None and obj.type == 'MESH'
    def execute(self, context):
        obj = context.object
        obj.update_from_editmode()
        used_groups = [False] * len(obj.vertex_groups)
        for v in obj.data.vertices:
            for g in v.groups:
                if g.weight > 0:
                    used_groups[g.group] = True
        removed_count = 0
        for i in reversed(range(len(used_groups))):
            if not used_groups[i]:
                obj.vertex_groups.remove(obj.vertex_groups[i])
                removed_count += 1
        self.report({'INFO'}, f"N3ST: Deleted {removed_count} Vertex Groups!")
        return {'FINISHED'}
def draw_remove_unused(self, context):
    self.layout.operator(
        N3ST_DATAS_OT_remove_unused_vertex_groups.bl_idname,
        icon='X'
    )
def register():
    bpy.utils.register_class(N3ST_DATAS_OT_remove_unused_vertex_groups)
    bpy.types.DATA_PT_vertex_groups.append(draw_remove_unused)
def unregister():
    bpy.types.DATA_PT_vertex_groups.remove(draw_remove_unused)
    bpy.utils.unregister_class(N3ST_DATAS_OT_remove_unused_vertex_groups)
if __name__ == "__main__":
    register()
