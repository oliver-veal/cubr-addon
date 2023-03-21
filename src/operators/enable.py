from bpy.types import Operator
import time

from .. import props
from .. import cache
from ..timers.file import file_change_handler

from ..panels.file import show_file_panel
from ..panels.render import show_render_panel
from ..panels.result import show_result_panel


class OperatorEnable(Operator):
    """Activate the addon"""
    bl_label = "Cubr: Enable"
    bl_idname = "cubr.enable"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        props.init_props()
        props.clear()
        file_change_handler(None)
        load_cache()

        if not start_core():
            self.report({'ERROR'}, "Failed to connect to core")
            return {'CANCELLED'}

        props.is_addon_enabled = True
        print("Cubr: Enabled")
        return {'FINISHED'}


def load_cache():
    cache_data = cache.Cache.read()

    if "access_token" in cache_data and "refresh_token" in cache_data:
        props.auth().login(
            cache_data["access_token"],
            cache_data["refresh_token"],
            int(time.time())
        )

    print("Cubr: Cache loaded")


def start_core():
    props.core().start()

    attempts = 10
    connected = False
    while attempts > 0:
        attempts -= 1
        time.sleep(0.1)
        try:
            r = props.core().get("/ping")

            if r.status_code == 200:
                connected = True
                break
        except:
            pass

    if connected:
        print("Cubr: Core connection OK after " +
              str(10 - attempts) + " attempts")
    else:
        print("Cubr: Failed to connect to core")

    return connected
