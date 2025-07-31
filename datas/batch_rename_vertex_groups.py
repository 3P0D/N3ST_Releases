import bpy
class N3ST_DATAS_OT_batch_rename_vertex_groups(bpy.types.Operator):
    bl_idname = "n3st_datas.batch_rename_vg"
    bl_label = "Batch Rename Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}  
    mode: bpy.props.EnumProperty(
        items=[
            ('REPLACE', "Replace Word", "Replace a given word within the name."),
            ('PREFIX', "Add Prefix", "Add a prefix to the vertex group."),
            ('SUFFIX', "Add Suffix", "Add a suffix to the vertex group."),
        ],
        name="Mode"
    ) 
    search: bpy.props.StringProperty(name="Old") 
    replace: bpy.props.StringProperty(name="New") 
    affix: bpy.props.StringProperty(name="Value") 
    def _rename_vertex_groups_replace(self, obj, search, replace):
        count = 0  
        for g in obj.vertex_groups:
            new_name = g.name.replace(search, replace)
            if g.name != new_name:
                g.name = new_name
                count += 1
        return count
    def _rename_vertex_groups_prefix(self, obj, prefix):
        count = 0
        for g in obj.vertex_groups:
            if not g.name.startswith(prefix + "_"):
                g.name = prefix + "_" + g.name
                count += 1
        return count
    def _rename_vertex_groups_suffix(self, obj, suffix):
        count = 0
        for g in obj.vertex_groups:
            if not g.name.endswith("_" + suffix):
                g.name = g.name + "_" + suffix
                count += 1
        return count
    def _batch_rename_vertex_groups(self, obj, mode, search="", replace="", affix=""):
        if mode == "REPLACE":
            return self._rename_vertex_groups_replace(obj, search, replace)
        elif mode == "PREFIX":
            return self._rename_vertex_groups_prefix(obj, affix)
        elif mode == "SUFFIX":
            return self._rename_vertex_groups_suffix(obj, affix)
        return 0
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "mode")
        if self.mode == 'REPLACE':
            layout.prop(self, "search")
            layout.prop(self, "replace")
        elif self.mode == 'PREFIX':
            layout.prop(self, "affix", text="Prefix")
        elif self.mode == 'SUFFIX':
            layout.prop(self, "affix", text="Suffix")
    def execute(self, context):
        obj = context.object
        if not obj or obj.type != 'MESH' or not hasattr(obj, "vertex_groups"):
            self.report({'WARNING'}, "N3ST: Select a mesh object with vertex groups.")
            return {'CANCELLED'}
        count = self._batch_rename_vertex_groups(
            obj, self.mode, search=self.search, replace=self.replace, affix=self.affix
        )
        self.report({'INFO'}, f"N3ST: {count} Vertex Group(s) renamed.")
        return {'FINISHED'}
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
def menu_func(self, context):
    self.layout.operator(N3ST_DATAS_OT_batch_rename_vertex_groups.bl_idname, icon="SORTALPHA")
def register():
    bpy.utils.register_class(N3ST_DATAS_OT_batch_rename_vertex_groups)
    bpy.types.DATA_PT_vertex_groups.append(menu_func)
def unregister():
    bpy.types.DATA_PT_vertex_groups.remove(menu_func)
    bpy.utils.unregister_class(N3ST_DATAS_OT_batch_rename_vertex_groups)
if __name__ == "__main__":
    register()
