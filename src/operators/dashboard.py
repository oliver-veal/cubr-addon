import bpy
from bpy.types import Operator

from .. import props
from .. import config


class OperatorOpenDashboard(Operator):
    """Open the dashboard in your browser"""
    bl_label = "Dashboard"
    bl_idname = "cubr.open_dashboard"

    def execute(self, context):
        if not props.is_addon_enabled:
            self.report({'ERROR'}, "Cubr is not enabled")
            return {'CANCELLED'}

        if not props.auth().is_user_logged_in:
            self.report({'ERROR'}, "You are not logged in")
            return {'CANCELLED'}

        url = config.DASHBOARD_URL
        bpy.ops.wm.url_open(url=url)

        return {'FINISHED'}


class OperatorOpenRenderInDashboard(Operator):
    """Open the render in the dashboard in your browser"""
    bl_label = "Open in Dashboard"
    bl_idname = "cubr.open_render_dashboard"

    def execute(self, context):
        if not props.is_addon_enabled:
            self.report({'ERROR'}, "Cubr is not enabled")
            return {'CANCELLED'}

        if not props.auth().is_user_logged_in:
            self.report({'ERROR'}, "You are not logged in")
            return {'CANCELLED'}

        url = config.DASHBOARD_URL + "/render/" + props.props().last_render_id
        bpy.ops.wm.url_open(url=url)

        return {'FINISHED'}


class OperatorOpenSupport(Operator):
    """Open Cubr support in your browser"""
    bl_label = "Support"
    bl_idname = "cubr.open_support"

    def execute(self, context):
        url = config.DASHBOARD_URL + "/support"
        bpy.ops.wm.url_open(url=url)

        return {'FINISHED'}
