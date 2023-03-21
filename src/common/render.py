import bpy
import os
import time
import datetime

from .. import props


def fetch_frame(file_id, render_id, frame, animation):
    try:
        r = props.api().get_frame(file_id, render_id, frame)

        if r.status_code != 200:
            e = str(r.status_code) + " " + r.text
            raise Exception("Cubr: Failed to get frame: " + e)

        p = props.props()
        out_path = p.render_output_dir

        if not os.path.isdir(out_path):
            raise Exception(
                "Cubr: Output directory does not exist: " + out_path)

        if animation:
            out_path = os.path.join(out_path, get_frame_name(
                p.render_output_name, frame, p.render_output_use_extension))
        else:
            out_path = os.path.join(out_path, "Cubr Render Result.png")

        with open(out_path, "wb") as f:
            f.write(r.content)

        if not animation:
            view_frame(out_path)

        return 1
    except Exception as e:
        print("Cubr: Failed to get frame:", e)
        return 1


def get_frame_name(template, frame, use_extension):
    name = template

    max_index, max_length = find_last_hash_block(template)
    if max_index > -1:
        name = template[:max_index] + \
            str(frame).zfill(max_length) + template[max_index + max_length:]
    else:
        name = template + str(frame).zfill(4)

    if use_extension:
        if name.endswith("."):
            name = name[:-1]

        if not name.endswith(".png"):
            name += ".png"

    return name


def find_last_hash_block(s):
    max_index = -1
    max_length = 0
    current_index = -1
    current_length = 0
    for i, c in enumerate(s):
        if c == '#':
            if current_index == -1:
                current_index = i
            current_length += 1
        else:
            if current_length > max_length:
                max_length = current_length
                max_index = current_index
            current_index = -1
            current_length = 0
    if current_length > max_length:
        max_length = current_length
        max_index = current_index
    return (max_index, max_length)


def view_frame(path):
    try:
        bpy.ops.render.view_show('INVOKE_DEFAULT')
    except Exception as e:
        print("Cubr: Failed to open render view:", e)

    for image in bpy.data.images:
        if image.name == "Cubr Render Result.png":
            bpy.data.images.remove(image, do_unlink=True)

    img = bpy.data.images.load(path)

    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == 'IMAGE_EDITOR':
                area.spaces.active.image = img
                area.tag_redraw()


def get_completed_frames():
    if not props.is_addon_enabled or not props.auth().is_user_logged_in or not props.props().render_active:
        return None

    try:
        time_now = time.time()
        r = props.api().get_frames(props.props().render_id, props.props().frames_last_polled)
        props.props().frames_last_polled = datetime.datetime.fromtimestamp(
            time_now).strftime('%Y-%m-%d %H:%M:%S')

        frames = r.json()

        if "code" in frames:
            e = str(frames["code"]) + " " + frames["message"]
            raise Exception("Cubr: Failed to get frames: " + e)

        for frame in frames:
            p = props.props()
            fetch_frame(p.render_file_id, p.render_id,
                        frame['frame'], p.render_animation)
    except Exception as e:
        print("Cubr: Failed to get frames:", e)
