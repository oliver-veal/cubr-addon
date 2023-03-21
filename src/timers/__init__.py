import bpy

from .auth import poll_login, refresh_token_timer
from .render import poll_render
from .file import handle_save_queue, handle_tag_redraw_queue

TIMERS = [
    poll_login,
    refresh_token_timer,
    poll_render,
    handle_save_queue,
    handle_tag_redraw_queue
]


def unregister():
    file.unregister()

    for timer in TIMERS:
        if bpy.app.timers.is_registered(timer):
            bpy.app.timers.unregister(timer)
