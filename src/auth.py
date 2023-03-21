import bpy
import time


from . import cache
from . import config
from . import props
from .timers.auth import refresh_token_timer
from .timers.file import file_change_handler

from .panels.file import show_file_panel
from .panels.render import show_render_panel


class CubrAuth:
    def __init__(self):
        self.access_token = ''
        self.refresh_token = ''
        self.expires_at = 0
        self.headers = {}
        self.is_user_logged_in = False

    def build_headers(self):
        self.headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json",
            "apikey": config.SUPABASE_KEY,
        }

    def logout(self):
        self.access_token = ''
        self.refresh_token = ''
        self.headers = {}

        cache.Cache.delete_key("access_token")
        cache.Cache.delete_key("refresh_token")

        self.is_user_logged_in = False

        props.clear()
        file_change_handler(None)

    def login(self, access_token, refresh_token, expires_at):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at
        self.build_headers()

        cache.Cache.save_key("access_token", access_token)
        cache.Cache.save_key("refresh_token", refresh_token)

        if expires_at > 0:
            bpy.app.timers.register(
                refresh_token_timer,
                # refresh the token 5 minutes before it expires
                first_interval=max(expires_at - 5 * 60 - time.time(), 0),
            )

        self.is_user_logged_in = True

        show_file_panel()
        show_render_panel()

    def clearLoginSession(self):
        props.props().pairing_code = ""
        props.props().login_session_token = ""
