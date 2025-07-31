import bpy
MAX_COLORS = 24
DEFAULT_COLOR = (0.025, 0.025, 0.025, 1.0)
DEBUG_COLORS = [
    (0.5, 0.0, 0.5, 1.0),   
    (1.0, 0.0, 0.0, 1.0),   
    (1.0, 0.1, 0.0, 1.0),   
    (1.0, 1.0, 0.0, 1.0),   
    (0.0, 1.0, 0.0, 1.0),   
    (0.0, 1.0, 1.0, 1.0),   
    (0.0, 0.0, 1.0, 1.0),   
    (0.1, 0.0, 1.0, 1.0),   
]
def update_color(self, context):
    scene = context.scene
    index = None
    for i, item in enumerate(scene.my_colors):  
        if item == self:                        
            index = i                          
            break                             
    if index is None or index < 0:
        return
    color = self.color
    name = f"MAT_DEBUG_{index + 1:02d}"
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
    nodes = mat.node_tree.nodes
    shd = nodes.get("Principled BSDF")
    if shd is None:
        shd = nodes.new(type="ShaderNodeBsdfPrincipled")
        out = nodes.get("Material Output")
        if out and not out.inputs['Surface'].is_linked:
            mat.node_tree.links.new(shd.outputs['BSDF'], out.inputs['Surface'])
    shd.inputs['Base Color'].default_value = color
    mat.diffuse_color = color
def update_color_count(self, context):
    col = context.scene.my_colors
    target = context.scene.color_count
    while len(col) < target:
        item = col.add()
        item.color = DEFAULT_COLOR   
    while len(col) > target:
        col.remove(len(col) - 1)    
class N3ST_ColorPickers(bpy.types.PropertyGroup):
    color: bpy.props.FloatVectorProperty(
        name="Color",          
        subtype='COLOR',       
        size=4,                
        min=0.0, max=1.0,     
        default=DEFAULT_COLOR, 
        update=update_color           
    )  
class N3ST_TEXMAT_OT_assign_mat(bpy.types.Operator):
    bl_idname = "n3st_texmat.pick_assign_mat"
    bl_label = "Assign Material"
    bl_description = "Assign the corresponding material to the selected object or faces."
    bl_options = {'REGISTER', 'UNDO'}
    idx: bpy.props.IntProperty()  
    @classmethod
    def poll(cls, context):
        obj = context.active_object  
        return obj is not None and obj.type == 'MESH'
    def execute(self, context):
        obj = context.active_object  
        idx = self.idx                
        color = context.scene.my_colors[idx].color  
        name = f"MAT_DEBUG_{idx+1:02d}"
        mat = bpy.data.materials.get(name)
        if mat is None:  
            mat = bpy.data.materials.new(name)
        mat.use_nodes = True  
        nodes = mat.node_tree.nodes
        shd = nodes.get("Principled BSDF")
        if not shd:
            shd = nodes.new(type="ShaderNodeBsdfPrincipled")
            out = nodes.get("Material Output")
            if out and not out.inputs['Surface'].is_linked:
                mat.node_tree.links.new(shd.outputs['BSDF'], out.inputs['Surface'])
        shd.inputs['Base Color'].default_value = color
        mat.diffuse_color = color
        mesh = obj.data
        if obj.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')  
            if mat.name not in mesh.materials:
                mesh.materials.append(mat)  
            idx_mat = mesh.materials.find(mat.name)  
            for poly in mesh.polygons:
                if poly.select:
                    poly.material_index = idx_mat  
            bpy.ops.object.material_slot_remove_unused()  
            bpy.ops.object.mode_set(mode='EDIT')  
            self.report({'INFO'}, f"N3ST: {mat.name} assigned to selected faces.") 
        else:
            mesh.materials.clear()  
            mesh.materials.append(mat)  
            for poly in mesh.polygons:
                poly.material_index = 0  
            self.report({'INFO'}, f"N3ST: {mat.name} assigned to the object.")  
        return {'FINISHED'}
class N3ST_TEXMAT_OT_debug_palette(bpy.types.Operator):
    bl_idname = "n3st_texmat.pick_debug_palette"
    bl_label = "Palette Debug (8 Colours)"
    bl_description = "Fill the palette with 8 debug colours: red, green, blue, cyan, magenta, yellow, orange and purple."
    def execute(self, context):
        scene = context.scene
        col = scene.my_colors
        target_count = len(DEBUG_COLORS)
        while len(col) < target_count:
            item = col.add()
            item.color = DEFAULT_COLOR
        while len(col) > target_count:
            col.remove(len(col) - 1)
        for i, c in enumerate(DEBUG_COLORS):
            col[i].color = c
        scene.color_count = target_count
        self.report({'INFO'}, "N3ST: Debug palette generated!")
        return {'FINISHED'}
def register():
    bpy.utils.register_class(N3ST_ColorPickers)
    bpy.utils.register_class(N3ST_TEXMAT_OT_assign_mat)
    bpy.utils.register_class(N3ST_TEXMAT_OT_debug_palette)
    bpy.types.Scene.my_colors = bpy.props.CollectionProperty(type=N3ST_ColorPickers)
    bpy.types.Scene.color_count = bpy.props.IntProperty(
        name="Color Pickers", min=1, max=MAX_COLORS,
        default=0, update=update_color_count)
def unregister():
    bpy.utils.unregister_class(N3ST_TEXMAT_OT_assign_mat)
    bpy.utils.unregister_class(N3ST_TEXMAT_OT_debug_palette)
    bpy.utils.unregister_class(N3ST_ColorPickers)
    del bpy.types.Scene.my_colors
    del bpy.types.Scene.color_count
