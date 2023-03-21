from bpy.types import Operator
import bpy

from .. import config
from .. import props
from ..timers import auth

from ..panels.file import hide_file_panel
from ..panels.render import hide_render_panel
from ..panels.result import hide_result_panel


class OperatorLogin(Operator):
    bl_label = "Login"
    bl_idname = "cubr.login"
    bl_description = "Log in to Cubr via your browser"

    def execute(self, context):
        try:
            r = props.api().get('/addon/create_login_session')

            if r.status_code != 200:
                self.report({'ERROR'}, "Failed to login")
                return {'CANCELLED'}

            res = r.json()

            props.props().pairing_code = res['code']
            props.props().login_session_token = res['token']

            url = config.DASHBOARD_URL + "/addon/confirm_auth/" + res['token']
            bpy.ops.wm.url_open(url=url)

            bpy.app.timers.register(auth.poll_login)

            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, "Failed to login")
            return {'CANCELLED'}


class OperatorCancelLogin(Operator):
    """Cancel login"""
    bl_label = "Cancel"
    bl_idname = "cubr.cancel_login"

    def execute(self, context):
        props.auth().clearLoginSession()
        return {'FINISHED'}


class OperatorLogout(Operator):
    bl_label = "Logout"
    bl_idname = "cubr.logout"
    bl_description = "Log out of Cubr"

    def execute(self, context):
        props.auth().logout()
        props.clear()
        hide_result_panel()
        hide_render_panel()
        hide_file_panel()
        return {'FINISHED'}
