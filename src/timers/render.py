import bpy
import datetime

from .. import props
from ..common.render import get_completed_frames
from ..panels.result import show_result_panel


def poll_render():
    p = props.props()
    if not props.is_addon_enabled or not props.auth().is_user_logged_in or not p.render_active:
        props.clear_render()
        return None

    interval = 1

    try:
        r = props.api().get_render(p.render_id)

        if r.status_code == 404:
            return 1

        if r.status_code != 200:
            raise Exception(str(r.status_code) + " " + r.text)

        res = r.json()[0]

        p.render_status = res['status']
        p.render_progress = 0 if res['progress'] == None else res['progress']
        cost = 0 if res['cost_billed'] == None else res['cost_billed']
        p.render_cost = formatCost(cost)

        p.render_elapsed = getElapsed(res['start_time'], res['end_time'])

        if res['status'] == 'complete' or res['status'] == 'failed' or res['status'] == 'canceled':
            p.last_render_id = p.render_id
            p.last_render_animation = p.render_animation
            p.last_render_status = p.render_status
            p.last_render_elapsed = p.render_elapsed
            p.last_render_cost = p.render_cost
            show_result_panel()

            get_completed_frames()
            props.clear_render()
            print("Cubr: Render " + res['status'])
            interval = None
        else:
            get_completed_frames()

    except Exception as e:
        print("Cubr: Failed to get render: ", e)
        props.clear_render()

    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()

    return interval


def formatCost(cost):
    return "£{:.2f}".format(cost)


def getElapsed(start_time, end_time):
    try:
        if start_time != None:
            start_time = datetime.datetime.strptime(
                start_time, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=datetime.timezone.utc)

            if end_time != None:
                end_time = datetime.datetime.strptime(
                    end_time, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=datetime.timezone.utc)
                return formatElapsed((end_time - start_time).seconds)
            else:
                now = datetime.datetime.now(tz=datetime.timezone.utc)
                return formatElapsed((now - start_time).seconds)
        else:
            return "pending"
    except Exception as e:
        print("Cubr: Failed to get elapsed: ", e)
        pass

    return "pending"


def formatElapsed(seconds):
    # e.g. 1h 2m 3s
    # e.g. 2m 3s
    # e.g. 3s

    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    if hours > 0:
        return str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s"
    elif minutes > 0:
        return str(minutes) + "m " + str(seconds) + "s"
    else:
        return str(seconds) + "s"
