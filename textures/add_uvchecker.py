import bpy
def add_checker_material(obj, context, size=512):
    if obj is None or not hasattr(obj.data, "materials"):
        return
    obj.data.materials.clear()
    name = f"T_checker_{size}"  
    matname = f"MAT_checker_{size}"  
    if matname in bpy.data.materials:
        mat = bpy.data.materials[matname]
    else:
        mat = bpy.data.materials.new(name=matname)
        mat.use_nodes = True
    shd = mat.node_tree.nodes.get("Principled BSDF")
    texImg = mat.node_tree.nodes.get('Image Texture')
    if not texImg:
        texImg = mat.node_tree.nodes.new('ShaderNodeTexImage')
    if name not in bpy.data.images:
        bpy.ops.image.new(name=name, width=size, height=size, color=(0.0, 0.0, 0.0, 1.0), alpha=True, generated_type='COLOR_GRID', float=False)
    texImg.image = bpy.data.images.get(name)
    if shd and texImg:
        mat.node_tree.links.new(texImg.outputs[0], shd.inputs[0])
    obj.data.materials.append(mat)
    try:
        area = next((a for a in context.screen.areas if a.type == 'VIEW_3D'), None)
        if area:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.color_type = 'TEXTURE'
    except Exception:
        pass
class N3ST_TEXMAT_OT_addchecker_512(bpy.types.Operator):
    bl_idname = "n3st_texmat.addchecker_512"
    bl_label = "512"
    def execute(self, context):
        obj = context.object
        add_checker_material(obj, context, 512)  
        return {'FINISHED'}
class N3ST_TEXMAT_OT_addchecker_1024(bpy.types.Operator):
    bl_idname = "n3st_texmat.addchecker_1024"
    bl_label = "1024"
    def execute(self, context):
        obj = context.object
        add_checker_material(obj, context, 1024)  
        return {'FINISHED'}
class N3ST_TEXMAT_OT_addchecker_2048(bpy.types.Operator):
    bl_idname = "n3st_texmat.addchecker_2048"
    bl_label = "2048"
    def execute(self, context):
        obj = context.object
        add_checker_material(obj, context, 2048)  
        return {'FINISHED'}
class N3ST_TEXMAT_OT_addchecker_4096(bpy.types.Operator):
    bl_idname = "n3st_texmat.addchecker_4096"
    bl_label = "4096"
    def execute(self, context):
        obj = context.object
        add_checker_material(obj, context, 4096)  
        return {'FINISHED'}
def register():
    bpy.utils.register_class(N3ST_TEXMAT_OT_addchecker_512)
    bpy.utils.register_class(N3ST_TEXMAT_OT_addchecker_1024)
    bpy.utils.register_class(N3ST_TEXMAT_OT_addchecker_2048)
    bpy.utils.register_class(N3ST_TEXMAT_OT_addchecker_4096)
def unregister():
    bpy.utils.unregister_class(N3ST_TEXMAT_OT_addchecker_4096)
    bpy.utils.unregister_class(N3ST_TEXMAT_OT_addchecker_2048)
    bpy.utils.unregister_class(N3ST_TEXMAT_OT_addchecker_1024)
    bpy.utils.unregister_class(N3ST_TEXMAT_OT_addchecker_512)
