import bpy


class OperatorInfo(bpy.types.Operator):
    """Log info message"""
    bl_idname = "cubr.info"
    bl_label = "Info"

    def execute(self, context):
        self.report({'INFO'}, "A message")
        return {'FINISHED'}
