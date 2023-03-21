from bpy.app.handlers import persistent
import time
import threading
import uuid
import queue
import bpy
import datetime

from .. import props
from ..panels.file import hide_file_panel
from ..panels.render import hide_render_panel
from ..panels.result import hide_result_panel

save_queue = queue.Queue(maxsize=1)
tag_redraw_queue = queue.Queue()


@ persistent
def save_handler(dummy):
    if not props.is_addon_enabled or not props.auth().is_user_logged_in:
        return

    try:
        save_queue.put(save_file, block=False)
    except queue.Full:
        print("Cubr: Save queue is full, skipping save")
        pass


def save_file():
    print("Cubr: Saving")

    if not props.is_addon_enabled or not bpy.data.use_autopack:
        props.is_file_ready = False
        props.is_file_saving = False
        return

    props.props().file_status_icon = "FILE_REFRESH"
    props.props().file_status = "Syncing"
    tag_redraw_queue.put(True)

    file_format = bpy.context.scene.render.image_settings.file_format
    engine = bpy.context.scene.render.engine

    try:
        r = props.core().emit_file_saved_event(bpy.data.filepath, props.props().file_id)

        if r.status_code == 200:
            print("Cubr: Saved")
            props.props().render_file_format = file_format
            props.props().render_engine = engine

            props.props().file_status = "Synced"
            props.props().file_status_icon = "CHECKMARK"
            props.props().file_last_synced = datetime.datetime.fromtimestamp(
                time.time()).strftime('%H:%M:%S')
            props.is_file_ready = True
        else:
            raise Exception("Cubr: Failed to save file: " +
                            str(r.status_code) + " " + r.text)

    except Exception as e:
        print("Cubr: Failed to save: ", e)
        props.props().file_status_icon = "ERROR"
        props.props().file_status = "Error"
        props.is_file_ready = False

    tag_redraw_queue.put(True)
    props.is_file_saving = False


def handle_save_queue():
    if props.is_file_saving:
        return 0.1

    if not save_queue.empty():
        props.is_file_saving = True
        func = save_queue.get()
        threading.Thread(target=func).start()

    return 0.1


def handle_tag_redraw_queue():
    if not tag_redraw_queue.empty():
        tag_redraw_queue.get()
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()

    return 0.1


@ persistent
def file_change_handler(dummy):
    print("Cubr: File changed")

    # Clear the save queue
    global save_queue
    save_queue = queue.Queue(maxsize=1)

    props.is_addon_enabled = False
    props.is_file_ready = False

    hide_result_panel()
    hide_render_panel()
    hide_file_panel()

    if props.props() is None:
        return

    activate()

    props.clear_last_render()

    props.props().file_status_icon = "INFO"
    props.props().file_status = "Save file to sync"

    if props.props().file_id == "":
        print("Cubr: File not registered")
        props.props().file_id = str(uuid.uuid4())

    print("Cubr: File ID: " + props.props().file_id)


def activate():
    if not save_handler in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.append(save_handler)
    if not file_change_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(file_change_handler)

    bpy.app.timers.register(handle_save_queue)
    bpy.app.timers.register(handle_tag_redraw_queue)


def unregister():
    if save_handler in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.remove(save_handler)
    if file_change_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(file_change_handler)
