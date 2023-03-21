from bpy.types import PropertyGroup
import bpy
import datetime

from . import auth
from . import api
from . import core

from .panels.result import hide_result_panel

is_addon_enabled = False
is_file_ready = False
is_file_saving = False


class CubrProps(PropertyGroup):
    ### Login Session Props ###
    pairing_code: bpy.props.StringProperty(name="Pairing Code", default="")
    login_session_token: bpy.props.StringProperty(
        name="Login Session Token", default="")

    ### File Props ###
    file_id: bpy.props.StringProperty(name="file_id")
    file_status: bpy.props.StringProperty(
        name="file_status", default="Not Synced")
    file_status_icon: bpy.props.StringProperty(
        name="file_status_icon", default="FILE_BACKUP")
    file_last_synced: bpy.props.StringProperty(
        name="file_last_synced", default="-")

    ### Render Props ###
    render_active: bpy.props.BoolProperty(name="render_active", default=False)
    render_animation: bpy.props.BoolProperty(
        name="render_animation", default=False)
    render_id: bpy.props.StringProperty(name="render_id")
    render_file_id: bpy.props.StringProperty(name="render_file_id")

    render_progress: bpy.props.IntProperty(
        name="Progress", default=0, min=0, max=100, step=1, subtype="PERCENTAGE")
    render_status: bpy.props.StringProperty(name="Status")
    render_elapsed: bpy.props.StringProperty(name="Elapsed")
    render_cost: bpy.props.StringProperty(name="Cost")

    last_render_id: bpy.props.StringProperty(name="last_render_id")
    last_render_animation: bpy.props.BoolProperty(name="last_render_anim")
    last_render_status: bpy.props.StringProperty(name="Status")
    last_render_elapsed: bpy.props.StringProperty(name="Elapsed")
    last_render_cost: bpy.props.StringProperty(name="Cost")

    frames_last_polled: bpy.props.StringProperty(name="frames_last_polled")

    ### Output Props ###
    render_output_dir: bpy.props.StringProperty(name="render_output_dir")
    render_output_name: bpy.props.StringProperty(name="render_output_name")
    render_output_use_extension: bpy.props.BoolProperty(
        name="render_output_use_extension", default=True)

    render_file_format: bpy.props.StringProperty(
        name="File Format", default="")
    render_engine: bpy.props.StringProperty(name="Engine", default="")

    ### Boost Props ###
    boost_enabled: bpy.props.BoolProperty(
        name="Boost Enabled", default=False, description="Speed up the render by assigning multiple GPUs to each frame, if capacity is available. This might increase the cost if boost is set too high for small frames")
    boost_amount: bpy.props.IntProperty(
        name="Boost Amount", default=1, min=1, max=8, step=1, description="The maximum number of GPUs to use for each frame")

    auth = auth.CubrAuth()
    api = api.CubrApi(auth)
    core = core.CubrCore(auth)


def init_props():
    if not ".cubr" in bpy.data.texts:
        bpy.data.texts.new(".cubr")
    bpy.types.Text.cubr_props = bpy.props.PointerProperty(
        type=CubrProps)


def props():
    if ".cubr" in bpy.data.texts:
        if hasattr(bpy.types.Text, "cubr_props"):
            return bpy.data.texts[".cubr"].cubr_props
        else:
            print("Cubr: CubrProps not found")
            return None


def auth():
    return props().auth


def core():
    return props().core


def api():
    return props().api


def clear():
    clear_render()
    clear_last_render()
    auth().clearLoginSession()
    global is_file_ready
    is_file_ready = False


def clear_render():
    props().render_active = False
    props().render_id = ""
    props().render_file_id = ""
    props().render_status = "Pending"
    props().render_progress = 0
    props().render_output_dir = ""
    props().render_output_name = ""
    props().frames_last_polled = datetime.datetime.fromtimestamp(
        0).strftime('%Y-%m-%d %H:%M:%S')


def clear_last_render():
    if props() == None:
        return

    props().last_render_id = ""
    props().last_render_animation = False
    props().last_render_status = ""
    props().last_render_elapsed = ""
    props().last_render_cost = ""

    hide_result_panel()


def register():
    bpy.utils.register_class(CubrProps)
    global is_addon_enabled, is_file_ready
    is_addon_enabled = False
    is_file_ready = False


def unregister():
    bpy.utils.unregister_class(CubrProps)
    if hasattr(bpy.types.Text, "cubr_props"):
        del bpy.types.Text.cubr_props
