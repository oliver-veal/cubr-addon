import bpy


class OperatorEnableAutopack(bpy.types.Operator):
    """External assets must be packed into the blend file for Cubr to work correctly"""
    bl_idname = "cubr.enable_autopack"
    bl_label = "Enable Autopack"

    def execute(self, context):
        bpy.data.use_autopack = True
        return {'FINISHED'}
