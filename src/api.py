import requests

from . import config


class CubrApi:
    def __init__(self, auth):
        self.auth = auth

    def render_still(self, file_id, boost, settings):
        return requests.post(config.RENDER_API_URL + '/render/still', json={
            'file_id': file_id,
            'frame': settings["frame_current"],
            'boost': boost,
            'settings': settings
        }, headers=self.auth.headers)

    def render_animation(self, file_id, boost, settings):
        return requests.post(config.RENDER_API_URL + '/render/animation', json={
            'file_id': file_id,
            'frame_start': settings["frame_start"],
            'frame_end': settings["frame_end"],
            'frame_step': settings["frame_step"],
            'boost': boost,
            'settings': settings
        }, headers=self.auth.headers)

    def cancel_render(self, render_id):
        return requests.post(config.RENDER_API_URL + '/render/' + render_id + '/cancel', headers=self.auth.headers)

    def refresh_token(self, refresh_token):
        return requests.post(config.SUPABASE_URL + '/auth/v1/token?grant_type=refresh_token', json={
            'refresh_token': refresh_token
        }, headers=self.auth.headers)

    def get_render(self, render_id):
        return requests.get(config.SUPABASE_URL + '/rest/v1/renders?select=start_time,end_time,cost_billed,status,progress&id=eq.' + render_id, headers=self.auth.headers)

    def get_frames(self, render_id, last_polled):
        return requests.get(config.SUPABASE_URL + '/rest/v1/frames?select=frame&render_id=eq.' + render_id + '&status=eq.complete&order=frame.asc&end_time=gte.' + last_polled, headers=self.auth.headers)

    def get_frame(self, file_id, render_id, frame):
        return requests.get(config.FRAME_API_URL + "/frame/" + file_id + "/" + render_id + "/" + str(frame), headers=self.auth.headers)

    def get(self, path):
        return requests.get(config.API_URL + path, headers=self.auth.headers)

    def post(self, path, data):
        return requests.post(config.API_URL + path, json=data, headers=self.auth.headers)
