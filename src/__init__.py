from . import sentry
from . import props
from . import operators
from . import core
from . import timers
from . import panels

bl_info = {
    "name": "Cubr",
    "blender": (3, 00, 0),
    "category": "Object",
    "location": "View3D > Sidebar > Cubr",
    "author": "cubr.io",
    "version": (1, 9, 0),
}

sentry.init()


def register():
    operators.register()
    panels.register()
    props.register()
    print("Cubr: Registered")


def unregister():
    core.unregister()
    operators.unregister()
    panels.unregister()
    props.unregister()
    timers.unregister()

    print("Cubr: Unregistered")
